#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" French electricity consumption analysis
over the June 2000 - February 2012 period, using data from "RTE éCO2mix"

* finds the consumption records (peak demand)
* plots the consumption over the years (average and min-max)

Pierre Haessig — February 2012
"""
from __future__ import print_function, division

from datetime import date, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Which data file to load
fname = 'RTE_eCO2mix_2000-06-24_2012-02-19.csv'
start_day = date(2000,6,24)

# Load the data file (big) :
data = np.genfromtxt(fname, delimiter=',',
                     skip_header=1, usecols = range(1,12+1),
                     missing='NA', usemask=True)

### Extract the data
# Consumption data:
consum15m = data[:,0]
consum15m.mask[consum15m == 100] = True # Remove a bunch of wrong data
consum15m = consum15m/1000 # Scale power from MW to GW

# Time vector
N15m = len(consum15m)
t15m = np.arange(N15m, dtype=float)/(24*4)

print('Electricity data loaded over %.1f years' % (N15m/4/24/365.25))

### Analysis: ##################################################################

# Helper function
def running_record(x, xmin, delta_min=0):
    '''find the running record in the `x` vector
    records values under xmin are skipped.
    records closer than `delta_min` are skipped
    returns (arg_records, records)
    '''
    arg_records = []
    records = []
    running_rec = xmin
    for i in xrange(len(x)):
        if x[i] > running_rec:
            # a new record is found
            # 1) check that the previous one is not too closer
            if arg_records and i - arg_records[-1] < delta_min:
                # Delete the previous record:
                arg_records.pop(-1)
                records.pop(-1)
            # 2) Save the new record
            running_rec = x[i]
            arg_records.append(i)
            records.append(running_rec)
    return (arg_records, records)
# end running_record()

# Compute consumption records (at least 6 hours apart):
P_min = 70 # GW
(arg_records, records) = running_record(consum15m, P_min, delta_min = 6*4)
print('Consumption records (peaks) above %d GW : %d' % (P_min, len(records)))

for rec_idx, rec_value in zip(arg_records, records):
    rec_day = start_day + timedelta(rec_idx//(4*24))
    rec_time = (rec_idx % (4*24)) # counted in 15 minutes intervals
    rec_hour = rec_time // 4
    rec_minute = (rec_time % 4)*15
    print('%s : %5.1f GW (%s, %02d:%02d)' % \
          (rec_day.isoformat(),rec_value,
           rec_day.strftime('%a'), rec_hour, rec_minute))


### Compute some averages:
# Daily averages
consum1d = consum15m.reshape(-1,24*4).mean(axis=1)
N1d = len(consum1d)
t1d = np.arange(N1d, dtype=float)+ 1/2

# Weekly averages:
day_skip=2 # Skip 2 days to start on Monday 2000-06-26
consum7d = consum1d[2:].reshape(-1,7).mean(axis=1)
N7d = len(consum7d)
t7d = np.arange(N7d, dtype=float)*7 + 7/2 + day_skip

# Compute some percentiles statistics
consum7d_min = consum15m[day_skip*24*4:].reshape(-1,7*24*4).min(axis=1)
consum7d_max = consum15m[day_skip*24*4:].reshape(-1,7*24*4).max(axis=1)

### Plot: ######################################################################
plt.figure('electricity consumption')
plt.title('Weekly electricty consumption average (2000-06-26 -> 2012-02-19)')

# Plot weekly min-max
plt.fill_between(t7d, consum7d_min, consum7d_max, 
                 lw=0, alpha=0.3)
## Plot 15 minutes data :
# plt.plot(t15m, consum15m, 'b', alpha=0.5)
# creates rectangle patch for legend use.
f_minmax = mpl.patches.Rectangle((0, 0), 1, 1, alpha=0.3)
# Plot Weekly average :
l_avg = plt.plot(t7d, consum7d, 'r')
# Plot Consumption records :
l_rec = plt.plot(t15m[arg_records], records, 'rD')

plt.legend(l_avg + [f_minmax] + l_rec ,
           ['weekly average', 'weekly min-max', 'records'],
           loc='upper left')

plt.xlabel('time [years]')
year_range = range(2001,2013)
plt.xticks([(date(y,1,1)-start_day).days for y in year_range], year_range)
plt.ylabel('Power [GW]')
plt.grid(True)
plt.show()
