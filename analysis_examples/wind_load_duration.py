#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" French wind power production analysis
over the July 2010 - March 2012 period, using data from "RTE éCO2mix"

Pierre Haessig — July 2012
"""
from __future__ import print_function, division

from datetime import date, datetime, timedelta
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib as mpl

# Which data file to load
fname = 'RTE_eCO2mix_2010-07-08_2012-03-15.csv'
start_day = date(2010,7,8)


prod_headers = [u'Nucléaire', u'Gaz',u'Charbon', u'Fioul + pointe',
                u'Hydraulique', u'Éolien',
                u'Autres', u'Import']
wind_column = prod_headers.index(u'Éolien') # aka = 5
wind_color = '#03dd80'

### Load the data file (big) :
data = np.genfromtxt(fname, delimiter=',',
                     skip_header=1, usecols = [1]+range(4,12),
                     missing='NA', usemask=True)
data /= 1000 # Scale power from MW to GW

# Load the datetime column:
dtconv = lambda d: datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
d = np.loadtxt(fname, delimiter=',', usecols=[0], dtype=object,  skiprows=1, converters={0:dtconv})

### Extract the data
# Consumption data:
consum = data[:,0]
consum.mask[consum == 100] = True # Remove a bunch of wrong data
# Production data
prod = data[:,1+wind_column]


# Time vector
N = len(consum)
t = np.arange(N, dtype=float)/(24*4)

### Compute some running averages ###
# fill in the blanks
prod_filled = prod.filled(0)
# average over 24 hours
prod_d1 = sig.lfilter([1]*24*4, [24*4], prod_filled)
# average over 7 days
prod_d7 = sig.lfilter([1]*24*4*7, [24*4*7], prod_filled)
# average over 30 days
prod_d30 = sig.lfilter([1]*24*4*30, [24*4*30], prod_filled)

# Normalization, with respect to the rated wind power, which
# increases along time.
# TODO : find the correct rated power values
Pnom = 4. + t/t[-1]*2.5 # dummy model of a linear increase from 4 GW to 6 GW

#prod /= Pnom
#prod_filled /= Pnom
#prod_d1 /= Pnom
#prod_d7 /= Pnom
#prod_d30 /= Pnom

### Some statistics
Pmean = prod.mean() # this is the average load rather than the average power

################################################################################
# Plots

fig = plt.figure('wind prod')
fig.add_subplot(111, title='wind power production along time',
                     xlabel='time (days)', ylabel='power (pu)')
#plt.fill_between(t, prod, color=wind_color, lw=0)
#plt.plot(t-0.5, prod_d1, 'c-')
#plt.plot(t-3.5, prod_d7, 'b-')
#plt.plot(t-15, prod_d30, 'r-')

td_d1 = timedelta(1) # 1 day
plt.fill_between(d, prod, color=wind_color, lw=0)
plt.plot(d-td_d1//2, prod_d1, 'c-', label='24 hours avg power')
plt.plot(d-7*td_d1//2, prod_d7, 'b-', label='7 days avg power')
plt.plot(d-15*td_d1, prod_d30, 'r-', label='30 days avg power')
# rotate the xlabels because of the long dates:
plt.xticks(rotation=45)
plt.legend()


### Load duration curve of Wind Power
fig = plt.figure('wind ldc')
fig.add_subplot(111, title='wind power load duration curve',
                     xlabel='fraction of time (%)', ylabel='power (pu)')

plt.plot(t/t[-1]*100, np.sort(prod_filled)[::-1], 'b-', label='15 min avg power')
plt.plot(t/t[-1]*100, np.sort(prod_d1)[::-1], 'c-', label='24 hours avg power')
plt.plot(t/t[-1]*100, np.sort(prod_d7)[::-1], 'g-', label='7 days avg power')
plt.plot(t/t[-1]*100, np.sort(prod_d30)[::-1], 'r-', label='30 days avg power')
plt.hlines(Pmean, 0,100, colors='r', linestyles='dashed', label='avg load')
plt.legend(loc='upper right')

plt.xlim(0,103)

plt.show()
