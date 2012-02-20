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
reordered_header = [u'Consommation', u'PrévisionJ-1', u'PrévisionJ',
                    u'Nucléaire', u'Gaz', u'Charbon', u'Fioul + pointe',
                    u'Hydraulique', u'Eolien',  u'Autres',
                    u'Solde',  u'Co2']


# Where are the data files:
filename_pattern = os.path.join('RTE_eCO2mix_daily','RTE_CO2mix_%s.csv')

# First day with a valid header : June 24th, 2000
start_day = dt.date(2000,6,24)
stop_day = dt.date.today() # stop excluded from range

aggregated_filename = 'RTE_eCO2mix_%s_%s.csv' % \
                       (start_day.isoformat(),
                       (stop_day - dt.timedelta(1)).isoformat())

def reordered_data_range(start_day, stop_day, 
                         filename_pattern, reordered_header,
                         NA = 'NA', colsep=','):
    '''generator of reordered data lines
    
    browse the daily éCO2mix data to yield reformatted lines data
    
    Parameters
    ----------
    start_day : datetime.date object
        at which day to start yielding data
    stop_day : datetime.date object
        at which date to stop yielding data (excluded from range)
    filename_pattern : str,
        where are the data files, with a "%s" to insert the date stamp
    reordered_header : list of str
        what data order is requested
    NA : str, optional
        What symbol to mark unavailable data
        [default to 'NA']
    colsep : str, optional
        What symbol to separate data columns
        [default to ',']
    '''
    # Build the header order Look-up Table:
    nb_column = len(reordered_header)
    order_lut = dict((label, i) 
                     for (label, i)
                     in zip(reordered_header,
                            range(nb_column)) )
    # Yield the header:
    yield colsep.join([u'Timestamp']+reordered_header)+'\n'
    # Browse the daily data files:
    for day in day_range(start_day, stop_day):
        datafilename = filename_pattern % day.isoformat()
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
            # Read the file header:
            header = dailyfile.readline().strip()
            header = header.split('\t')[1:] # drop the first label "Heures"
            # Compute column reordering:
            reorder = [order_lut[label] for label in header]
            # Browse the daily file line by line 
            for hour in range(24):
                for minute in range(0,60,15): # timestep is 15 minutes
                    # Split columns
                    line = dailyfile.readline().strip().split('\t')
                    # 1) Process the timestamp
                    # Check the continuity of time:
                    assert line[0] == '%.2d:%.2d' % (hour, minute)
                    data_date = dt.datetime.combine(day, dt.time(hour, minute))
                    timestamp = [data_date.isoformat()]
                    
                    # 2) Process the data
                    line_data = line[1:]
                    # Build the reordered data
                    reordered_data = [NA]*nb_column
                    for i,data in zip(reorder, line_data):
                        if data: 
                            reordered_data[i] = data
                    # 3) Paste time and data together:
                    yield colsep.join(timestamp + reordered_data)+'\n'

if __name__ == '__main__':
    print('Aggregating daily data from %s to %s in "%s"...' %\
          (start_day.isoformat(), stop_day.isoformat(), aggregated_filename) )
    # Create the line generator:
    reordered_data_gen = reordered_data_range(start_day, stop_day,
                                              filename_pattern, reordered_header)
    # Write the data in one big file:
    with codecs.open(aggregated_filename, 'w', encoding='utf-8') as out:
        out.writelines(reordered_data_gen)
