#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" RTE electricity consumption data downloader

éCO2mix = consommation, production et contenu CO2 de l’électricité française
Source : http://www.rte-france.com/fr/developpement-durable/maitriser-sa-consommation-electrique/eco2mix-consommation-production-et-contenu-co2-de-l-electricite-francaise#telechargement

Pierre Haessig — December 2011
updates:
 * february 2012 : zip file unpacking
"""

import urllib, urllib2
import codecs, os.path
from tempfile import TemporaryFile
from zipfile import ZipFile
from datetime import date, timedelta

def day_range(start, stop, step = timedelta(days=1)):
    '''range of date objects, with a default step of 1 day
    (like in `range`, `stop` is excluded from the range)'''
    d = start
    while d < stop:
        yield d
        d += step

def get_daily_data(day):
    '''get the daily electricty consumption data from
    
    Note that the output file may be empty if the requested day
    is too far in time. (year 2000)
    
    Parameters
    ----------
    day : datetime.date object
        which day to grab
    
    Returns
    -------
    data : file-like object
        daily CSV data file in a ISO-8859-15 encoding
    '''
    print('dowloading RTE data for day %s...' % day.isoformat())
    date_str = day.strftime('%d/%m/%Y') # like '31/02/2012'
    # Forge the HTTP GET request 
    url = 'http://www.rte-france.com/curves/eco2mixDl'
    content = urllib.urlencode([('date',date_str)])
    # Download the zipped data:
    a = urllib.urlopen(url,content)
    # Add some sanity checks
    # 'content-disposition' header is 'attachment; filename="eCO2mix_RTE_2013-01-01.zip"'
    assert a.headers['content-disposition'].startswith('attachment; filename=')
    # Write the zip archive to a tmp file
    tmp = TemporaryFile()
    tmp.write(a.read())
    # Open the zip file:
    z = ZipFile(tmp)
    # The archive only contains one file :
    assert len(z.namelist()) == 1
    conso_filename = z.namelist()[0]
    #print('extracting %s...' % conso_filename)
    # Open the data file in the zip archive
    return z.open(conso_filename)
# end get_daily_data()

def get_data_range(start_day, stop_day, target_dir):
    '''download a range of daily data from RTE éCO2mix
    between `start_day` and `stop_day` (excluded)
    
    data consist of CSV files (tab separated, utf-8 encoding).
    Those files are saved in `target_dir`.
    '''
    name_pattern = os.path.join(target_dir, 'RTE_CO2mix_%s.csv')
    for day in day_range(start_day, stop_day):
        datafilename = name_pattern % day.isoformat()
        if os.path.exists(datafilename):
            print('skipping day %s [already downloaded]' % day.isoformat())
            continue
        # 1) Grab the daily data:
        datafile = get_daily_data(day)
        # 2) Write the CSV file:
        with codecs.open(datafilename, 'w', encoding='utf-8') as out:
            out.write(datafile.read().decode('iso-8859-15'))
# end get_data_range()

# Where to dowload the data files:
target_dir = 'RTE_eCO2mix_daily'

# First day with a valid header : June 24th, 2000
start_day = date(2000,6,24)
stop_day = date.today() # stop excluded from range

if __name__ == '__main__':
    print('Downloading RTE éCO2mix data')
    print(' from day %s to %s' % (start_day.isoformat(), stop_day.isoformat()))
    get_data_range(start_day, stop_day, target_dir)

