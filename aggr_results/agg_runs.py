import argparse
import logging
import numpy as np
import os.path
import sys
from torch_geometric.graphgym.utils.io import dict_list_to_tb

sys.path.append(".")
sys.path.append("..")
try:
    from tensorboardX import SummaryWriter
except ImportError:
    SummaryWriter = None
from torch_geometric.graphgym.config import cfg, set_cfg, assert_cfg
from torch_geometric.graphgym.utils.agg_runs import is_seed, is_split, \
    agg_dict_list
from torch_geometric.graphgym.utils.io import dict_list_to_json, \
    json_to_dict_list, makedirs_rm_exist, dict_to_json

from graphgps.finetuning import set_new_cfg_allowed


def parse_args():
    """Parses the arguments."""
    parser = argparse.ArgumentParser(
        description='Train a classification model')
    parser.add_argument('--dir', dest='dir',
                        help='Dir with multiple seed results',
                        required=True, type=str)
    parser.add_argument('--metric', dest='metric',
                        help='metric to select best epoch', required=False,
                        type=str, default='auto')

    return parser.parse_args()


def join_list(l1, l2):
    if len(l1) > len(l2):
        print(f'>> W: Padding the second list (len={len(l2)}) with the last '
              f'item to match len={len(l1)} of the first list.')
        while len(l1) > len(l2):
            l2.append(l2[-1])
    if len(l1) < len(l2):
        print(f'>> W: Padding the first list (len={len(l1)}) with the last '
              f'item to match len={len(l2)} of the second list.')
        while len(l1) < len(l2):
            l1.append(l1[-1])
    assert len(l1) == len(l2), \
        'Results with different seeds must have the save format'
    for i in range(len(l1)):
        l1[i] += l2[i]
    return l1


def agg_runs(dir, metric_best='auto'):
    r'''
    Aggregate over different random seeds of a single experiment.

    NOTE: This is an unchanged copy from GraphGym, only `join_list` function
    had to be modified to pad list to process incomplete runs.

    Args:
        dir (str): Directory of the results, containing 1 experiment
        metric_best (str, optional): The metric for selecting the best
        validation performance. Options: auto, accuracy, auc.

    '''
    results = {'train': None, 'val': None, 'test': None}
    results_best = {'train': None, 'val': None, 'test': None}
    for seed in os.listdir(dir):
        if is_seed(seed):
            dir_seed = os.path.join(dir, seed)
            # find the best epoch for each seed with the given metric
            split = 'val'  # test
            if split in os.listdir(dir_seed):
                dir_split = os.path.join(dir_seed, split)
                fname_stats = os.path.join(dir_split, 'stats.json')
                stats_list = json_to_dict_list(fname_stats)
                if metric_best == 'auto':
                    metric = 'auc' if 'auc' in stats_list[0] else 'accuracy'
                else:
                    metric = metric_best
                performance_np = np.array(  # noqa
                    [stats[metric] for stats in stats_list])
                # Determine best epoch based on the metric type
                # if metric == 'loss':
                #     best_epoch = stats_list[performance_np.argmin()]['epoch']  # Find epoch with minimum loss
                # else:
                #     best_epoch = stats_list[performance_np.argmax()]['epoch']  # Find epoch with maximum accuracy/auc
                # #
                best_epoch = \
                    stats_list[
                        eval("performance_np.{}()".format(cfg.metric_agg))][
                        'epoch']
                logging.info(f'>> Best epoch for seed {seed} is {best_epoch} in split {split} with metric {metric}.')
            # aggregate the results: train, val, test for each seed
            for split in os.listdir(dir_seed):
                if is_split(split):
                    dir_split = os.path.join(dir_seed, split)
                    fname_stats = os.path.join(dir_split, 'stats.json')
                    stats_list = json_to_dict_list(fname_stats)
                    try:
                        stats_best = [
                            stats for stats in stats_list
                            if stats['epoch'] == best_epoch
                        ][0]
                    except:
                        pass
                    # print(stats_best)
                    logging.info(f'>> --- Best stats for seed {seed} in split {split} is \n {stats_best}.')

                    stats_list = [[stats] for stats in stats_list]
                    if results[split] is None:
                        results[split] = stats_list
                    else:
                        results[split] = join_list(results[split], stats_list)
                    if results_best[split] is None:
                        results_best[split] = [stats_best]
                    else:
                        results_best[split] += [stats_best]
    results = {k: v for k, v in results.items() if v is not None}  # rm None
    results_best = {k: v
                    for k, v in results_best.items()
                    if v is not None}  # rm None
    for key in results:
        for i in range(len(results[key])):
            results[key][i] = agg_dict_list(results[key][i])
    for key in results_best:
        results_best[key] = agg_dict_list(
            results_best[key])  # here it just save the epoch of the first dict as the output epoch. strange.

    # save aggregated results
    for key, value in results.items():
        dir_out = os.path.join(dir, 'agg', key)
        makedirs_rm_exist(dir_out)
        fname = os.path.join(dir_out, 'stats.json')
        dict_list_to_json(value, fname)

        if cfg.tensorboard_agg:
            if SummaryWriter is None:
                raise ImportError(
                    'Tensorboard support requires `tensorboardX`.')
            writer = SummaryWriter(dir_out)
            dict_list_to_tb(value, writer)
            writer.close()

    for key, value in results_best.items():
        dir_out = os.path.join(dir, 'agg', key)
        fname = os.path.join(dir_out, 'best.json')
        dict_to_json(value, fname)
        logging.info('Best results saved in {}'.format(fname))
    logging.info('Results aggregated across runs saved in {}'.format(
        os.path.join(dir, 'agg')))


if __name__ == '__main__':

    # best result is based on auc
    args = parse_args()

    set_cfg(cfg)
    set_new_cfg_allowed(cfg, True)
    cfg.merge_from_file(os.path.join(args.dir, 'config.yaml'))
    assert_cfg(cfg)

    if args.metric == 'auto':
        args.metric = cfg.metric_best  # auto/accuracy
    print(f'metric:   {args.metric}')
    print(f'agg_type: {cfg.metric_agg}')

    # Aggregate results from different seeds
    agg_runs(args.dir, args.metric)
