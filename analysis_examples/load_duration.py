#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Load Duration Curve for France
evolution over the years 2001-2011

In the field of Electric Power Generation, the Load Duration Curve
is the name given to the quantile function of the power consumption over a year.

Quick reference :
http://en.wikipedia.org/wiki/Load_duration_curve

A separate source for the French Duration Curve in 2009 :
http://www.observatoire-electricite.fr/2010/fiche/courbe-monotone-de-consommation-d%E2%80%99%C3%A9lectricit%C3%A9-pour-l%E2%80%99ann%C3%A9e-2009
(curve named "courbe monotone de consommation")

Pierre Haessig — March 2012
"""

from __future__ import division, print_function

from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Where to read:
fname = 'RTE_eCO2mix_2000-06-24_2012-02-19.csv'

years_of_interest = range(2001,2012)
print('Load duration curve analysis over the %d - %d period' %\
      (years_of_interest[0], years_of_interest[-1]))

# Load the datetime column:
print('reading time data...')
dtconv = lambda d: datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
time = np.loadtxt(fname, delimiter=',', usecols=[0], dtype=object,  skiprows=1, converters={0:dtconv})

# Load the consumption data, 15 minutes timestep :
print('reading consumption data...')
consum = np.genfromtxt(fname, delimiter=',',
                     skip_header=1, usecols = [1],
                     missing='NA', usemask=True)
consum.mask[consum == 100] = True # Remove a bunch of wrong data
consum /= 1000 # Scale power from MW to GW

# Retreive the year:
time_year = np.array([d.year for d in time])

# Hours vector, with a 15 minutes time step
hours = np.arange(366*24*4)/4

################################################################################
# Plot the load duration curves

# Choose a colormap:
cm = lambda x: mpl.cm.jet(0.2+0.7*x)

fig = plt.figure('load duration curve', figsize=(10,6))
fig.add_subplot(111, title = 'Load duration curve for France (%d - %d)' %\
                  (years_of_interest[0], years_of_interest[-1]),
                xlabel='Load duration (hours)',
                ylabel='Power consumption (GW)',
                axis_bgcolor='0.5',
                xlim=(-100,9500), ylim=(0,110))

# Compute some stats on the LDC
hours_of_interest = np.array([0,2000,4000,8000])
typical_power_min = np.zeros(len(hours_of_interest))+np.nan
typical_power_max = np.zeros(len(hours_of_interest))+np.nan

# Compute and plot the LDC for each year
for k,y in enumerate(years_of_interest):
    year_consum = consum[time_year==y]
    n_missing = year_consum.mask.sum()
    # Remove NaNs by padding median values:
    year_consum = year_consum.filled(fill_value = np.median(year_consum))
    # Sort the load power:
    sorted_consum = np.sort(year_consum)
    sorted_consum = sorted_consum[::-1] # Reverse the order
    L = len(sorted_consum)
    print('Year %d: %d days, %d missing data' %\
          (y, L/24/4 ,n_missing))
    # Plot
    color = cm(k/(len(years_of_interest)-1))
    plt.plot(hours[0:L], sorted_consum, label='year %d' % y, color=color)
    # Add the max and the min
    plt.plot(0, sorted_consum[0], 'D', color=color )
    plt.plot((L-1)/4, sorted_consum[-1], 'D', color=color )
    
    # Compute some stats
    typical_power = sorted_consum[hours_of_interest*4]
    typical_power_min = np.where(typical_power > typical_power_min,
                                 typical_power_min, typical_power)
    typical_power_max = np.where(typical_power < typical_power_max,
                                 typical_power_max, typical_power)
# Add some annotations
for i, h in enumerate(hours_of_interest):
    Pmin = typical_power_min[i]
    Pmax = typical_power_max[i]
    plt.annotate(u'ΔP=%.0f GW' % (Pmax-Pmin),
                (h, Pmin), (h+200, Pmin-25),
                va='top', ha='left', fontsize=12, rotation='horizontal',
                color='white',
                bbox=dict(boxstyle="round", fc="0.2"),
                arrowprops=dict(arrowstyle="->", connectionstyle="angle,"
                                "angleA=0,angleB=90,rad=10"))
    plt.annotate('',
                (h, Pmax), (h, Pmax +5),
                 arrowprops=dict(arrowstyle="->"))


leg = plt.legend(loc='upper right', prop={'size':10})
leg.get_frame().set_facecolor('0.6')
plt.grid(True)
plt.show()

