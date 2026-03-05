from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_gprgnn(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    https://github.com/jianhao2016/GPRGNN/blob/4e0a7ee5435058b70eaec3c23c55fb96dc37f2d5/src/train_model.py
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.gprgnn = CN()

    # then argument can be specified within the group
    cfg.gprgnn.K = 10
    cfg.gprgnn.alpha = 0.1
    cfg.gprgnn.ppnp = 'GPR_prop'  # choices=['PPNP', 'GPR_prop']
    cfg.gprgnn.Gamma = None
    cfg.gprgnn.Init = 'PPR' # choices=['SGC', 'PPR', 'NPPR', 'Random', 'WS', 'Null']
    cfg.gprgnn.hidden = 64
    cfg.gprgnn.dropout = 0.5
    cfg.gprgnn.dprate = 0.5


register_config('gprgnn', set_cfg_gprgnn)
