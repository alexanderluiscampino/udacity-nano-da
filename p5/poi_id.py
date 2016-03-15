#!/usr/bin/python
"""
POI identifier script.

Usage:
  poi_id.py [-s|--search]

-s, --search  search for parameters
-r, --report  parse metrics out of logs and display them
"""
import sys
import pickle
import warnings

import pandas as pd
import datetime as dt

from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV

from time import time
from tester import test_classifier, dump_classifier_and_data
from poi_dataset import fix_broken_records, clean_df, create_features, \
    features_split_df, features_combine_df
from poi_algo import Algo, ExtraFeatures, create_pipeline, create_scorer
from poi_utils import init_logfile, close_logfile, subset_name, algo_name, \
    retrieve_all_metrics_df

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
### You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

data_dict = fix_broken_records(data_dict)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)

df = pd.DataFrame.from_dict(data_dict, orient='index')
df = clean_df(df)


def evaluate_clasifier(df, extras, algo, dump=False):
    """Evaluate and possibly store classifier and data"""

    if not dump:
        # Only redirect output for the search
        orig_stdout, logfile = init_logfile(extras, algo)

    ### Task 3: Create new feature(s)
    df = create_features(df, *extras)

    ### Extract features and labels from dataset for local testing
    dfx, dfy = features_split_df(df)

    ### Task 4: Try a varity of classifiers
    ### Please name your classifier clf for easy export below.
    ### Note that if you want to do PCA or other multi-stage operations,
    ### you'll need to use Pipelines. For more info:
    ### http://scikit-learn.org/stable/modules/pipeline.html

    ### Task 5: Tune your classifier to achieve better than .3 precision and recall
    ### using our testing script. Check the tester.py script in the final project
    ### folder for details on the evaluation method, especially the test_classifier
    ### function. Because of the small size of the dataset, the script uses
    ### stratified shuffle split cross validation. For more info:
    ### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

    split_indices = StratifiedShuffleSplit(dfy, n_iter=1000, test_size=0.1)

    features_list = ['poi'] + dfx.columns.values.tolist()

    pipeline, params = create_pipeline(
        algo,
        extras,
        is_search=(not dump),
        max_features=len(dfx.columns))

    grid_searcher = GridSearchCV(
        pipeline,
        param_grid=params,
        cv=split_indices,
        n_jobs=-1,
        scoring=create_scorer(),
        verbose=0)

    t0 = time()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)

        grid_searcher.fit(dfx, y=dfy)
        print '\nTime to fit: {:0>8}\n'.format(dt.timedelta(seconds=(time() - t0)))

        print "Best parameters set:"
        print grid_searcher.best_params_
        print ''

        print 'Grid score:'
        for params, mean_score, scores in grid_searcher.grid_scores_:
            print "%0.3f for %r" % (mean_score, params)
        print ''

        selector = grid_searcher.best_estimator_.named_steps['selection']
        scored = pd.DataFrame(zip(
            dfx.columns.tolist(),
            selector.scores_,
            selector.get_support()))

        scored.columns = ['Feature', 'Score', 'Selected']
        scored = scored.sort_values(by=['Score'], ascending=False)
        scored.index = range(1, len(scored) + 1)
        n_selected = len(scored[scored.Selected])
        print 'Scored features: {} selected'.format(n_selected)
        print scored
        print ''

        # n_pca_components = grid_searcher.best_estimator_.named_steps[
        #     'reducer'].n_components_

        # print "Reduced to {0} PCA components".format(n_pca_components)

        ### Task 6: Dump your classifier, dataset, and features_list so anyone can
        ### check your results. You do not need to change anything below, but make sure
        ### that the version of poi_id.py that you submit can be run on its own and
        ### generates the necessary .pkl files for validating your results.

        clf = grid_searcher.best_estimator_

        ### Store to my_dataset for easy export below.
        df = features_combine_df(dfx, dfy)
        my_dataset = df.to_dict(orient='index')

        test_classifier(clf, my_dataset, features_list)

        if dump:
            dump_classifier_and_data(clf, my_dataset, features_list)
        else:
            close_logfile(orig_stdout, logfile)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd in ['-s', '--search']:
        # Search all possible classifiers and their parameters and output
        # results to log files
        t0 = time()
        for extras in ExtraFeatures.all_values():
            subname = subset_name(extras)
            for algo in Algo.all_values():
                algoname = algo_name(algo)
                print 'Features: {}, evaluating {}'.format(subname, algoname)
                evaluate_clasifier(df, extras, algo, dump=False)

        print '\nTotal time {:0>8}\n'.format(dt.timedelta(seconds=(time() - t0)))
    elif cmd in ['-r', '--report']:
        log_root = sys.argv[2] if len(sys.argv) > 2 else None
        mdf = retrieve_all_metrics_df(log_root)
        print 'Metrics sorted by precision and recall:\n'
        mds = mdf.sort_values(by=['Precision', 'Recall'], ascending=False)
        mds.index = range(1, len(mds) + 1)
        print mds
        print ''
        print 'Metrics with precision and recall equal to or above 0.3:\n'
        print mds[(mds['Precision'] >= 0.3) & (mds['Recall'] >= 0.3)]
        print ''
    else:
        # Just dump the best pre-selected classifier
        extras = ExtraFeatures.NONE
        algo = Algo.LOG_REG
        t0 = time()
        evaluate_clasifier(df, extras, algo, dump=True)
        print '\nTotal time {:0>8}\n'.format(dt.timedelta(seconds=(time() - t0)))
