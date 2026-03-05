from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_fosr(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.fosr = CN()

    # then argument can be specified within the group
    cfg.fosr.use = False
    cfg.fosr.iteration = 100


register_config('fosr', set_cfg_fosr)
