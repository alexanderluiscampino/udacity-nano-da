# -*- coding: utf-8 -*-
import statsmodels.api as sm

def linear_regression(features, values):
    """
    Performs linear regression given a dataset with an arbitrary number of features.
    'features' is the input data points (or the X's) and 'values' is the output data points
    (or the Y's).

    Returns the intercept and the parameters, that is, the optimal values of theta.

    This page contains example code that may be helpful:
    http://statsmodels.sourceforge.net/0.5.0/generated/statsmodels.regression.linear_model.OLS.html
    """

    ###########################
    ### YOUR CODE GOES HERE ###
    ###########################
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    result = model.fit()
    intercept = result.params[0]
    params = result.params[1:]
    return intercept, params
