import logging
import time

import numpy as np
import torch
from scipy.stats import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, \
    f1_score, roc_auc_score
from torch_geometric.graphgym import get_current_gpu_usage
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.logger import infer_task, Logger
from torch_geometric.graphgym.utils.io import dict_to_json, dict_to_tb
from torchmetrics.functional import auroc




class CustomLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Whether to run comparison tests of alternative score implementations.
        self.test_scores = False

    # basic properties
    def basic(self):
        stats = {
            'loss': round(self._loss / self._size_current, max(8, cfg.round)),
            'lr': round(self._lr, max(8, cfg.round)),
            'params': self._params,
            'time_iter': round(self.time_iter(), cfg.round),
        }
        gpu_memory = get_current_gpu_usage()
        if gpu_memory > 0:
            stats['gpu_memory'] = gpu_memory
        return stats

    # task properties
    def classification_binary(self):
        true = torch.cat(self._true).squeeze(-1)
        pred_score = torch.cat(self._pred)
        pred_int = self._get_pred_int(pred_score)

        if true.shape[0] < 1e7:  # AUROC computation for very large datasets is too slow.
            # TorchMetrics AUROC on GPU if available.
            auroc_score = auroc(pred_score.to(torch.device(cfg.device)),
                                true.to(torch.device(cfg.device)),
                                pos_label=1)
            if self.test_scores:
                # SK-learn version.
                try:
                    r_a_score = roc_auc_score(true.cpu().numpy(),
                                              pred_score.cpu().numpy())
                except ValueError:
                    r_a_score = 0.0
                assert np.isclose(float(auroc_score), r_a_score)
        else:
            auroc_score = 0.

        reformat = lambda x: round(float(x), cfg.round)
        return {
            'accuracy': reformat(accuracy_score(true, pred_int)),
            'precision': reformat(precision_score(true, pred_int)),
            'recall': reformat(recall_score(true, pred_int)),
            'f1': reformat(f1_score(true, pred_int)),
            'auc': reformat(auroc_score),
        }

    def classification_multi(self):
        true, pred_score = torch.cat(self._true), torch.cat(self._pred)
        pred_int = self._get_pred_int(pred_score)
        reformat = lambda x: round(float(x), cfg.round)
        res = {
            'accuracy': reformat(accuracy_score(true, pred_int)),
            'f1': reformat(f1_score(true, pred_int,
                                    average='macro', zero_division=0)),
        }
        if true.shape[0] < 1e7:
            # AUROC computation for very large datasets runs out of memory.
            # TorchMetrics AUROC on GPU is much faster than sklearn for large ds
            res['auc'] = reformat(auroc(pred_score.to(torch.device(cfg.device)),
                                        true.to(torch.device(cfg.device)).squeeze(),
                                        num_classes=pred_score.shape[1],
                                        average='macro'))

            if self.test_scores:
                # SK-learn version.
                sk_auc = reformat(roc_auc_score(true, pred_score.exp(),
                                                average='macro',
                                                multi_class='ovr'))
                assert np.isclose(sk_auc, res['auc'])

        return res

    def update_stats(self, true, pred, loss, lr, time_used, params,
                     dataset_name=None, **kwargs):
        assert true.shape[0] == pred.shape[0]
        batch_size = true.shape[0]
        self._iter += 1
        self._true.append(true)
        self._pred.append(pred)
        self._size_current += batch_size
        self._loss += loss * batch_size
        self._lr = lr
        self._params = params
        self._time_used += time_used
        self._time_total += time_used
        for key, val in kwargs.items():
            if key not in self._custom_stats:
                self._custom_stats[key] = val * batch_size
            else:
                self._custom_stats[key] += val * batch_size

    def write_epoch(self, cur_epoch):
        start_time = time.perf_counter()
        basic_stats = self.basic()

        if self.task_type == 'classification_binary':
            task_stats = self.classification_binary()
        elif self.task_type == 'classification_multi':
            task_stats = self.classification_multi()
        else:
            raise ValueError('Task has to be regression or classification')
        
        epoch_stats = {'epoch': cur_epoch,
                       'time_epoch': round(self._time_used, cfg.round)}
        eta_stats = {'eta': round(self.eta(cur_epoch), cfg.round),
                     'eta_hours': round(self.eta(cur_epoch) / 3600, cfg.round)}
        custom_stats = self.custom()

        if self.name == 'train':
            stats = {
                **epoch_stats,
                **eta_stats,
                **basic_stats,
                **task_stats,
                **custom_stats
            }
        else:
            stats = {
                **epoch_stats,
                **basic_stats,
                **task_stats,
                **custom_stats
            }

        # print
        logging.info('{}: {}'.format(self.name, stats))
        # json
        dict_to_json(stats, '{}/stats.json'.format(self.out_dir))
        # tensorboard
        if cfg.tensorboard_each_run:
            dict_to_tb(stats, self.tb_writer, cur_epoch)
        self.reset()
        if cur_epoch < 3:
            logging.info(f"...computing epoch stats took: "
                         f"{time.perf_counter() - start_time:.2f}s")
        return stats


def create_logger():
    """
    Create logger for the experiment

    Returns: List of logger objects

    """
    loggers = []
    names = ['train', 'val', 'test']
    for i, dataset in enumerate(range(cfg.share.num_splits)):
        loggers.append(CustomLogger(name=names[i], task_type=infer_task()))
    return loggers


def eval_spearmanr(y_true, y_pred):
    """Compute Spearman Rho averaged across tasks.
    """
    res_list = []

    if y_true.ndim == 1:
        res_list.append(stats.spearmanr(y_true, y_pred)[0])
    else:
        for i in range(y_true.shape[1]):
            # ignore nan values
            is_labeled = ~np.isnan(y_true[:, i])
            res_list.append(stats.spearmanr(y_true[is_labeled, i],
                                            y_pred[is_labeled, i])[0])

    return {'spearmanr': sum(res_list) / len(res_list)}
