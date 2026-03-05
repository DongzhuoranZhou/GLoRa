from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config

def set_cfg_pairnorm(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.pairnorm = CN()

    # then argument can be specified within the group
    cfg.pairnorm.use = False
    cfg.pairnorm.scale = 1
    cfg.pairnorm.scale_individually = False
    cfg.pairnorm.eps = 1e-5


register_config('pairnorm', set_cfg_pairnorm)