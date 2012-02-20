#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" RTE electricity consumption data aggregator

aggregate the daily CSV file from "RTE éCO2mix"
into a large one homogenous file

Pierre Haessig — February 2012
"""
from __future__ import print_function

import os.path, codecs
import datetime as dt
from RTE_eCO2mix_download import day_range
# How to order the columns in the aggregated file:
column_order = {u'Consommation'   : 0,
                u'PrévisionJ-1'   : 1,
                u'PrévisionJ'     : 2,
                u'Nucléaire'      : 3,
                u'Gaz'            : 4,
                u'Charbon'        : 5,
                u'Fioul + pointe' : 6,
                u'Hydraulique'    : 7,
                u'Eolien'         : 8,
                u'Autres'         : 9,
                u'Co2'            : 10,
                u'Solde'          : 11}

# Where are the data files:
name_pattern = os.path.join('RTE_eCO2mix_daily','RTE_CO2mix_%s.csv')

# First day with a valid header : June 24th, 2000
start_day = dt.date(2011,6,24)
stop_day = dt.date.today() # stop excluded from range

# Browse the daily data files:
for day in day_range(start_day, stop_day):
    datafilename = name_pattern % day.isoformat()
    if not os.path.exists(datafilename):
        raise ValueError('data file not found for day %s (filename: %s)' %\
                          (day.isoformat(), datafilename))
    # Open the daily file:
    with codecs.open(datafilename, encoding='utf-8') as dailyfile:
        line1 = dailyfile.readline()
        # Check validity of the first line:
        if not line1.startswith(u'Journée du'):
            raise ValueError('data file for day %s is not valid (filename: %s)' %\
                             (day.isoformat(), datafilename))
        # Read the header:
        header = dailyfile.readline().strip()
        # Compute column reordering:
        reorder = [column_order[label] for label in header.split('\t')[1:]]
        # Browse the daily file line by line (that is 15 minutes timestep)
        for hour in range(24):
            for minute in range(0,60,15):
                line = dailyfile.readline().strip().split('\t')
                # Check the continuity of time:
                assert line[0] == '%.2d:%.2d' % (hour, minute)
                linedata = line[1:]
                data_date = dt.datetime.combine(day, dt.time(hour, minute))
                # TODO : continue
