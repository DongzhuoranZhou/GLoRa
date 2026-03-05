from torch_geometric.utils import to_networkx
from numba import jit, int64
import networkx as nx
import numpy as np
from math import inf



import torch
from torch_geometric.utils import to_dense_adj, dense_to_sparse
from tqdm import tqdm
from torch_geometric.graphgym.config import cfg
import os
from os.path import join, exists
from torch_geometric.data import Data
import copy
import torch
from torch_geometric.utils import to_dense_adj, dense_to_sparse
from tqdm import tqdm
from torch_geometric.graphgym.config import cfg
import os
from os.path import join, exists
from torch_geometric.data import Data
import copy


def make_fosr_edges(dataset, format, name):
    K = 1
    print('Stage type %s, model type %s, using %d-hops' % (cfg.gnn.stage_type, cfg.model.type, K))
    # get k-hop edge amended dataset - either load or make it
    # filedir = join(cfg.dataset.dir, 'k_hop_indices')
    filedir = cfg.dataset.dir
    if not exists(filedir): os.makedirs(filedir)

    # check if files exist already
    slic = '-slic=%02d' % cfg.dataset.slic_compactness if (
                (format == 'PyG-VOCSuperpixels') & (cfg.dataset.slic_compactness != 10)) else ''
    if cfg.dataset.transform != 'none':
        preproc = '-preproc=%s_alpha=p%02d' % (cfg.dataset.transform, int(100 * cfg.digl.alpha))
    else:
        preproc = ''
    extra = ''.join([slic, preproc])

    list_of_K = [1, -20]  # add 1 for FOSR edges indices

    file_exists = [exists(join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, k))) for k in
                   list_of_K]  # list of K bools
    file_exist_dict = {k: exists(join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, k))) for k in
                          list_of_K}  # list of K bools
    if not all(file_exists):  # checks all files are there
        # last_nonexistent_file = max(loc for loc, val in enumerate(file_exists) if val == False) + 1
        last_nonexistent_file = max(loc for loc, val in file_exist_dict.items() if val == False)
        print('Edge index file(s) not found for %s-%s%s_k=%02d (or lower); making file(s) now...' % (
        format, name, extra, last_nonexistent_file))

        # compute_fosr_edges(dataset, filedir, format, name, extra)  # if they don't, make them, here K is always 1
        compute_k_hop_edges(dataset, K, filedir, format, name, extra)

        if not exists(join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, -10))):
            compute_fosr_edges(dataset, filedir, format, name, extra)

    # load files
    all_graphs = []
    print('Loading 1-hop fosr data files...')
    for k in tqdm(list_of_K):
        filepath = join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, k))
        try:
            all_graphs.append(torch.load(filepath))  # [K,N,2,d]
        except:
            files_to_remake = [k]
            # for j in range(K, k, -1):
            for j in range(len(list_of_K) - 1, -1, -1):
                try:
                    torch.load(join(filedir, "%s-%s_k=%02d.pt" % (format, name, k)))
                except:
                    files_to_remake.append(j)
            print('Issue with following files, deleting and remaking them...\nk = ', files_to_remake)
            for j in files_to_remake:
                filepath = join(filedir, "%s-%s_k=%02d.pt" % (format, name, j))
                os.remove(filepath)

            compute_fosr_edges(dataset, filedir, format, name, extra)
            filepath = join(filedir, "%s-%s_k=%02d.pt" % (format, name, k))
            all_graphs.append(torch.load(filepath))  # [K,N,2,d]


    all_hops = [list(n) for n in
                zip(*all_graphs)]  # Transposing. n is graph; all_hops indexed by graph. [N,K,2,d] N is number of graphs, K is number of hops
    labels = []  # get k-hop labels, here k = 1 or -10 (FA)
    for n in all_hops:
        for k, khop in enumerate(n, 1):
            # first is 1-hop, second is fa-hop
            if k == len(n):  # if fully adjacent
                labels += [1 * -20] * khop.shape[-1]
            else:
                labels += [1 * k] * khop.shape[-1]

    labels = torch.tensor(labels, dtype=torch.long)
    all_hops = [torch.cat(n, dim=1) for n in all_hops]  # [K,2,d]
    count, ei_slices = 0, [0]
    for d in all_hops:
        count += d.shape[-1]
        ei_slices.append(count)
    ei_slices = torch.tensor(ei_slices)
    all_hops = torch.cat(all_hops, dim=1)  # [2,d]
    # set to dataset
    dataset.data.edge_index = all_hops
    dataset.data.edge_attr = labels
    dataset.slices['edge_index'] = dataset.slices['edge_attr'] = ei_slices

    print('Checking correct conversion...')
    count = 0
    for i in tqdm(range(len(dataset))):
        if not torch.equal(dataset.get(i).edge_attr.float(),
                           dataset.data.edge_attr[ei_slices[i]:ei_slices[i + 1]].float()):
            # print('Graph %d not changed in dataset._data_list; setting manually' % i)
            count += 1
            dataset._data_list[i] = Data(x=dataset.get(i).x,
                                         edge_index=dataset.data.edge_index[:, ei_slices[i]:ei_slices[i + 1]],
                                         edge_attr=dataset.data.edge_attr[ei_slices[i]:ei_slices[i + 1]],
                                         y=dataset.get(i).y)
        assert torch.equal(dataset.get(i).edge_attr,
                           dataset.data.edge_attr[ei_slices[i]:ei_slices[i + 1]])  # check that the conversion worked
    if count > 0: print('%d/%d graphs not changed in dataset._data_list; have been set manually' % (
    count, len(dataset)))  # this is expected for VOC and COCO

    return dataset


