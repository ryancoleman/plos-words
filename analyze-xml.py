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

authorToNumber = collections.defaultdict(list)
numberToWords = collections.defaultdict(set)
numberToWordCount = collections.defaultdict(int)
for xmlfile in glob.iglob('xml/00000*.xml.bz2'):
  xmlNumber = int(string.split(os.path.split(xmlfile)[1], '.')[0])
  try:
    xmldata = xml.etree.ElementTree.parse(bz2.BZ2File(xmlfile, 'rb'))
    for child in xmldata.getroot().iter('contrib'):  # parses outh author
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
            numberToWords[xmlNumber].update([stemmed])
        numberToWordCount[xmlNumber] += len(words)
  except xml.etree.ElementTree.ParseError:  # article not valid xml
    pass
#for test in authorToNumber.itervalues():
#  print test
for xmlNumber in numberToWords.iterkeys():
  #print numberToWords[xmlNumber]
  print xmlNumber, len(numberToWords[xmlNumber]), numberToWordCount[xmlNumber],
  print len(numberToWords[xmlNumber])/float(numberToWordCount[xmlNumber])
