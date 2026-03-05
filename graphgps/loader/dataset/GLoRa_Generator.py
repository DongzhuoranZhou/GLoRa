from typing import Callable, Optional

import torch
import numpy as np
from torch import Tensor
from typing import List
import networkx as nx
import pickle
import errno, os, stat, shutil
import math

import random

from torch_geometric.data import Data, InMemoryDataset
from torch_geometric.graphgym.config import cfg


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def makedirs_rm_exist(dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=False, onerror=handleRemoveReadonly)
    os.makedirs(dir, exist_ok=True)


def custom_set_dataset_dir(run_dir: str, seed: int):
    """Custom output directory naming for each experiment run.

    Args:
        cfg (CfgNode): Configuration node
        run_id (int): Main for-loop iter id (the random seed or dataset split)
    """
    run_dir = os.path.join(run_dir, "seed_" + str(seed))
    # Make output directory
    if not os.path.isdir(run_dir):
        os.makedirs(run_dir, exist_ok=True)


def index_to_mask(index: Tensor, size: Optional[int] = None) -> Tensor:
    r"""Converts indices to a mask representation.

    Args:
        idx (Tensor): The indices.
        size (int, optional). The size of the mask. If set to :obj:`None`, a
            minimal sized output mask is returned.

    Example:

        >>> index = torch.tensor([1, 3, 5])
        >>> index_to_mask(index)
        tensor([False,  True, False,  True, False,  True])

        >>> index_to_mask(index, size=7)
        tensor([False,  True, False,  True, False,  True, False])
    """
    index = index.view(-1)
    size = int(index.max()) + 1 if size is None else size
    mask = index.new_zeros(size, dtype=torch.bool)
    mask[index] = True
    return mask


