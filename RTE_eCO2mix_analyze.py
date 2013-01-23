#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" RTE electricity consumption data analyzer

analyze the CSV file formats of the "RTE éCO2mix" data files
(downloaded with RTE_eCO2mix_download.py )

Pierre Haessig — February 2012

Updates:
* January 2013: accounts for the new "éCO2mix v2" file format
  where headers are uniform.
  Also there is a new line about the "data status"

"""
from __future__ import print_function
import os.path, codecs
from glob import glob

target_dir = 'RTE_eCO2mix_daily'
target_glob = os.path.join(target_dir,'*.csv')
print('searching files like "%s"' % target_glob)
filenames =  glob(target_glob)
filenames.sort()

print('%d data files found' % len(filenames))
print('from "%s" to "%s"' % (os.path.basename(filenames[0]),
                             os.path.basename(filenames[-1])) )

### Analyze the 2nd line which gives the electricity data status ###############

# data status should be either:
# * "Données temps réel"
# * "Données consolidées" or
# * "Données définitives"

data_status_collection = []
data_status_first_occurence = []
for datafile in filenames:
    with codecs.open(datafile, encoding='utf-8') as dailyfile:
        line1 = dailyfile.readline()
        # Skip invalid file
        if not line1.startswith(u'Journée du'):
            print('skipping %s (invalid file)' % datafile)
            continue
        # Read the header
        data_status_line = dailyfile.readline().strip()
        if not data_status_collection:
            data_status_collection.append(data_status_line)
            data_status_first_occurence.append(datafile)
        elif data_status_line != data_status_collection[-1]:
            data_status_collection.append(data_status_line)
            data_status_first_occurence.append(datafile)

print('\nData status : %d changes found' % len(data_status_collection) )
for status, startfile in zip(data_status_collection, data_status_first_occurence):
    print(' * starting with "%s": %s' % (os.path.basename(startfile),
                                         status.encode('utf-8'))
         )

print('\n'+'-'*80)

### Analyze the 3rd line which contains column headers #########################
header_collection = []
header_first_occurence = []
for datafile in filenames:
    with codecs.open(datafile, encoding='utf-8') as dailyfile:
        line1 = dailyfile.readline()
        # Skip invalid file
        if not line1.startswith(u'Journée du'):
            print('skipping %s (invalid file)' % datafile)
            continue
        line2 = dailyfile.readline().strip()
        # Skip invalid file
        if not line2 in [u"Données temps réel", u"Données consolidées", u"Données définitives"]:
            print('skipping %s (invalid file)' % datafile)
            continue
        # Read the header
        header_line = dailyfile.readline().strip()
        if not header_collection:
            header_collection.append(header_line)
            header_first_occurence.append(datafile)
        elif header_line != header_collection[-1]:
            header_collection.append(header_line)
            header_first_occurence.append(datafile)

print('\nHeaders : %d changes found, %d different kinds' %\
                  (len(header_collection),
                   len(set(header_collection))) )
for header, startfile in zip(header_collection, header_first_occurence):
    print(' * starting with "%s":' % os.path.basename(startfile))
    print("   %s" % header.encode('utf-8'))

label_collection = set([label for header in  header_collection
                              for label in header.split('\t')])
label_collection = list(label_collection)
label_collection.sort()
print('\nLabels : %d different found' % len(label_collection))
print('\n'.join(label_collection))


print('\n'+'-'*80)

### Analyze data availability (starting at the 4th line) #######################
available_data_collection = []
available_data_first_occurence = []
for datafile in filenames:
    with codecs.open(datafile, encoding='utf-8') as dailyfile:
        line1 = dailyfile.readline()
        # Skip invalid file
        if not line1.startswith(u'Journée du'):
            print('skipping %s (invalid file)' % datafile)
            continue
        line2 = dailyfile.readline().strip()
        # Skip invalid file
        if not line2 in [u"Données temps réel", u"Données consolidées", u"Données définitives"]:
            print('skipping %s (invalid file)' % datafile)
            continue
        # Read line 3 and 4:
        # Decode the header
        headers = dailyfile.readline().strip().split('\t')
        # Decode the first data line
        data = dailyfile.readline().strip().split('\t')
        
        # Find out which data is truly available (that is not empty or "ND")
        available_data = []
        for h,d in zip(headers, data):
            if d == '' or d == 'ND':
                continue
            else:
                available_data.append(h)
        
        # Combine available headers in one string (for hashability)
        available_data = '\t'.join(available_data)
        
        # Save this header if it's different from the previous file:
        if not available_data_collection or available_data != available_data_collection[-1]:
            available_data_collection.append(available_data)
            available_data_first_occurence.append(datafile)


print('\nAvailable data : %d changes found, %d different kinds' %\
                  (len(available_data_collection),
                   len(set(available_data_collection))) )
for header, startfile in zip(available_data_collection, available_data_first_occurence):
    print(' * starting with "%s":' % os.path.basename(startfile))
    print("   %s" % header.encode('utf-8'))
