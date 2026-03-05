from torch_geometric.loader import DataLoader



from torch_geometric.graphgym.config import cfg

from torch_geometric.loader import (GraphSAINTNodeSampler,
                                    GraphSAINTEdgeSampler,
                                    GraphSAINTRandomWalkSampler)
from torch_geometric.loader import ClusterLoader
from torch_geometric.loader import RandomNodeSampler
from torch_geometric.loader import NeighborSampler
from torch_geometric.graphgym.loader import create_dataset  # , get_loader


def create_loader_custom():
    """
    Create data loader object

    Returns: List of PyTorch data loaders

    """
    dataset = create_dataset()
    # train loader
    if cfg.dataset.task == 'graph':
        id = dataset.data['train_graph_index']
        loaders = [
            get_loader(dataset[id], cfg.train.sampler, cfg.train.batch_size,
                       shuffle=True)
        ]
        delattr(dataset.data, 'train_graph_index')
    else:
        train_dataset = [data for data, m in zip(dataset, dataset.data.train_mask.tolist()) if m]
        # torch.nonzero(dataset.data.val_mask).squeeze()
        loaders = [
            get_loader(train_dataset, cfg.train.sampler, cfg.train.batch_size,
                       shuffle=True)
        ]

    # val and test loaders
    for i in range(cfg.share.num_splits - 1):
        if cfg.dataset.task == 'graph':
            split_names = ['val_graph_index', 'test_graph_index']
            id = dataset.data[split_names[i]]
            loaders.append(
                get_loader(dataset[id], cfg.val.sampler, cfg.train.batch_size,
                           shuffle=False))
            delattr(dataset.data, split_names[i])
        else:
            if i == 0:  # val
                val_dataset = [data for data, m in zip(dataset, dataset.data.val_mask.tolist()) if m]
                loaders.append(
                    get_loader(val_dataset, cfg.val.sampler, len(val_dataset),
                               shuffle=False))

            if i == 1:  # test
                test_dataset = [data for data, m in zip(dataset, dataset.data.test_mask.tolist()) if m]
                loaders.append(
                    get_loader(test_dataset, cfg.val.sampler, len(test_dataset),
                               shuffle=False))

    return loaders


def get_loader(dataset, sampler, batch_size, shuffle=True):
    if sampler == "full_batch" or len(dataset) > 1:
        loader_train = DataLoader(dataset, batch_size=batch_size,
                                  shuffle=shuffle, num_workers=cfg.num_workers,
                                  pin_memory=True)
    elif sampler == "neighbor":
        loader_train = NeighborSampler(
            dataset[0], sizes=cfg.train.neighbor_sizes[:cfg.gnn.layers_mp],
            batch_size=batch_size, shuffle=shuffle,
            num_workers=cfg.num_workers, pin_memory=True)
    elif sampler == "random_node":
        loader_train = RandomNodeSampler(dataset[0],
                                         num_parts=cfg.train.train_parts,
                                         shuffle=shuffle,
                                         num_workers=cfg.num_workers,
                                         pin_memory=True)
    elif sampler == "saint_rw":
        loader_train = \
            GraphSAINTRandomWalkSampler(dataset[0],
                                        batch_size=batch_size,
                                        walk_length=cfg.train.walk_length,
                                        num_steps=cfg.train.iter_per_epoch,
                                        sample_coverage=0,
                                        shuffle=shuffle,
                                        num_workers=cfg.num_workers,
                                        pin_memory=True)
    elif sampler == "saint_node":
        loader_train = \
            GraphSAINTNodeSampler(dataset[0], batch_size=batch_size,
                                  num_steps=cfg.train.iter_per_epoch,
                                  sample_coverage=0, shuffle=shuffle,
                                  num_workers=cfg.num_workers,
                                  pin_memory=True)
    elif sampler == "saint_edge":
        loader_train = \
            GraphSAINTEdgeSampler(dataset[0], batch_size=batch_size,
                                  num_steps=cfg.train.iter_per_epoch,
                                  sample_coverage=0, shuffle=shuffle,
                                  num_workers=cfg.num_workers,
                                  pin_memory=True)
    elif sampler == "cluster":
        loader_train = \
            ClusterLoader(dataset[0],
                          num_parts=cfg.train.train_parts,
                          save_dir="{}/{}".format(cfg.dataset.dir,
                                                  cfg.dataset.name.replace(
                                                      "-", "_")),
                          batch_size=batch_size, shuffle=shuffle,
                          num_workers=cfg.num_workers,
                          pin_memory=True)

    else:
        raise NotImplementedError("%s sampler is not implemented!" % sampler)
    return loader_train
