#!/usr/bin/env python

import bokeh.plotting
import readdata
import statistics

bokeh.plotting.output_file("wordiness-by-year.html", title="wordiness-by-year")

yearToNumber = readdata.yearToNumber()
numberToUnique = readdata.numberToUnique()
numberToCount = readdata.numberToCount()
numberToWordiness = readdata.numberToWordiness()
print numberToWordiness  
'''
scatter(
    flowers["petal_length"], flowers["petal_width"],
    fill_alpha=0.2, size=10, name="iris")

show()
'''
