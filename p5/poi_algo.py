# -*- coding: utf-8
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import recall_score, precision_score, make_scorer


class ExtraFeatures(object):
    ALL = (True, True, True, False)
    ALL_TOTALS = (True, True, False, False)
    FINANCE_TOTALS = (True, False, False, False)
    EMAIL_TOTALS = (False, True, False, False)
    EMAIL_RATIOS = (False, False, True, False)
    NONE = (False, False, False, False)
    NO_TOTALS = (False, False, False, True)

    @classmethod
    def all_values(cls):
        return [cls.ALL, cls.ALL_TOTALS, cls.FINANCE_TOTALS, cls.EMAIL_TOTALS,
                cls.EMAIL_RATIOS, cls.NONE, cls.NO_TOTALS]


class Algo(object):
    """Keeps constants to identify machine learning method."""

    LOG_REG = 1
    LINEAR_SVC = 2
    SVC = 3
    K_MEANS = 4
    GAUSSIAN_NB = 5

    @staticmethod
    def all_values():
        return [1, 2, 3, 4, 5]


def k_best_features(features_df, labels_df, k='all'):
    """Run SelectKBest feature selection
    :return: DataFrame with scores
    """
    k_best = SelectKBest(k=k)
    k_best.fit(features_df, labels_df)
    scores = pd.DataFrame(k_best.scores_,
                          index=features_df.columns)
    scores.columns = ['Score']
    scores = scores.sort_values(by=['Score'], ascending=False)
    scores['Rank'] = range(1, len(features_df.count()) + 1)
    return scores[0:k] if k and k != 'all' else scores


def precision_vs_recall_score(actual, predicted):
    """We want both precision and recall to be as high as possible, 0.3 at
    least."""
    pr = precision_score(actual, predicted)
    rc = recall_score(actual, predicted)
    if (pr < 0.3) or (rc < 0.3):
        return min(pr, rc)
    return max(pr, rc)


def create_scorer():
    """Create a custom scorer with both recall and precision."""
    return make_scorer(precision_vs_recall_score, greater_is_better=True)


def create_pipeline(algo, extras=ExtraFeatures.ALL, is_search=False, max_features=20):
    """Create processing pipeline for one of algorithm constants.

    :param algo: int
    :param extras: tuple of additional feature flags
    :param is_search: boolean
    :param max_features: int
    :return: Pipeline
    """
    pipeline, params_best, classifier = None, None, None

    k_range = []
    for x in [10, 12, 17, 20]:
        if x <= max_features:
            k_range += [x]
    k_range += ['all']

    params_search = {
        'selection__k': k_range,
        'classifier__C': [1e-05, 1e-2, 1e-1, 1],
        'classifier__class_weight': ['balanced'],
    }

    if algo == Algo.LOG_REG:
        # Logistic regression
        classifier = LogisticRegression()
        best_k = {
            ExtraFeatures.ALL: ['all'],
            ExtraFeatures.ALL_TOTALS: [20],
            ExtraFeatures.FINANCE_TOTALS: [20],
            ExtraFeatures.EMAIL_TOTALS: [17],
            ExtraFeatures.EMAIL_RATIOS: ['all'],
            ExtraFeatures.NONE: [17],
            ExtraFeatures.NO_TOTALS: [17],
        }
        best_C = {
            ExtraFeatures.ALL: [1e-1],
            ExtraFeatures.ALL_TOTALS: [1e-2],
            ExtraFeatures.FINANCE_TOTALS: [1e-2],
            ExtraFeatures.EMAIL_TOTALS: [1e-1],
            ExtraFeatures.EMAIL_RATIOS: [1e-1],
            ExtraFeatures.NONE: [1e-2],
            ExtraFeatures.NO_TOTALS: [1e-2],
        }
        params_best = {
            'classifier__class_weight': ['balanced'],
            'classifier__C': best_C[extras],
            'selection__k': best_k[extras]
        }
    elif algo == Algo.LINEAR_SVC:
        # Linear SVC
        classifier = LinearSVC()
        best_k = {
            ExtraFeatures.ALL: [20],
            ExtraFeatures.ALL_TOTALS: [17],
            ExtraFeatures.FINANCE_TOTALS: [20],
            ExtraFeatures.EMAIL_TOTALS: ['all'],
            ExtraFeatures.EMAIL_RATIOS: [20],
            ExtraFeatures.NONE: [17],
            ExtraFeatures.NO_TOTALS: [12],
        }
        best_C = {
            ExtraFeatures.ALL: [1e-1],
            ExtraFeatures.ALL_TOTALS: [1e-5],
            ExtraFeatures.FINANCE_TOTALS: [1e-05],
            ExtraFeatures.EMAIL_TOTALS: [1e-2],
            ExtraFeatures.EMAIL_RATIOS: [1e-1],
            ExtraFeatures.NONE: [1e-05],
            ExtraFeatures.NO_TOTALS: [1e-05],
        }
        params_best = {
            'classifier__class_weight': ['balanced'],
            'classifier__C': best_C[extras],
            'selection__k': best_k[extras]
        }
    elif algo == Algo.SVC:
        # SVC with rbf kernel
        classifier = SVC()
        best_k = {
            ExtraFeatures.ALL: ['all'],
            ExtraFeatures.ALL_TOTALS: [20],
            ExtraFeatures.FINANCE_TOTALS: [17],
            ExtraFeatures.EMAIL_TOTALS: ['all'],
            ExtraFeatures.EMAIL_RATIOS: ['all'],
            ExtraFeatures.NONE: [17],
            ExtraFeatures.NO_TOTALS: [12],
        }
        params_best = {
            'classifier__class_weight': ['balanced'],
            'classifier__C': [1],
            'selection__k': best_k[extras]
        }
    elif algo == Algo.K_MEANS:
        # K-Means clustering
        best_k = {
            ExtraFeatures.ALL: ['all'],
            ExtraFeatures.ALL_TOTALS: [20],
            ExtraFeatures.FINANCE_TOTALS: ['all'],
            ExtraFeatures.EMAIL_TOTALS: [17],
            ExtraFeatures.EMAIL_RATIOS: ['all'],
            ExtraFeatures.NONE: [17],
            ExtraFeatures.NO_TOTALS: [12],
        }
        best_tol = {
            ExtraFeatures.ALL: [1e-1],
            ExtraFeatures.ALL_TOTALS: [1e-16],
            ExtraFeatures.FINANCE_TOTALS: [1e-08],
            ExtraFeatures.EMAIL_TOTALS: [1e-16],
            ExtraFeatures.EMAIL_RATIOS: [1e-1],
            ExtraFeatures.NONE: [1e-16],
            ExtraFeatures.NO_TOTALS: [1e-1],
        }
        classifier = KMeans(n_clusters=2)
        params_search = {
            'selection__k': k_range,
            'classifier__n_clusters': [2],
            'classifier__tol': [1e-16, 1e-8, 1e-4, 1e-2, 1e-1],
        }
        params_best = {
            'selection__k': best_k[extras],
            'classifier__n_clusters': [2],
            'classifier__tol': best_tol[extras],
        }
    elif algo == Algo.GAUSSIAN_NB:
        classifier = GaussianNB()
        params_search = {}
        params_best = {}

    pipeline = Pipeline(steps=[('minmaxer', MinMaxScaler()),
                               ('selection', SelectKBest()),
                               ('classifier', classifier)])

    params = params_search if is_search else params_best

    return pipeline, params
