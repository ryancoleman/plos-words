#!/usr/bin/env python

import collections
import string

#reads all the data in plos-words files produced by analyze-xml.py

def numberToType(filename='number.to.type.txt'):
  numberToType = {}
  for line in open(filename, 'r'):
    tokens = string.split(line)
    numberToType[int(tokens[0])] = tokens[1]
  return numberToType 

def yearToNumber(filename='year.to.number.txt', include=None, exclude=None):
  if include is not None or exclude is not None:
    numberToTypeDict = numberToType()
  yearToNumber = collections.defaultdict(list)
  for line in open(filename, 'r'):
    tokens = string.split(line)
    try:
      for number in tokens[1:]:
        artNumber = int(number)
        if include is None or numberToTypeDict[artNumber] in include:
          if exclude is None or numberToTypeDict[artNumber] not in include:
            yearToNumber[int(tokens[0])].append(artNumber)
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

def yearToWordiness(exclude=None, include=None):
  yearToNumberDict = yearToNumber(exclude=exclude, include=include)
  numberToWordinessDict = numberToWordiness()
  yearToWordinessDict = collections.defaultdict(list)
  for year, numberList in yearToNumberDict.iteritems():
    for oneNumber in numberList:
      yearToWordinessDict[year].append(numberToWordinessDict[oneNumber])
  return yearToWordinessDict

def authorToNumber(filename='author.to.number.txt'):
  authorToNumber = {}
  for line in open(filename, 'r'):
    tokens = string.split(line)
    name = tokens[0]
    numbers = []
    for token in tokens[1:]:
      try:
        artNumber = int(token)
        numbers.append(artNumber)
      except ValueError:
        name += ' ' + token
    authorToNumber[name] = numbers
  return authorToNumber

def authorToWordiness(exclude=None, include=None):
  authorToNumberDict = authorToNumber()
  yearToNumberDict = yearToNumber(exclude=exclude, include=include)
  numberToWordinessDict = numberToWordiness()
  yearToWordinessDict = collections.defaultdict(list)
  for year, numberList in yearToNumberDict.iteritems():
    for oneNumber in numberList:
      yearToWordinessDict[year].append(numberToWordinessDict[oneNumber])
  return yearToWordinessDict
