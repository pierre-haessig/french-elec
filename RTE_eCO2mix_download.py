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
    # Forge the HTTP POST request 
    url = 'http://clients.rte-france.com/servlets/MixtrServlet?dl=DATAJOURXLS'
    content = urllib.urlencode([('jour',date_str),('dl','Télécharger')])
    # Download the zipped data:
    a = urllib.urlopen(url,content)
    # Add some sanity checks
    assert a.headers['content-type'] == 'application/zip'
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

# Where to dowload the data files:
target_dir = 'RTE_eCO2mix_daily'

# First day with a valid header : June 24th, 2000
start_day = date(2000,6,24)
stop_day = date.today() # stop excluded from range

for day in day_range(start_day, stop_day):
    datafilename = os.path.join(target_dir, 'RTE_CO2mix_%s.csv' % day.isoformat())
    if os.path.exists(datafilename):
        print('skipping day %s [already downloaded]' % day.isoformat())
        continue
    # 1) Grab the daily data:
    datafile = get_daily_data(day)
    # 2) Write the CSV file:
    with codecs.open(datafilename, 'w', encoding='utf-8') as out:
        out.write(datafile.read().decode('iso-8859-15'))

