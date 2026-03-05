# parameter calculators
from torch_geometric.graphgym.config import cfg

sort_and_removes_dupes = lambda mylist: sorted(list(dict.fromkeys(mylist)))


def set_d_fixed_params(cfg):
    # N = cfg.fixed_params.N
    if cfg.dataset.name == "GLoRa":
        if cfg.gnn.stage_type == 'drew_gnn':  # (L^2+L)/2 scaling for DRew
            n_layers, d = cfg.gnn.layers_mp, cfg.gnn.dim_inner
            cfg.gnn.dim_inner = round(
                (2 * (d ** 2) / (n_layers + 1)) ** 0.5)  # sets param count to roughly the same for fixed L
        print('Using d = %d' % cfg.gnn.dim_inner)
    else:
        print('Using given hidden dim of %d' % cfg.gnn.dim_inner)


def get_k_neighbourhoods(t):
    sp_nbhs = list(range(1, min(t + 1, cfg.k_max) + 1))
    return sort_and_removes_dupes(sp_nbhs)


def get_num_fc_drew(L):
    """Base number of FC layers in DRew MP"""
    num_fc = 0
    assert cfg.k_max >= 0, 'Error: k_max < 0'
    for t in range(L):
        k_nbhs = get_k_neighbourhoods(t)
        toprint = ' '.join([str(i).ljust(2) if i in k_nbhs else 'X'.ljust(2) for i in range(1, k_nbhs[-1] + 1)])
        print('\t%02d: %s' % (t, toprint))
        num_fc += len(k_nbhs)
    return num_fc



def solve_quadratic(a, b, c):
    # Solve the quadratic equation ax**2 + bx + c = 0
    d = (b ** 2) - (4 * a * c)
    # find two solutions
    sol1 = (-b - d ** .5) / (2 * a)
    sol2 = (-b + d ** .5) / (2 * a)
    if sol1 > 0 and sol2 < 0:
        return sol1
    else:
        return sol2
