#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
import pandas as pd

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

total_rows = len(enron_data)
df = pd.DataFrame.from_dict(enron_data, orient='index')
poi_count = df[df.poi == 1].shape[0]
other_count = total_rows - poi_count

print "* total number of data points:", len(enron_data)
print "* POI: {}, non-POI: {} ({:.0%} POI)".format(poi_count, other_count, float(poi_count) / total_rows)
print "* features ({} total):".format(df.dtypes.count())
for c in list(df):
    nans = df[c][df[c] == 'NaN'].count() if df[c].dtype == object else 0
    print ' - {} : {:.0%} empty'.format(c, float(nans) / total_rows)
