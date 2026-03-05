import torch
import numpy as np
import os
from tqdm import tqdm

if os.environ.get("DEVICE", "cpu") == "cuda":
    from gdl.curvature.cuda import sdrf
else:
    from gdl.curvature.numba import sdrf
from gdl.data.base import BaseDataset
from torch_geometric.graphgym.config import cfg

class SDRFDataset(BaseDataset):
    """
    Dataset preprocessed with SDRF (Cuda version).
    """

    def __init__(
            self,
            name: str = "Cora",
            use_lcc: bool = True,
            max_steps: int = None,
            remove_edges: bool = True,
            removal_bound: float = 0.5,
            tau: float = 1,
            undirected: bool = False,
            data_dir: str = None,
    ):
        self.name = name
        self.use_lcc = use_lcc
        self.max_steps = int(max_steps)
        self.remove_edges = remove_edges
        self.removal_bound = removal_bound
        self.tau = tau
        self.undirected = undirected
        super(SDRFDataset, self).init(data_dir)
    def init(self, data_dir):
        self.data_dir = data_dir

        super(BaseDataset, self).__init__(self.data_dir)
        self.data, self.slices = torch.load(self.processed_paths[0])
    def process(self):
        filepath = self.processed_paths[0]
        filepath = filepath[filepath.rfind('/') + 1:]
        filepath = filepath.replace('Cora', 'peptides')
        filepath = os.path.join('/Users/beng/Downloads', filepath)
        if os.path.exists(filepath):
            print('Loading file from %s...' % filepath)
            return torch.load(filepath)
        else:
            dataset = torch.load('/Users/beng/Downloads/peptides.pt')
            data_list = list()
            for i in tqdm(range(len(dataset))):
                base = dataset[i]  # already Data object
                altered_data = sdrf(
                    base,  # .data
                    loops=self.max_steps,
                    remove_edges=self.remove_edges,
                    tau=self.tau,
                    is_undirected=self.undirected,
                )
                edge_index = altered_data.edge_index
                data, slices = self.to_dataset(base, edge_index,
                                               None)  # edited to take Data object rather than Dataset object
                dataset._data_list[i] = data
            print('Saving file to %s...' % filepath)
            torch.save((data, slices),filepath)
            return dataset

    def __str__(self) -> str:
        return (
                f"{self.name}_sdrf_ms={self.max_steps}_re={self.remove_edges}_rb={self.removal_bound}_tau={self.tau}_lcc={self.use_lcc}"
                + ("_undirected" if self.undirected else "")
        )


class SDRFDataset_synthetic(BaseDataset):
    """
    Dataset preprocessed with SDRF (Cuda version).
    """

    def __init__(
            self,
            name: str = "Cora",
            use_lcc: bool = True,
            max_steps: int = None,
            remove_edges: bool = True,
            removal_bound: float = 0.5,
            tau: float = 1,
            undirected: bool = False,
            data_dir: str = None,
            dataset=None,
    ):
        self.name = name
        self.dataset_original = dataset
        self.use_lcc = use_lcc
        self.max_steps = int(max_steps)
        self.remove_edges = remove_edges
        self.removal_bound = removal_bound
        self.tau = tau
        self.undirected = undirected

        super(SDRFDataset_synthetic, self).init(data_dir)

    def process(self):
        filepath = self.processed_paths[0]
        if os.path.exists(filepath):
            print('Loading file from %s...' % filepath)
            return torch.load(filepath)
        else:
            dataset = self.dataset_original
            for i in tqdm(range(len(dataset))):
                base = dataset[i]  # already Data object
                base_mask = base.mask
                altered_data = sdrf(
                    base,
                    loops=self.max_steps,
                    remove_edges=self.remove_edges,
                    tau=self.tau,
                    is_undirected=self.undirected,
                )
                edge_index = altered_data.edge_index
                data, slices = self.to_dataset(base, edge_index, # has lose the mask
                                               None)  # edited to take Data object rather than Dataset object
                data.mask = base_mask
                dataset._data_list[i] = data # dataset has train_mask
                # data_list.append(data)
            # self.data, self.slices = self.collate(data_list)
            print('Saving file to %s...' % filepath)
            torch.save((dataset.data, dataset.slices), filepath)
            return (dataset.data, dataset.slices)

    def __str__(self) -> str:
        return (
                f"{self.name}_sdrf_ms={self.max_steps}_re={self.remove_edges}_rb={self.removal_bound}_tau={self.tau}_lcc={self.use_lcc}"
                + ("_undirected" if self.undirected else "")
        )
