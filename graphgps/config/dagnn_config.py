from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_dagnn(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    https://github.com/jianhao2016/GPRGNN/blob/4e0a7ee5435058b70eaec3c23c55fb96dc37f2d5/src/train_model.py
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.dagnn = CN()

    # then argument can be specified within the group

register_config('dagnn', set_cfg_dagnn)
