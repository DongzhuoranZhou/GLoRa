import logging
import os
import os.path as osp
import time
from functools import partial
import torch
import torch_geometric.transforms as T

from torch_geometric.data import Data

from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_loader

from graphgps.loader.dataset.GLoRa_Generator import GLoRaDataset
from graphgps.loader.split_generator import (prepare_splits,
                                             set_dataset_splits)
from graphgps.transform.posenc_stats import compute_posenc_stats
from graphgps.transform.transforms import (pre_transform_in_memory, pre_transform_in_memory_glora)
from graphgps.drew_utils import get_edge_labels
from graphgps.make_k_hop_edges import make_k_hop_edges
from tqdm import tqdm
import pickle
from graphgps.preprocessing.fa import make_fa_edges
from graphgps.preprocessing.fosr import make_fosr_edges


def log_loaded_dataset(dataset, format, name):
    logging.info(f"[*] Loaded dataset '{name}' from '{format}':")
    logging.info(f"  {dataset.data}")
    logging.info(f"  undirected: {dataset[0].is_undirected()}")
    logging.info(f"  num graphs: {len(dataset)}")

    total_num_nodes = 0
    if hasattr(dataset.data, 'num_nodes'):
        total_num_nodes = dataset.data.num_nodes
    elif hasattr(dataset.data, 'x'):
        total_num_nodes = dataset.data.x.size(0)
    logging.info(f"  avg num_nodes/graph: "
                 f"{total_num_nodes // len(dataset)}")
    logging.info(f"  num node features: {dataset.num_node_features}")
    logging.info(f"  num edge features: {dataset.num_edge_features}")
    if hasattr(dataset, 'num_tasks'):
        logging.info(f"  num tasks: {dataset.num_tasks}")

    if hasattr(dataset.data, 'y') and dataset.data.y is not None:
        if isinstance(dataset.data.y, list):
            # A special case for ogbg-code2 dataset.
            logging.info(f"  num classes: n/a")
        elif dataset.data.y.numel() == dataset.data.y.size(0) and \
                torch.is_floating_point(dataset.data.y):
            logging.info(f"  num classes: (appears to be a regression task)")
        else:
            logging.info(f"  num classes: {dataset.num_classes}")
    elif hasattr(dataset.data, 'train_edge_label') or hasattr(dataset.data, 'edge_label'):
        # Edge/link prediction task.
        if hasattr(dataset.data, 'train_edge_label'):
            labels = dataset.data.train_edge_label  # Transductive link task
        else:
            labels = dataset.data.edge_label  # Inductive link task
        if labels.numel() == labels.size(0) and \
                torch.is_floating_point(labels):
            logging.info(f"  num edge classes: (probably a regression task)")
        else:
            logging.info(f"  num edge classes: {len(torch.unique(labels))}")


