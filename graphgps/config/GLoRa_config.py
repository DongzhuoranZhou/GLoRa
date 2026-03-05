from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_GLoRa(cfg):
    r'''
    Hyperparameters for GLoRa dataset (used when dataset.format is synthetic and dataset.name is glora)
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    cfg.GLoRa = CN()
    cfg.GLoRa.num_nodes = 10
    cfg.GLoRa.num_graphs = 2000
    cfg.GLoRa.num_classes = 2
    cfg.GLoRa.adapt = None
    cfg.GLoRa.type = 'dag'
    cfg.GLoRa.depth = 10
    cfg.GLoRa.arity = 1
    cfg.GLoRa.direction = True
    cfg.GLoRa.fix = False
    cfg.GLoRa.pure_fix = False
    cfg.GLoRa.R_random = True
    cfg.GLoRa.save = True
    cfg.GLoRa.save_path = './datasets/GLoRa'
    cfg.GLoRa.load = False
    cfg.GLoRa.load_path = './datasets/GLoRa'
    cfg.GLoRa.dataset_seed = 0
    cfg.GLoRa.random_hole_ratio = 1 / 3
    cfg.GLoRa.mix = False
    cfg.GLoRa.mix_save = False
    cfg.GLoRa.save_dataset_log = True
    cfg.GLoRa.save_dataset_log_path = './datasets_Log/GLoRa'
    cfg.GLoRa.m = 0
    cfg.GLoRa.add_two_ends_nodes = False
    cfg.GLoRa.add_in_out_paths = False
    cfg.GLoRa.add_multiple_ends_nodes = False
    cfg.GLoRa.add_nodes_to_source_only = False
    cfg.GLoRa.add_nodes_to_target_only = False
    cfg.GLoRa.add_source_end_node_only= False
    cfg.GLoRa.add_target_end_node_only= False
    cfg.GLoRa.use_vn = False
    cfg.GLoRa.use_k_longest_path_vn = False



register_config('GLoRa', set_cfg_GLoRa)
