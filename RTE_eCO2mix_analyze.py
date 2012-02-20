#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" RTE electricity consumption data analyzer

analyze the CSV file formats of the "RTE éCO2mix" data files
(downloaded with RTE_eCO2mix_download.py )

Pierre Haessig — February 2012
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

header_collection = []
header_first_occurence = []
for datafile in filenames:
    with codecs.open(datafile, encoding='utf-8') as dailyfile:
        line1 = dailyfile.readline()
        # Skip invalid file
        if not line1.startswith(u'Journée du'):
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
