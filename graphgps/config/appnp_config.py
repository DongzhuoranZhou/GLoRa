from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_appnp(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.appnp = CN()

    # then argument can be specified within the group
    cfg.appnp.K = 10
    cfg.appnp.alpha = 0.1


register_config('appnp', set_cfg_appnp)
