# -*- coding: utf-8
import os
import sys
import pandas as pd
from poi_algo import Algo, ExtraFeatures


def retrieve_all_metrics_df(root_dir=None):
    """Create dataframe with all metrics.
    :return: pd.DataFrame"""
    all_metrics = []
    for extras in ExtraFeatures.all_values():
        for algo in Algo.all_values():
            all_metrics.append(retrieve_metrics(extras, algo, root_dir))
    df = pd.DataFrame(all_metrics)
    df.columns = ['Subset', 'Classifier', 'Accuracy', 'Precision', 'Recall',
                  'F1', 'F2']
    return df


def retrieve_metrics(extras, algo, root_dir=None):
    """Read metrics from log file.
    :param extras: tuple
    :param algo: int
    :param root_dir: string
    :return: tuple of (accuracy, precision, recall, f1, f2)"""
    subname = subset_name(extras)
    algoname = algo_name(algo)
    logdir, logname = log_file_name(extras, algo, root_dir)
    if os.path.exists(logname):
        with open(logname, 'r') as f:
            for line in f:
                if 'Precision:' in line:
                    line = line.strip()
                    line = line.split('\t')
                    line = [float(x.split(':')[1].strip()) for x in line]
                    return tuple([subname, algoname] + line)
    return (subname, algoname, None, None, None, None, None)


def subset_name(extras):
    subdir = {
        ExtraFeatures.ALL: 'all',
        ExtraFeatures.ALL_TOTALS: 'all-totals',
        ExtraFeatures.FINANCE_TOTALS: 'finance-totals',
        ExtraFeatures.EMAIL_TOTALS: 'email-totals',
        ExtraFeatures.EMAIL_RATIOS: 'email-ratios',
        ExtraFeatures.NONE: 'none',
        ExtraFeatures.NO_TOTALS: 'no-totals',
    }
    return subdir[extras]


def algo_name(algo):
    name = {
        Algo.LOG_REG: 'logreg',
        Algo.LINEAR_SVC: 'linsvc',
        Algo.SVC: 'svc',
        Algo.K_MEANS: 'kmeans',
        Algo.GAUSSIAN_NB: 'gaussiannb'
    }
    return name[algo]


def log_file_name(extras, algo, root_dir=None):
    """Get log file name.
    :return: tuple with (dir_name, full_file_path)
    """
    root_dir = './output' if root_dir is None else root_dir
    subname = subset_name(extras)
    algoname = algo_name(algo)
    logdir = os.path.join(root_dir, subname)
    logname = os.path.join(root_dir, subname, algoname + '.log')
    return logdir, logname


def init_logfile(extras, algo):
    """Create log file at ./output/{subname}/{algoname}.log."""
    logdir, logname = log_file_name(extras, algo)
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    elif os.path.exists(logname):
        os.unlink(logname)
    orig_stdout = sys.stdout
    current_file = open(logname, 'a')
    sys.stdout = current_file
    return orig_stdout, current_file


def close_logfile(orig_stdout, current_file):
    sys.stdout = orig_stdout
    current_file.close()