def load_dataset_master(format, name, dataset_dir):
    """
    Master loader that controls loading of all datasets, overshadowing execution
    of any default GraphGym dataset loader. Default GraphGym dataset loader are
    instead called from this function, the format keywords `PyG` and `OGB` are
    reserved for these default GraphGym loaders.

    Custom transforms and dataset splitting is applied to each loaded dataset.

    Args:
        format: dataset format name that identifies Dataset class
        name: dataset name to select from the class identified by `format`
        dataset_dir: path where to store the processed dataset

    Returns:
        PyG dataset object with applied perturbation transforms and data splits
    """

    if format == 'synthetic':
        if name == 'GLoRa':
            if cfg.GLoRa.load is True:
                dataset_path = os.path.join(cfg.GLoRa.load_path,
                                            "seed_" + str(cfg.GLoRa.dataset_seed),
                                            'depth_{}.pkl'.format(cfg.GLoRa.depth))
                with open(dataset_path, 'rb') as f:
                    dataset = pickle.load(f)

            else:
                # if cfg.GLoRa.use_vn or cfg.GLoRa.use_k_longest_path_vn:
                #     dataset = GLoRaDataset_VN(num_graphs=cfg.GLoRa.num_graphs,
                #                                   depth=cfg.GLoRa.depth,
                #                                   num_classes=cfg.GLoRa.num_classes)
                # else:
                dataset = GLoRaDataset(num_graphs=cfg.GLoRa.num_graphs,
                                              depth=cfg.GLoRa.depth,
                                              num_classes=cfg.GLoRa.num_classes)
                # dataset = GLoRaDataset_Adaptive(num_graphs=cfg.GLoRa.num_graphs,
                #                                 depth=cfg.GLoRa.depth,
                #                                 num_classes=cfg.GLoRa.num_classes)


        else:
            ValueError(f"Unknown data format/name: {format}, {name}")
    else:
        raise ValueError(f"Unknown data format: {format}")

    if cfg.sdrf.use and format == 'synthetic':
        from gdl.data.sdrf import SDRFDataset_synthetic
        name = "%s-%s" % (format, name)
        tmp = SDRFDataset_synthetic(name=name, max_steps=round(cfg.GLoRa.depth / 2),
                                    data_dir=cfg.dataset.dir, dataset=dataset, )
        dataset.data, dataset.slices = tmp.process()
    if cfg.fosr.use and format == 'synthetic':
        dataset = make_fosr_edges(dataset, format, name)
    multi_hop_stages = [
        'sp_gnn',
        'drew_gnn',
        'multi_hop_gat',
        'trainable_hop_gat',
        'lran_simple'
    ]
    multi_hop_models = ['drew_gated_gnn', 'drew_gin']
    use_drew = any([
        (cfg.gnn.stage_type in multi_hop_stages),
        ('delay' in cfg.gnn.stage_type),
        (cfg.model.type in multi_hop_models),

    ])

    if cfg.dataset.transform.startswith('digl'):
        avg_degree = int(cfg.dataset.transform[cfg.dataset.transform.index('=') + 1:])
        print('Using GDC transform, average degree %d' % avg_degree)
        alpha_str = '_alpha=p%02d' % int(cfg.digl.alpha * 100) if cfg.digl.alpha != 0.15 else ''
        digl_filepath = osp.join(cfg.dataset.dir, 'k_hop_indices',
                                 '%s_%s_%s%s.pt' % (format, name, cfg.dataset.transform, alpha_str))
        if osp.exists(digl_filepath):
            print('Loading GDC transformed dataset from file %s' % digl_filepath)
            dataset = torch.load(digl_filepath)
        else:
            print('No file %s\nApplying transform...' % digl_filepath)
            os.makedirs(os.path.dirname(digl_filepath), exist_ok=True)
            tf = T.GDC(
                self_loop_weight=1.,
                normalization_in='sym',
                normalization_out='col',
                diffusion_kwargs=dict(method='ppr', alpha=cfg.digl.alpha),
                sparsification_kwargs=dict(method='threshold', avg_degree=avg_degree),
                exact=True,
            )  # using default, except for avg degree
            tf = digl_tf_wrapper(tf)
            if not format == 'synthetic':
                if 1 in dataset.data.edge_attr.shape:
                    dataset = squeeze_edge_attrs(dataset)
                else:
                    dataset = remove_edge_attrs(dataset)
            if format == 'synthetic':
                dataset = pre_transform_in_memory_glora(dataset, tf, show_progress=True)
            else:
                pre_transform_in_memory(dataset, tf, show_progress=True)  # make split mask disappeared
            # try:
            print('Saving file to %s...' % digl_filepath)
            torch.save(dataset, digl_filepath)
        if use_drew or ('noedge' in cfg.gnn.layer_type):
            dataset = remove_edge_attrs(dataset)
        else:
            dataset = unsqueeze_edge_attrs(dataset)

    if cfg.use_edge_labels:
        edge_labels = get_edge_labels(dataset)
        edge_types = [int(torch.unique(edge_labels)[i]) for i in range(len(torch.unique(edge_labels)))]
        n_digits = len(str(max(edge_types)))
        cfg.edge_types = [str(i).zfill(n_digits) for i in edge_types]

    if use_drew:
        k_max = min(cfg.gnn.layers_mp, cfg.k_max)
        dataset = make_k_hop_edges(dataset, k_max, format, name) # A is out-neighbourhood. Keep using out-neighbourhood.
    if cfg.gnn.stage_type == 'fa_gnn':  # add full adjacency matrix
        # every layer or last layer
        dataset = make_fa_edges(dataset, 1, format, name)

    # Precompute necessary statistics for positional encodings.

    pe_enabled_list = []
    for key, pecfg in cfg.items():
        if key.startswith('posenc_') and pecfg.enable:
            pe_name = key.split('_', 1)[1]
            pe_enabled_list.append(pe_name)
            if hasattr(pecfg, 'kernel'):
                # Generate kernel times if functional snippet is set.
                if pecfg.kernel.times_func:
                    pecfg.kernel.times = list(eval(pecfg.kernel.times_func))
                logging.info(f"Parsed {pe_name} PE kernel times / steps: "
                             f"{pecfg.kernel.times}")
    if pe_enabled_list:
        start = time.perf_counter()
        logging.info(f"Precomputing Positional Encoding statistics: "
                     f"{pe_enabled_list} for all graphs...")
        # Estimate directedness based on 10 graphs to save time.
        is_undirected = all(d.is_undirected() for d in dataset[:10])
        logging.info(f"  ...estimated to be undirected: {is_undirected}")
        if format == 'synthetic':
            dataset = pre_transform_in_memory_glora(dataset,
                                                    partial(compute_posenc_stats,
                                                            pe_types=pe_enabled_list,
                                                            is_undirected=is_undirected,
                                                            cfg=cfg),
                                                    show_progress=True
                                                    )

        else:
            pre_transform_in_memory(dataset,
                                    partial(compute_posenc_stats,
                                            pe_types=pe_enabled_list,
                                            is_undirected=is_undirected,
                                            cfg=cfg),
                                    show_progress=True
                                    )
        elapsed = time.perf_counter() - start
        timestr = time.strftime('%H:%M:%S', time.gmtime(elapsed)) \
                  + f'{elapsed:.2f}'[-3:]
        logging.info(f"Done! Took {timestr}")
    log_loaded_dataset(dataset, format, name)
    # Set standard dataset train/val/test splits
    if hasattr(dataset, 'split_idxs'):
        set_dataset_splits(dataset, dataset.split_idxs)
        delattr(dataset, 'split_idxs')

    # Verify or generate dataset train/val/test splits
    prepare_splits(dataset)

    return dataset