def indent(elem, level=0):
    """In-place prettyprint formatter.

    Args:
        elem (Element): XML element to format.
        level (int): Current indentation level.
    """
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class GLoRaDataset(InMemoryDataset):
    r"""A synthetic dataset that returns a GLoRa dataset.

    Args:
        num_graphs (int, optional): The number of graphs. (default: :obj:`1`)
        depth (int, optional): The depth of the GLoRa dataset. (default: :obj:`10`)
        num_classes (int, optional): The number of node features.
            (default: :obj:`64`)
        transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric_utils.data.Data` object and returns a
            transformed version. The data object will be transformed before
            every access. (default: :obj:`None`)
        data_list (List[Data], optional): A list of pre-generated GLoRa graphs.
            If set to :obj:`None`, the dataset will be generated on-the-fly.
            (default: :obj:`None`)
        split (List[int], optional): The split of the dataset into training,
            validation and test set. If set to :obj:`None`, the dataset will
            be randomly split. (default: :obj:`None`)
        save (bool, optional): If set to :obj:`True`, the dataset will be saved
            to disk. (default: :obj:`None`)
        save_path (str, optional): The directory to save the dataset to.
            (default: :obj:`None`)
        **kwargs (optional): Additional arguments of
            :class:`torch_geometric_utils.data.InMemoryDataset`.
    """

    def __init__(
            self,
            num_graphs,
            depth,
            num_classes,
            transform: Optional[Callable] = None,
            data_list: Optional[List[Data]] = None,
            split: Optional[List[int]] = None,
            save: bool = None,
            save_path: str = None,
            **kwargs,
    ):
        super().__init__('.', transform)
        assert depth >= 3, "Depth must be greater than or equal to 3."

        self.num_graphs = num_graphs
        self.type = cfg.GLoRa.type
        self.adapt = cfg.GLoRa.adapt
        self.depth = depth
        self.arity = cfg.GLoRa.arity
        self.fix = cfg.GLoRa.fix
        self.pure_fix = cfg.GLoRa.pure_fix
        self.R_random = cfg.GLoRa.R_random
        self.additional_path_counter = 0

        if save == None:
            self.save = cfg.GLoRa.save
        else:
            self.save = save
        if save_path == None:
            self.save_path = cfg.GLoRa.save_path
        else:
            self.save_path = save_path

        self.dataset_seed = cfg.GLoRa.dataset_seed
        self._num_classes = num_classes
        self.kwargs = kwargs
        if cfg.gnn.layers_mp == 1:
            cfg.gnn.layers_mp = depth
        if split is None:
            split = (self.num_graphs * torch.tensor(cfg.dataset.split)).long()
        self.example_split_num = (self.num_graphs * torch.tensor(cfg.dataset.split)).long()
        if self.type == 'dag':
            if data_list is None:
                data_list, split = self.load_GLoRa_dataset(split=self.example_split_num,
                                                           classes=self._num_classes,
                                                           depth=self.depth,
                                                           arity=self.arity)

                split[1] = split[1] + self.example_split_num[0].numpy()
                split[2] = split[2] + self.example_split_num[0].numpy() + self.example_split_num[1].numpy()

        self.data, self.slices = self.collate(data_list)
        self.data.train_mask = index_to_mask(torch.tensor(split[0], dtype=torch.long), size=len(self.data.y))
        self.data.val_mask = index_to_mask(torch.tensor(split[1], dtype=torch.long),
                                           size=len(self.data.y))
        self.data.test_mask = index_to_mask(
            torch.tensor(split[2], dtype=torch.long),
            size=len(self.data.y))
        self.data.split = split

        custom_set_dataset_dir(self.save_path, self.dataset_seed)
        run_dir = os.path.join(self.save_path, "seed_" + str(self.dataset_seed))
        if self.save:
            save_f_path = os.path.join(run_dir, 'depth_{}.pkl'.format(self.depth))
            with open(save_f_path, 'wb') as f:
                pickle.dump(self, f)

    def load_GLoRa_dataset(self, split=[5000, 500, 500], classes=5, depth=10,
                           arity=2):
        train = self.generate_GLoRa_dataset(depth, arity, classes=classes,
                                            samples=split[0],
                                            )
        val = self.generate_GLoRa_dataset(depth, arity, classes=classes,
                                          samples=split[1],
                                          )
        test = self.generate_GLoRa_dataset(depth, arity, classes=classes,
                                           samples=split[2],
                                           )
        print(f"Train examples: {len(train)}, Validation examples: {len(val)}, Test examples: {len(test)}")

        dataset = train + val + test

        return dataset, [list(range(int(split[i]))) for i in range(3)]

    def generate_GLoRa_graph(self, depth: int, target_label: List[int], arity: int,
                             R_random=False):
        while True:
            if depth <= 2: raise ValueError("Depth K should >= 3")
            k_main_path = np.random.randint(math.floor(2 / 3 * depth),
                                            depth + 1)
            if arity != 1:
                num_nodes_main_path = int((arity ** (k_main_path + 1) - 1) / (arity - 1))
            else:
                num_nodes_main_path = k_main_path + 1
            node_attribute_dict = dict()
            nodes_total_array = np.array([], dtype=int)
            start_index_main_path = 0
            nodes_indices_main_path = np.arange(k_main_path + 1) + start_index_main_path
            nodes_total_array = np.concatenate((nodes_total_array, nodes_indices_main_path))
            target_node_sparse_index = nodes_indices_main_path[-1]

            D = np.concatenate((np.arange(-7, -2, 0.01), np.arange(3, 8, 0.01)))

            y = torch.tensor([np.argmax(target_label)], dtype=torch.long)

            x = np.random.choice(D, size=(num_nodes_main_path, len(target_label)))

            source_node = nodes_indices_main_path[0]

            x[source_node, 0] = 1.0
            x[1:, 1] = 1.0

            edge_index = []

            last_child_counter = 0

            for i in range(num_nodes_main_path - arity ** k_main_path + 1):
                for child in range(1, arity + 1):
                    if last_child_counter + child > num_nodes_main_path - 1:
                        break

                    edge_index.append([i, last_child_counter + child])
                last_child_counter += arity

            for node_index in nodes_indices_main_path:
                vo_0 = source_node
                vo_t = node_index
                t = vo_t - vo_0
                node_attribute_dict[node_index] = (t, k_main_path)
            if R_random:
                R = int(np.random.randint(5 + cfg.GLoRa.m, 11 + cfg.GLoRa.m, size=1))

            else:
                R = 1
            Random_path_nodes_set_P = list()

            self.additional_path_counter = 0
            for p_index in range(R):
                current_num_nodes = max(node_attribute_dict) + 1
                assert current_num_nodes > nodes_total_array.max(), "current_num_nodes: {}, nodes_total_array: {}".format(
                    current_num_nodes, nodes_total_array)

                V_prime, E_prime, X_prime, node_attribute_dict_prime, m_prime, n_prime, K_prime, additional_path_info = self.generate_random_chain(
                    depth=depth, arity=arity,
                    start_index=current_num_nodes,
                    domain=D)

                assert len(set(V_prime).intersection(set(range(current_num_nodes)))) == 0
                x = np.concatenate((x, X_prime), axis=0)
                edge_index = edge_index + E_prime

                new_path_source, new_path_target = V_prime[0], V_prime[-1]

                Vm = [node_index for node_index, (am, k_star) in node_attribute_dict.items() if
                      am == math.floor(
                          ((k_star * (m_prime - 1)) / K_prime) + 1 / 2) and node_index in nodes_total_array]
                vm_from_graph = random.choice(Vm) if Vm else None

                Vn = [node_index for node_index, (am, k_star) in node_attribute_dict.items() if
                      am == math.floor(
                          ((k_star * (n_prime + 1)) / K_prime) + 1 / 2) and node_index in nodes_total_array]
                vn_from_graph = random.choice(Vn) if Vn else None

                edge_index = edge_index + [[vm_from_graph, new_path_source]] + [[new_path_target, vn_from_graph]]

                Random_path_nodes_set_P.append(V_prime)
                node_attribute_dict.update(node_attribute_dict_prime)
                nodes_total_array = np.concatenate((nodes_total_array, V_prime))

            V_shape = x.shape[0]
            Vo_shape = nodes_indices_main_path.shape[0]
            num_holes_upper_limit = V_shape - Vo_shape
            max_holes = np.random.randint(R + 2, R + 4)
            H = max_holes
            if H > num_holes_upper_limit:
                H = num_holes_upper_limit

            Holes_index = list()

            num_nodes = x.shape[0]
            dense_indices = np.arange(num_nodes)
            sparse_to_dense_mapping = dict(zip(nodes_total_array, dense_indices))
            assert len(Random_path_nodes_set_P) == R, print('len(Random_path_nodes_set_P) is not equal to R')
            for Random_path_nodes in Random_path_nodes_set_P:
                random_sample_hole_on_path_p = np.random.choice(Random_path_nodes)
                Holes_index.append(random_sample_hole_on_path_p)
                assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"

            if y == torch.tensor([np.argmax(np.array([1, 0]))], dtype=torch.long):  # negative example

                filtered_main_path = nodes_indices_main_path[
                    ~np.isin(nodes_indices_main_path,
                             np.array([nodes_indices_main_path[0], nodes_indices_main_path[-1]]))]

                random_sample_hole_on_main_path = np.random.choice(filtered_main_path, size=1, replace=False)
                random_sample_hole_on_main_path = random_sample_hole_on_main_path.tolist()
                Holes_index.extend(random_sample_hole_on_main_path)

                assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"
                assert len(Holes_index) == R + 1, 'len(Holes_index) is not equal to num_paths + 1'

                filtered_rest_nodes = nodes_total_array[
                    ~np.isin(nodes_total_array, np.array([nodes_indices_main_path[0], nodes_indices_main_path[-1]]))]
                filtered_rest_nodes = filtered_rest_nodes[
                    ~np.isin(filtered_rest_nodes, np.array(Holes_index))]

                rest_holes_num = H - (R + 1)
                try:
                    assert rest_holes_num >= 0
                except AssertionError:
                    continue  # skip this iteration and start a new one

                assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"
                assert filtered_rest_nodes.shape[0] >= rest_holes_num, print(
                    'filtered_rest_nodes.shape[0] < rest_holes_num')
                if rest_holes_num >= 1:
                    filtered_rest_nodes = nodes_total_array[
                        ~np.isin(nodes_total_array,
                                 np.array([nodes_indices_main_path[0], nodes_indices_main_path[-1]]))]
                    filtered_rest_nodes = filtered_rest_nodes[
                        ~np.isin(filtered_rest_nodes, np.array(Holes_index))]
                    selected_points = np.random.choice(filtered_rest_nodes, size=rest_holes_num, replace=False)
                    selected_points = selected_points.tolist()
                    Holes_index.extend(selected_points)
                    assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"
                    assert len(Holes_index) == (H), print('len(Holes_index) is not equal to H')

                break

            else:
                rest_holes_num = H - R
                assert rest_holes_num >= 0, "rest_holes_num is negative, skipping this iteration"
                assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"
                assert len(Holes_index) == (R), print('len(Holes_index) is not equal to R')
                filtered_rest_nodes_pos = nodes_total_array[
                    ~np.isin(nodes_total_array, np.array(nodes_indices_main_path))]
                filtered_rest_nodes_pos = filtered_rest_nodes_pos[
                    ~np.isin(filtered_rest_nodes_pos, np.array(Holes_index))]
                selected_points = np.random.choice(filtered_rest_nodes_pos, size=rest_holes_num, replace=False)
                selected_points = selected_points.tolist()
                Holes_index.extend(selected_points)
                assert len(Holes_index) == len(set(Holes_index)), "Error: List contains duplicate elements!"
                assert len(Holes_index) == (H), print('len(Holes_index) is not equal to H')
                break

        holes_dense_values = [sparse_to_dense_mapping[point] for point in Holes_index]
        x[holes_dense_values, 1] = 0

        num_nodes = x.shape[0]
        dense_indices = np.arange(num_nodes)
        sparse_to_dense_mapping = dict(zip(nodes_total_array, dense_indices))

        dense_edge_index = [[sparse_to_dense_mapping[edge[0]], sparse_to_dense_mapping[edge[1]]] for edge in edge_index]

        G = nx.DiGraph()
        G.add_nodes_from(range(x.shape[0]))
        G.add_edges_from(dense_edge_index)

        if cfg.GLoRa.direction is False:
            G_undirected = G.to_undirected()
            undirected_edges = list(G_undirected.edges())
            undirected_edges_list = [[edge[0], edge[1]] for edge in undirected_edges]
            dense_edge_index = undirected_edges_list + [[v, u] for u, v in undirected_edges_list]

        num_nodes = x.shape[0]
        shuffled_indices = np.random.permutation(num_nodes)
        dense_to_shuffle_mapping = dict(zip(range(num_nodes), shuffled_indices))
        dense_to_shuffle_mapping_inverse = dict(zip(shuffled_indices, range(num_nodes)))
        shuffled_edge_index = shuffled_indices[dense_edge_index]
        new_indices = np.array(
            [dense_to_shuffle_mapping_inverse[i] for i in range(len(dense_to_shuffle_mapping_inverse))])
        shuffled_x = x[new_indices]

        shuffled_mask = torch.zeros(shuffled_x.shape[0], dtype=torch.bool)
        target_node_dense_index = sparse_to_dense_mapping[target_node_sparse_index]
        target_node_shuffled_index = dense_to_shuffle_mapping[target_node_dense_index]
        shuffled_mask[target_node_shuffled_index] = 1

        shuffled_edge_index = shuffled_edge_index.tolist()
        shuffled_edge_index = np.array(shuffled_edge_index, dtype=np.compat.long).T
        sizes = shuffled_x.shape[0]
        shuffled_edge_index = torch.tensor(shuffled_edge_index, dtype=torch.long)
        shuffled_x = torch.tensor(shuffled_x, dtype=torch.float32)
        assert shuffled_edge_index.min() >= 0 and shuffled_edge_index.max() < sizes, "Index out of bounds"
        return Data(x=shuffled_x, edge_index=shuffled_edge_index, mask=shuffled_mask, y=y)

    def generate_random_chain(self, depth: int, arity: int, start_index=0,
                              domain=None):
        """
        Generate the random chain G'.
        """

        D = domain
        g_p_node_attribute_dict = dict()

        self.additional_path_counter += 1
        K_prime = np.random.randint(math.floor(2 / 3 * depth), depth + 1)

        if K_prime <= 0:
            raise ValueError("Minimum of depth one")
        if arity != 1:
            num_nodes_additional_path = int((arity ** (K_prime + 1) - 1) / (arity - 1))
        else:
            num_nodes_additional_path = K_prime + 1

        V_prime = np.arange(K_prime + 1) + start_index
        X_prime = np.random.choice(D, size=(V_prime.shape[0], 2))
        X_prime[:, 1] = 1.0
        for node_index in V_prime:
            vo_0 = V_prime[0]
            vo_t = node_index
            t = vo_t - vo_0
            g_p_node_attribute_dict[node_index] = (t, K_prime)

        random_selected_points = np.random.choice(V_prime[1:-1], size=2, replace=True)

        idx1 = np.where(V_prime == random_selected_points[0])[0][0]
        idx2 = np.where(V_prime == random_selected_points[1])[0][0]

        start_idx_m = min(idx1, idx2)
        end_idx_n = max(idx1, idx2)
        V_prime_after_cut = V_prime[start_idx_m:end_idx_n + 1]

        E_prime_index = []
        last_child_counter = start_index

        for i in range(start_index, num_nodes_additional_path - arity ** K_prime + 1 + start_index):
            for child in range(1, arity + 1):
                if last_child_counter + child > num_nodes_additional_path - 1 + start_index:
                    break

                E_prime_index.append([i, last_child_counter + child])

            last_child_counter += arity

        filtered_edges = [[vi, vj] for vi, vj in E_prime_index
                          if {vi, vj}.intersection(V_prime_after_cut) == {vi, vj}]
        V_prime_after_cut_minus_start = V_prime_after_cut - start_index

        X_prime_after_cut = X_prime[V_prime_after_cut_minus_start, :]

        m_prime = start_idx_m
        n_prime = end_idx_n

        additional_path_info = {"length": V_prime_after_cut.shape[0], "K_prime": K_prime}

        return V_prime_after_cut, filtered_edges, X_prime_after_cut, g_p_node_attribute_dict, m_prime, n_prime, K_prime, additional_path_info

    def generate_GLoRa_dataset(self, depth: int, arity: int, classes: int = 5,
                               samples: int = 10000):
        dataset = []
        samples_per_class = samples // classes
        for i in range(samples):
            label = int(i // samples_per_class)
            target_class = np.zeros(classes)
            target_class[label] = 1.0
            graph = self.generate_GLoRa_graph(depth=depth,
                                              target_label=target_class,
                                              arity=arity,
                                              R_random=self.R_random)
            dataset.append(graph)
        return dataset
