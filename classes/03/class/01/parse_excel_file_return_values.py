#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    max_coast = None
    max_time = None
    min_coast = None
    min_time = None
    total_coast = 0

    for r in range(1, sheet.nrows):
        coast = sheet.cell_value(r, 1)

        if coast > max_coast or max_coast is None:
            max_coast = coast
            max_time = sheet.cell_value(r, 0)

        if coast < min_coast or min_coast is None:
            min_coast = coast
            min_time = sheet.cell_value(r, 0)

        total_coast += coast

    data = {
            'maxtime': xlrd.xldate_as_tuple(max_time, 0),
            'maxvalue': max_coast,
            'mintime': xlrd.xldate_as_tuple(min_time, 0),
            'minvalue': min_coast,
            'avgcoast': total_coast / (sheet.nrows - 1)
    }
    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()