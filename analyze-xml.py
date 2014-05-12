#!/usr/bin/env python

import xml.etree.ElementTree
import glob
import string
import os
import collections
import re
import porter2
import itertools
import bz2

def isNumber(word):
  '''helper that returns True iff the word is a number.'''
  try:
    float(word)
    return True
  except ValueError:
    return False

#track these 4 things. we'll write them out to plain files.
authorToNumber = collections.defaultdict(list)
numberToWordCount = collections.defaultdict(int)
yearToNumber = collections.defaultdict(list)
numberToType = collections.defaultdict(list)
#this needs written out on the fly for memory usage reasons
outNTW = open('number.to.words.txt', 'w')
for xmlfile in glob.iglob('xml/*.xml.bz2'):
  xmlNumber = int(string.split(os.path.split(xmlfile)[1], '.')[0])
  numberToWords = set()
  try:
    xmldata = xml.etree.ElementTree.parse(bz2.BZ2File(xmlfile, 'rb'))
    for child in xmldata.getroot().iter('article'):  # may want to exclude 
      if 'article-type' in child.attrib:           # corrections
        numberToType[xmlNumber].append(child.attrib['article-type'])
    for child in xmldata.getroot().iter('copyright-year'):  # parses out year
      yearToNumber[child.text].append(xmlNumber)
    for child in xmldata.getroot().iter('contrib'):  # parses out author
      if 'contrib-type' in child.attrib:
        if child.attrib['contrib-type'] == 'author':
          surname, givenname = '', ''
          for data in child.iter('surname'):
            surname = data.text
          for data in child.iter('given-names'):
            givenname = data.text
          authorToNumber[string.join([givenname, surname], ' ')].append(
              xmlNumber)
    for child in itertools.chain(
        xmldata.getroot().iter('p'), xmldata.getroot().iter('title')):
      #does the text
      if child.text is not None:
        lowerText = string.lower(child.text).encode('ascii', 'ignore')
        mangledText = re.sub(r'\W+', ' ', lowerText)  # removes non alphabet
        words = string.split(mangledText)
        for word in words:
          stemmed = porter2.stem(word)  # stemming removes -ing -ed etc
          if not isNumber(stemmed):   # if converts to a float, don't do it
            numberToWords.update([stemmed])
        numberToWordCount[xmlNumber] += len(words)
  except xml.etree.ElementTree.ParseError:  # article not valid xml
    pass
  outNTW.write(str(xmlNumber) + ' ' + str(len(numberToWords)) + ' ')
  for oneWord in numberToWords:
    outNTW.write(oneWord + ' ')
  outNTW.write('\n')
outNTW.close()
#just write these to plaintext files. janky but lets others use the data
#easily without having to unpack pickled files or whatever other solution
#i could choose from.
outNTT = open('number.to.type.txt', 'w')
for outdata in numberToType.iteritems():
  outNTT.write(str(outdata[0]) + ' ')
  for typeData in outdata[1]:
    outNTT.write(str(typeData) + ' ')
  outNTT.write('\n')
outNTT.close()
outATN = open('author.to.number.txt', 'w')
for outdata in authorToNumber.iteritems():
  outATN.write(str(outdata[0].encode('ascii', 'replace')) + ' ')
  for oneNumber in outdata[1]:
    outATN.write(str(oneNumber) + ' ')
  outATN.write('\n')
outATN.close()
outNTC = open('number.to.count.txt', 'w')
for xmlNumber in numberToWordCount.iterkeys():
  outNTC.write(str(xmlNumber) + ' ' + str(numberToWordCount[xmlNumber]) + '\n')
outNTC.close()
outYTN = open('year.to.number.txt', 'w')
for year, numberList in yearToNumber.iteritems():
  outYTN.write(str(year) + ' ')
  for oneNumber in numberList:
    outYTN.write(str(oneNumber) + ' ')
  outYTN.write('\n')
outYTN.close()
