import torch
import time
import logging
import os
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.loss import compute_loss
from torch_geometric.graphgym.utils.epoch import is_eval_epoch, is_ckpt_epoch
from torch_geometric.graphgym.checkpoint import load_ckpt, save_ckpt, \
    clean_ckpt
from torch_geometric.graphgym.register import register_train
def get_best_model_dir():
    return '{}/val/ckpt'.format(cfg.run_dir)


def save_best_model(model, optimizer, scheduler, epoch):
    r'''
    Save model checkpoint at given epoch

    Args:
        model (torch.nn.Module): The model that will be saved
        optimizer (torch.optim): The optimizer that will be saved
        scheduler (torch.optim): The schduler that will be saved
        epoch (int): The epoch when the model is saved

    '''
    ckpt = {
        'epoch': epoch,
        'model_state': model.state_dict(),
        'optimizer_state': optimizer.state_dict(),
        'scheduler_state': scheduler.state_dict()
    }
    os.makedirs(get_best_model_dir(), exist_ok=True)
    ckpt_name = '{}/{}.ckpt'.format(get_best_model_dir(), epoch)
    torch.save(ckpt, ckpt_name)
    logging.info('Check point saved: {}'.format(ckpt_name))


def get_all_epoch():
    d = get_best_model_dir()
    names = os.listdir(d) if os.path.exists(d) else []
    if len(names) == 0:
        return [0]
    epochs = [int(name.split('.')[0]) for name in names]
    return epochs


def get_last_epoch():
    return max(get_all_epoch())


def clean_redudant_best_model():
    r'''

    Only keep the latest model checkpoint, remove all the older checkpoints

    '''
    epochs = get_all_epoch()
    epoch_last = max(epochs)
    for epoch in epochs:
        if epoch != epoch_last:
            ckpt_name = '{}/{}.ckpt'.format(get_best_model_dir(), epoch)
            os.remove(ckpt_name)


def train_epoch(logger, loader, model, optimizer, scheduler, layers_grads=None):
    model.train()
    time_start = time.time()
    for batch in loader:
        batch.split = 'train'
        batch.layer_grads = layers_grads
        optimizer.zero_grad()
        batch.to(torch.device(cfg.device))
        pred, true = model(batch)
        loss, pred_score = compute_loss(pred, true)
        loss.backward()
        optimizer.step()
        logger.update_stats(true=true.detach().cpu(),
                            pred=pred_score.detach().cpu(), loss=loss.item(),
                            lr=scheduler.get_last_lr()[0],
                            time_used=time.time() - time_start,
                            params=cfg.params)
        time_start = time.time()
    scheduler.step()


@torch.no_grad()
def eval_epoch(logger, loader, model, split='val', layers_grads=None):
    model.eval()
    time_start = time.time()
    for batch in loader:
        batch.split = split
        batch.layer_grads = layers_grads
        batch.to(torch.device(cfg.device))
        pred, true = model(batch)
        loss, pred_score = compute_loss(pred, true)
        logger.update_stats(true=true.detach().cpu(),
                            pred=pred_score.detach().cpu(), loss=loss.item(),
                            lr=0, time_used=time.time() - time_start,
                            params=cfg.params)
        time_start = time.time()


def train(loggers, loaders, model, optimizer, scheduler):
    """
    The core training pipeline

    Args:
        loggers: List of loggers
        loaders: List of loaders
        model: GNN model
        optimizer: PyTorch optimizer
        scheduler: PyTorch learning rate scheduler

    """
    start_epoch = 0
    if cfg.train.auto_resume:
        start_epoch = load_ckpt(model, optimizer, scheduler)
    if start_epoch == cfg.optim.max_epoch:
        logging.info('Checkpoint found, Task already done')
    else:
        logging.info('Start from epoch {}'.format(start_epoch))

    num_splits = len(loggers)
    split_names = ['val', 'test']
    best_val_loss = float('inf')  # Initialize with a large value
    layer_grads = {}

    for cur_epoch in range(start_epoch, cfg.optim.max_epoch):
        train_epoch(loggers[0], loaders[0], model, optimizer, scheduler, layer_grads)
        stats = loggers[0].write_epoch(cur_epoch)
        if is_eval_epoch(cur_epoch):
            for i in range(1, num_splits):
                eval_epoch(loggers[i], loaders[i], model,
                           split=split_names[i - 1], layers_grads=layer_grads)
                # debug
                stats_val = loggers[i].write_epoch(cur_epoch)
                # Check if the current validation loss is the best so far
                if split_names[i - 1] == 'val':
                    current_val_loss = stats_val['loss']
                    if current_val_loss < best_val_loss:
                        best_val_loss = current_val_loss
                        best_epoch = cur_epoch
                        # Save the model with the best validation performance
                        save_best_model(model, optimizer, scheduler, best_epoch)
                        logging.info('Best model saved at epoch {} base on val loss'.format(
                            best_epoch))
        if is_ckpt_epoch(cur_epoch):
            save_ckpt(model, optimizer, scheduler, cur_epoch)
    for logger in loggers:
        logger.close()
    if cfg.train.ckpt_clean:
        clean_ckpt()
        clean_redudant_best_model()

    logging.info('Task done, results saved in {}'.format(cfg.run_dir))