register_loader('custom_master_loader', load_dataset_master)


def join_dataset_splits(datasets):
    """Join train, val, test datasets into one dataset object.

    Args:
        datasets: list of 3 PyG datasets to merge

    Returns:
        joint dataset with `split_idxs` property storing the split indices
    """
    assert len(datasets) == 3, "Expecting train, val, test datasets"

    n1, n2, n3 = len(datasets[0]), len(datasets[1]), len(datasets[2])
    data_list = [datasets[0].get(i) for i in range(n1)] + \
                [datasets[1].get(i) for i in range(n2)] + \
                [datasets[2].get(i) for i in range(n3)]

    datasets[0]._indices = None
    datasets[0]._data_list = data_list
    datasets[0].data, datasets[0].slices = datasets[0].collate(data_list)
    split_idxs = [list(range(n1)),
                  list(range(n1, n1 + n2)),
                  list(range(n1 + n2, n1 + n2 + n3))]
    datasets[0].split_idxs = split_idxs

    return datasets[0]


def remove_edge_attrs(dataset):
    """Removes edge attrs from dataset for experiments which don't use them"""
    dataset.data.edge_attr = None
    if any([dataset.get(i).edge_attr is not None for i in range(len(dataset))]):
        print('Removing edge attrs so GDC preprocessing can be performed...')
        count = 0
        for i in tqdm(range(len(dataset))):
            if dataset.get(i).edge_attr is not None:
                count += 1
                dataset._data_list[i] = Data(x=dataset.get(i).x,
                                             edge_index=dataset.get(i).edge_index,
                                             edge_attr=None,
                                             y=dataset.get(i).y)
        assert not any([dataset.get(i).edge_attr is not None for i in range(len(dataset))])
    return dataset


def squeeze_edge_attrs(dataset):
    """Removes edge attrs from dataset for experiments which don't use them"""
    dataset.data.edge_attr = dataset.data.edge_attr.squeeze()
    if any([dataset.get(i).edge_attr.dim() > 1 for i in range(len(dataset))]):
        print('Squeezing edge attrs down to 1D...')
        count = 0
        for i in tqdm(range(len(dataset))):
            if dataset.get(i).edge_attr.dim() > 1:
                count += 1
                dataset._data_list[i] = Data(x=dataset.get(i).x,
                                             edge_index=dataset.get(i).edge_index,
                                             edge_attr=dataset.get(i).edge_attr.squeeze(),
                                             y=dataset.get(i).y)
        assert not any([dataset.get(i).edge_attr.dim() > 1 for i in range(len(dataset))])
    return dataset


def unsqueeze_edge_attrs(dataset, type_config='long'):
    """Turns back into nx1 2d tensor (ie col vector)"""
    if type_config == 'float':
        dataset.data.edge_attr = dataset.data.edge_attr.float()
    dataset.data.edge_attr = dataset.data.edge_attr.reshape(-1, 1)

    if any([dataset.get(i).edge_attr.dim() == 1 for i in range(len(dataset))]):
        print('Reshaping edge attrs...')
        for i in tqdm(range(len(dataset))):
            if dataset.get(i).edge_attr.dim() == 1:
                d_i = dataset.get(i)
                if type_config == 'float':
                    d_i.edge_attr = d_i.edge_attr.float()
                dataset._data_list[i] = Data(x=d_i.x,
                                             edge_index=d_i.edge_index,
                                             edge_attr=d_i.edge_attr.reshape(-1, 1),
                                             y=d_i.y,
                                             edge_index_labeled=getattr(d_i, 'edge_index_labeled', None),  # for PCQM
                                             edge_label=getattr(d_i, 'edge_label', None),  # for PCQM
                                             mask=d_i.mask,
                                             )
        assert all([dataset.get(i).edge_attr.dim() == 2 for i in range(len(dataset))])
    return dataset


def digl_tf_wrapper(f):
    """For DIGL transformation; skipping over graphs with no edges"""

    def wrapper(x):
        if x.edge_index.shape[-1] == 0:
            print('Edgeless graph skipped.')
            if x.edge_attr is None:
                x = Data(edge_index=x.edge_index,
                         x=x.x,
                         edge_index_labeled=x.edge_index_labeled,
                         edge_label=x.edge_label,
                         edge_attr=torch.tensor([])
                         )
            return x
        else:
            return f(x)

    return wrapper