def compute_fosr_edges(dataset, filedir, format, name, extra):
    """take regular dataset, save fully adjacency edges
    from SJLR https://github.com/jhonygiraldo/SJLR
    """
    # we're saving a list of fully adjacency edge indices
    # K = 1 # only need 1-hop for fully adjacency
    edge_indices = dataset.data.edge_index
    slices = dataset.slices['edge_index']  # used to slice the graph
    idxs = [[]] # only need for fosr
    for i in tqdm(range(len(slices) - 1)):
        edge_index = edge_indices[:, slices[i]:slices[i + 1]]
        # number of nodes
        # num_nodes = int(edge_index.max().item()) + 1
        # edge_index_fa = torch.cartesian_prod(torch.arange(0, num_nodes), torch.arange(0, num_nodes)).T
        edge_index_fosr, edge_type_fosr, _ = edge_rewire(edge_index.numpy(), num_iterations=cfg.fosr.iteration)
        # dataset.data.edge_index = torch.tensor(edge_index)
        # dataset.data.edge_type = torch.tensor(edge_type)
        # print(dataset.data.num_edges)
        # print(len(dataset.data.edge_type))
        # calculate the FA edges
        edge_index_fosr = torch.tensor(edge_index_fosr)
        # dataset.data.edge_type = torch.tensor(edge_type)
        idxs[0].append(edge_index_fosr)
    # for FA only
    k = -20
    ei_k = idxs[0]
    filepath = join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, k))
    if not exists(filepath):
        print('Saving edge indices for k=%d (FA) to %s...' % (k, filepath))
        torch.save(ei_k, filepath)
        # shortest path neighborhoods

def compute_k_hop_edges(dataset, K, filedir, format, name, extra):
    """take regular dataset, save k-hop edges"""
    # we're saving a list of k-hop edge indices
    edge_indices = dataset.data.edge_index
    slices = dataset.slices['edge_index']  # used to slice the graph
    idxs = [[] for _ in range(K)]
    for i in tqdm(range(len(slices) - 1)):
        # for edge_index in [edge_indices]:
        edge_index = edge_indices[:, slices[i]:slices[i + 1]]
        idxs[0].append(edge_index)  # 1-hop
        try:
            tmp = to_dense_adj(edge_index).float()
        except:
            print('Offending tensor:\nedge_index:\n', edge_index, '\nedge_index.shape:', edge_index.shape)
            adj = None  # if it fails, set adj to None to force an errorx
        adj = tmp.to_sparse().float()
        matrices = [tmp]
        for k in range(2, K + 1):
            tmp = torch.bmm(adj, tmp)
            for j in range(tmp.shape[-1]):
                tmp[0, j, j] = 0  # remove self-connections
            tmp = (tmp > 0).float()  # remove edge multiples
            for m in matrices:
                tmp -= m
            tmp = (tmp > 0).float()  # remove -ves, cancelled edges
            idx, _ = dense_to_sparse(tmp)  # outputs int64, which we want
            matrices.append(tmp)
            idxs[k - 1].append(idx)
    for k, ei_k in enumerate(idxs, 1):
        filepath = join(filedir, "%s-%s%s_k=%02d.pt" % (format, name, extra, k))
        if not exists(filepath):
            print('Saving edge indices for k=%d to %s...' % (k, filepath))
            torch.save(ei_k, filepath)
            # shortest path neighborhoods

