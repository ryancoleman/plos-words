#!/usr/bin/env python

import bokeh.plotting
import readdata
import statistics

bokeh.plotting.output_file("wordiness-by-year.html", title="wordiness-by-year")

yearToWordiness = readdata.yearToWordiness(include=['research-article'])
dataTable = [], []
for year in sorted(yearToWordiness.iterkeys()):
  dataTable[0].append(year)
  dataTable[1].append(statistics.computeMean(yearToWordiness[year]))
allDataTable = [], []
for year in sorted(yearToWordiness.iterkeys()):
  for oneWordiness in yearToWordiness[year]:
    allDataTable[0].append(year)
    allDataTable[1].append(oneWordiness)
bokeh.plotting.scatter(
    dataTable[0], dataTable[1],
    color='red', fill_alpha=0.2, size=20, name="mean-wordiness")
bokeh.plotting.scatter(
    allDataTable[0], allDataTable[1],
    color='blue', fill_alpha=0.2, size=1, name="wordiness")
bokeh.plotting.show()
