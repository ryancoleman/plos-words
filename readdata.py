#!/usr/bin/env python

import collections
import string

#reads all the data in plos-words files produced by analyze-xml.py

def yearToNumber(filename='year.to.number.txt'):
  yearToNumber = collections.defaultdict(list)
  for line in open(filename, 'r'):
    tokens = string.split(line)
    try:
      yearToNumber[int(tokens[0])].extend([int(token) for token in tokens[1:]])
    except ValueError:
      pass  # some articles don't have years.
  return yearToNumber

def readTwoColumnIntIntoDict(filename):
  returnDict = {}
  for line in open(filename, 'r'):
    tokens = string.split(line)
    returnDict[int(tokens[0])] = int(tokens[1])
  return returnDict

def numberToUnique(filename='number.to.unique.words.count.txt'):
  return readTwoColumnIntIntoDict(filename)

def numberToCount(filename='number.to.count.txt'):
  return readTwoColumnIntIntoDict(filename)

def numberToWordiness():
  numberToUniqueDict = numberToUnique()
  numberToCountDict = numberToCount()
  numberToWordiness = {}
  for xmlNumber in numberToUniqueDict.iterkeys():
    try:
      numberToWordiness[xmlNumber] = numberToUniqueDict[xmlNumber]/float(
          numberToCountDict[xmlNumber])
    except KeyError:
      pass  # means the article xml was invalid
  return numberToWordiness  

def yearToWordiness():
  yearToNumberDict = yearToNumber()
  numberToWordinessDict = numberToWordiness()
  yearToWordinessDict = collections.defaultdict(list)
  for year, numberList in yearToNumberDict.iteritems():
    for oneNumber in numberList:
      yearToWordinessDict[year].append(numberToWordinessDict[oneNumber])
  return yearToWordinessDict
