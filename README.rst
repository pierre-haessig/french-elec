:::::::::::::::::
RTE éCO2mix tools
:::::::::::::::::

Various simple tools to play with the *RTE éco2mix* data :
a set of publicly available tables about the French electricty market,
provided by the French Transmission system operator (TSO) RTE.

**Original data source [FR]** : RTE's website

http://www.rte-france.com/fr/developpement-durable/eco2mix
http://www.rte-france.com/fr/developpement-durable/eco2mix/telechargement-de-donnees


About the data
==============

Data is available as 15 minutes averages. 
The richness of the content increases over time :

* starting June 24th, 2000, *consumption* + *D-1 forecast* is available
* starting July 8th, 2010, production data is also available
  (detailed by production means : nuclear, hydro, wind, ...)

*Note* : RTE does't guarantee this data to be accurate.
It is provided for "informative" purpose only.

*Note2* : starting December 2012, RTE moved to "éCO2mix v2" file format,
described in "specifications_fichiers_eco2mix_V2.pdf" [FR]


Tools
=====

Tools available in this "package" :

* *RTE_eCO2mix_download.py*
  download data files from RTE's website
* *RTE_eCO2mix_analyze.py*
  analyze the content of those files, because they are not homogenous

Analysis examples
-----------------
located in the dedicated subdirectory `analysis_examples`

* *elec_consumption.py*
  plots the *weekly consumption average* over the 2000 - 2012 period.
  It also finds the consumption *records* over this period.

.. image:: https://github.com/pierre-haessig/french-elec/raw/master/analysis_examples/weekly_consumption_2001-2011_with_records.png
    :height: 20em

* *elec_production_mix.py*
  plots the electricity **production mix** (that is, the amount of power
  generated by each technology) over the 2010 - 2012 period


* *load_duration.py*
  plots the *Load Duration Curve* for France, over the 2001-2011 period.

.. image:: https://github.com/pierre-haessig/french-elec/raw/master/analysis_examples/load_duration_curve_2001-2011.png
    :height: 20em

License
=======

These simple software tools are freely available under a standard BSD license.

*Pierre Haessig* -- 2012
