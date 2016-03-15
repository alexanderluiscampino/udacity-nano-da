# -*- coding: utf-8
import numpy as np
import pandas as pd


def clean_df(df):
    """Cleanup original dataframe."""
    del df['email_address']  # Not a useful feature
    df = df.replace('NaN', np.nan)
    df = df.fillna(0)
    return df


def features_split_df(df):
    """Splits one dataframe into 2: features and labels."""
    features = df.drop('poi', axis=1).astype(float)
    labels = df['poi']
    return features, labels


def features_combine_df(features, labels):
    """Re-combine features and labels into one dataframe."""
    df = pd.concat([labels, features], axis=1)
    return df


def fix_broken_records(data_dict):
    """There are 2 records with incorrect values (do not match the PDF)."""

    # This is one record with all values NaN
    del data_dict['LOCKHART EUGENE E']

    data_dict['BELFER ROBERT'] = {
        'bonus': 'NaN',
        'deferral_payments': 'NaN',
        'deferred_income': -102500,
        'director_fees': 102500,
        'email_address': 'NaN',
        'exercised_stock_options': 'NaN',
        'expenses': 3285,
        'from_messages': 'NaN',
        'from_poi_to_this_person': 'NaN',
        'from_this_person_to_poi': 'NaN',
        'loan_advances': 'NaN',
        'long_term_incentive': 'NaN',
        'other': 'NaN',
        'poi': False,
        'restricted_stock': -44093,
        'restricted_stock_deferred': 44093,
        'salary': 'NaN',
        'shared_receipt_with_poi': 'NaN',
        'to_messages': 'NaN',
        'total_payments': 3285,
        'total_stock_value': 'NaN'
    }

    data_dict['BHATNAGAR SANJAY'] = {
        'bonus': 'NaN',
        'deferral_payments': 'NaN',
        'deferred_income': 'NaN',
        'director_fees': 'NaN',
        'email_address': 'sanjay.bhatnagar@enron.com',
        'exercised_stock_options': 15456290,
        'expenses': 137864,
        'from_messages': 29,
        'from_poi_to_this_person': 0,
        'from_this_person_to_poi': 1,
        'loan_advances': 'NaN',
        'long_term_incentive': 'NaN',
        'other': 'NaN',
        'poi': False,
        'restricted_stock': 2604490,
        'restricted_stock_deferred': -2604490,
        'salary': 'NaN',
        'shared_receipt_with_poi': 463,
        'to_messages': 523,
        'total_payments': 137864,
        'total_stock_value': 15456290
    }

    return data_dict


def create_features(df, total_financial=False, total_email=False,
                    fraction_email=False, remove_totals=False):
    """Add new features to pandas DataFrame.
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    if total_financial:
        df['total_income'] = df['total_payments'] + df['total_stock_value']

    if total_email:
        df['total_poi_correspondence'] = (
            df['from_poi_to_this_person'] +
            df['from_this_person_to_poi'] +
            df['shared_receipt_with_poi']
        )

    if fraction_email:
        df['fraction_to_poi'] = (df['from_this_person_to_poi'] /
                                 df['to_messages'].replace({0: np.nan}))
        df['fraction_from_poi'] = (df['from_poi_to_this_person'] /
                                   df['from_messages'].replace({0: np.nan}))

    if total_email and fraction_email:
        df['fraction_poi_correspondence'] = \
            df['total_poi_correspondence'] / \
            ((df['to_messages'] + df['from_messages']).replace({0: np.nan}))

    if remove_totals:
        df = df.drop('total_payments', axis=1)
        df = df.drop('total_stock_value', axis=1)

    df = df.fillna(0)

    return df
