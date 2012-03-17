#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" French electricity production mix analysis
over the July 2010 - March 2012 period, using data from "RTE éCO2mix"

* Ability to plot a stacked production graph,
  with a selectable stacking order.
* TODO : add production *averages*

Pierre Haessig — Marchy 2012
"""
from __future__ import print_function, division

from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Which data file to load
fname = 'RTE_eCO2mix_2010-07-08_2012-03-15.csv'
start_day = date(2010,7,8)


prod_headers = [u'Nucléaire', u'Gaz',u'Charbon', u'Fioul + pointe',
                u'Hydraulique', u'Éolien',
                u'Autres', u'Import']
prod_colors = ['#f5da00', '#ff8c04' ,'#ff5704','#d71818',
               '#015cfb','#03dd80',
               '#8303dd', '#353137']

## Load the data file (big) :
#data = np.genfromtxt(fname, delimiter=',',
#                     skip_header=1, usecols = [1]+range(4,12),
#                     missing='NA', usemask=True)
#data /= 1000 # Scale power from MW to GW

## Load the datetime column:
#dtconv = lambda d: datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
#d = np.loadtxt(fname, delimiter=',', usecols=[0], dtype=object,  skiprows=1, converters={0:dtconv})

### Extract the data
# Consumption data:
consum = data[:,0]
consum.mask[consum == 100] = True # Remove a bunch of wrong data
# Production data
prod = data[:,1:]
N_prod = len(prod_headers)
assert N_prod == prod.shape[1]

# Column reordering: based on increasing std
zoom = np.arange(550*24*4, 600*24*4)
reordering = prod[zoom,:].std(axis=0).argsort()
reordering = [6,0,1,2,5,3,4,7]
prod_headers = [prod_headers[k] for k in reordering]
prod_colors = [prod_colors[k] for k in reordering]

prod = prod[:,reordering]
# Cumulated (or stacked) production
cumprod = prod.cumsum(axis=1)

# Time vector
N = len(consum)
t = np.arange(N, dtype=float)/(24*4)

################################################################################
# Plots

fig = plt.figure('elec mix')
fig.add_subplot(111, title = 'French electricity production mix',
                     xlabel='time (days)', ylabel='power (GW)')
# Use the proxy artist trick:
legend_artists = []
for k in range(N_prod):
    bottom = cumprod[:,k-1] if k>= 1 else 0.
    plt.fill_between(t, bottom, cumprod[:,k],
                     color=prod_colors[k], alpha=0.5,
                     label=prod_headers[k])
    legend_artists.append(mpl.patches.Rectangle((0, 0), 1, 1, fc=prod_colors[k]))
plt.legend(legend_artists, prod_headers, loc='upper right')
plt.grid(True)

