#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]


def audit_file(filename, fields):
    fieldtypes = {
        field_name: set() for field_name in fields
    }

    def is_none(x):
        return x in ["NULL", ""]

    def is_list(x):
        return x and isinstance(x, basestring) and x.startswith("{")

    def is_int(x):
        try:
            y = int(x)
            return True
        except:
            return False

    def is_float(x):
        if not is_int(x):
            try:
                y = float(x)
                return True
            except:
                pass
        return False

    with open(filename, 'r') as f:
        r = csv.DictReader(f)

        # skip few first rows
        for i in range(4):
            r.next()

        for row in r:
            for k, v in row.items():
                if k in fieldtypes:
                    if is_none(v):
                        fieldtypes[k].add(type(None))
                    elif is_list(v):
                        fieldtypes[k].add(type([]))
                    elif is_int(v):
                        fieldtypes[k].add(int)
                    elif is_float(v):
                        fieldtypes[k].add(float)
                    else:
                        fieldtypes[k].add(str)

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