class EarlyStopping:
    def __init__(self, patience=5, min_delta=0.001):
        """
        Args:
            patience (int): How many epochs to wait after last time the monitored metric improved.
            min_delta (float): Minimum change to qualify as an improvement.
        """
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = None
        self.counter = 0
        self.early_stop = False

    def __call__(self, val_loss,epoch=0):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0  # Reset the counter if the loss improves
        else:
            self.counter += 1  # Increment the counter if no improvement
            if self.counter >= self.patience:
                self.early_stop = True  # Trigger early stop
                logging.info(f'Early stopping at epoch {epoch} with val loss {val_loss}')

def train_early_stop_flex_metric(loggers, loaders, model, optimizer, scheduler):
    """
    The core training pipeline

    Args:
        loggers: List of loggers
        loaders: List of loaders
        model: GNN model
        optimizer: PyTorch optimizer
        scheduler: PyTorch learning rate scheduler

    """
    start_epoch = 0
    if cfg.train.auto_resume:
        start_epoch = load_ckpt(model, optimizer, scheduler)
    if start_epoch == cfg.optim.max_epoch:
        logging.info('Checkpoint found, Task already done')
    else:
        logging.info('Start from epoch {}'.format(start_epoch))

    num_splits = len(loggers)
    split_names = ['val', 'test']
    best_val_loss = float('inf')  # Initialize with a large value
    # Initialize best_val_metric based on cfg.metric_agg
    best_val_metric = -float('inf') if cfg.metric_agg == 'argmax' else float('inf')
    layer_grads = {}
    early_stopping = EarlyStopping(patience=cfg.patience, min_delta=cfg.min_delta)  # Create early stopping object

    for cur_epoch in range(start_epoch, cfg.optim.max_epoch):
        train_epoch(loggers[0], loaders[0], model, optimizer, scheduler, layer_grads)
        stats = loggers[0].write_epoch(cur_epoch)
        if is_eval_epoch(cur_epoch):
            for i in range(1, num_splits):
                eval_epoch(loggers[i], loaders[i], model,
                           split=split_names[i - 1], layers_grads=layer_grads)
                stats = loggers[i].write_epoch(cur_epoch)
                # Check if the current validation loss is the best so far
                if split_names[i - 1] == 'val':
                    if cfg.metric_best == 'auto':
                        metric = 'auc' if 'auc' in stats else 'accuracy'  # Automatically choose 'auc' or 'accuracy'
                    else:
                        metric = cfg.metric_best  # Use the specified metric from config

                    current_val_metric = stats[metric]
                    best_metric = best_val_loss if metric == 'loss' else best_val_metric  # Initialize best metric (use best_val_loss for 'loss')

                    # Log the comparison of best_metric and current_val_metric
                    logging.info(f"Current {metric} at epoch {cur_epoch}: {current_val_metric}, "
                                 f"Best {metric} so far: {best_metric}")
                    if (cfg.metric_agg == 'argmin' and current_val_metric < best_val_metric) or \
                            (cfg.metric_agg == 'argmax' and current_val_metric > best_val_metric):
                        logging.info(f'Best {metric} updated from {best_val_metric} to {current_val_metric}')
                        best_val_metric = current_val_metric  # Update best_val_metric with the current best

                        best_epoch = cur_epoch

                        # Save the model with the best validation performance
                        save_best_model(model, optimizer, scheduler, best_epoch)
                        logging.info(f'Best model saved at epoch {best_epoch} based on {metric}')
                    # Check for early stopping
                    current_val_loss = stats['loss']
                    early_stopping(current_val_loss, cur_epoch)
                    if early_stopping.early_stop:
                        logging.info(f"Early stopping at epoch {cur_epoch}")
                        # update the test result
                        eval_epoch(loggers[i+1], loaders[i+1], model,
                                   split=split_names[i], layers_grads=layer_grads)
                        loggers[i+1].write_epoch(cur_epoch)
                        if is_ckpt_epoch(cur_epoch):
                            save_ckpt(model, optimizer, scheduler, cur_epoch)
                        for logger in loggers:
                            logger.close()  # Close loggers properly
                        if cfg.train.ckpt_clean:
                            clean_ckpt()
                            clean_redudant_best_model()
                        return
        if is_ckpt_epoch(cur_epoch):
            save_ckpt(model, optimizer, scheduler, cur_epoch)
    for logger in loggers:
        logger.close()
    if cfg.train.ckpt_clean:
        clean_ckpt()
        clean_redudant_best_model()

    logging.info('Task done, results saved in {}'.format(cfg.run_dir))
register_train("train_early_stop_flex_metric", train_early_stop_flex_metric)