@jit(nopython=True)
def choose_edge_to_add(x, edge_index, degrees):
	# chooses edge (u, v) to add which minimizes y[u]*y[v]
	n = x.size
	m = edge_index.shape[1]
	y = x / ((degrees + 1) ** 0.5)
	products = np.outer(y, y)
	for i in range(m):
		u = edge_index[0, i]
		v = edge_index[1, i]
		products[u, v] = inf
	for i in range(n):
		products[i, i] = inf
	smallest_product = np.argmin(products)
	return (smallest_product % n, smallest_product // n)

@jit(nopython=True)
def compute_degrees(edge_index, num_nodes=None):
	# returns array of degrees of all nodes
	if num_nodes is None:
		num_nodes = np.max(edge_index) + 1
	degrees = np.zeros(num_nodes)
	m = edge_index.shape[1]
	for i in range(m):
		degrees[edge_index[0, i]] += 1
	return degrees

@jit(nopython=True)
def add_edge(edge_index, u, v):
	new_edge = np.array([[u, v],[v, u]])
	return np.concatenate((edge_index, new_edge), axis=1)

@jit(nopython=True)
def adj_matrix_multiply(edge_index, x):
	# given an edge_index, computes Ax, where A is the corresponding adjacency matrix
	n = x.size
	y = np.zeros(n)
	m = edge_index.shape[1]
	for i in range(m):
		u = edge_index[0, i]
		v = edge_index[1, i]
		y[u] += x[v]
	return y

@jit(nopython=True)
def compute_spectral_gap(edge_index, x):
	m = edge_index.shape[1]
	n = np.max(edge_index) + 1
	degrees = compute_degrees(edge_index, num_nodes=n)
	y = adj_matrix_multiply(edge_index, x / (degrees ** 0.5)) / (degrees ** 0.5)
	for i in range(n):
		if x[i] > 1e-9:
			return 1 - y[i]/x[i]
	return 0.

@jit(nopython=True)
def _edge_rewire(edge_index, edge_type, x=None, num_iterations=50, initial_power_iters=50):
	m = edge_index.shape[1]
	n = np.max(edge_index) + 1
	if x is None:
		x = 2 * np.random.random(n) - 1
	degrees = compute_degrees(edge_index, num_nodes=n)
	for i in range(initial_power_iters):
		x = x - x.dot(degrees ** 0.5) * (degrees ** 0.5)/sum(degrees)
		y = x + adj_matrix_multiply(edge_index, x / (degrees ** 0.5)) / (degrees ** 0.5)
		x = y / np.linalg.norm(y)
	for I in range(num_iterations):
		i, j = choose_edge_to_add(x, edge_index, degrees=degrees)
		edge_index = add_edge(edge_index, i, j)
		degrees[i] += 1
		degrees[j] += 1
		edge_type = np.append(edge_type, 1)
		edge_type = np.append(edge_type, 1)
		x = x - x.dot(degrees ** 0.5) * (degrees ** 0.5)/sum(degrees)
		y = x + adj_matrix_multiply(edge_index, x / (degrees ** 0.5)) / (degrees ** 0.5)
		x = y / np.linalg.norm(y)
	return edge_index, edge_type, x

def edge_rewire(edge_index, x=None, edge_type=None, num_iterations=50, initial_power_iters=5):
	m = edge_index.shape[1]
	n = np.max(edge_index) + 1
	if x is None:
		x = 2 * np.random.random(n) - 1
	if edge_type is None:
		edge_type = np.zeros(m, dtype=np.int64)
	return _edge_rewire(edge_index, edge_type=edge_type, x=x, num_iterations=num_iterations, initial_power_iters=initial_power_iters)