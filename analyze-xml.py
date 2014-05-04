#!/usr/bin/env python

import xml.etree.ElementTree
import glob
import string
import os
import collections
import re

authorToNumber = collections.defaultdict(list)
numberToWords = collections.defaultdict(set)
numberToWordCount = collections.defaultdict(int)
for xmlfile in glob.iglob('xml/*.xml'):
  xmlNumber = int(string.split(os.path.split(xmlfile)[1], '.')[0])
  try:
    xmldata = xml.etree.ElementTree.parse(xmlfile)
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
    for child in xmldata.getroot().iter('p'):   # does the text
      if child.text is not None:
        lowerText = string.lower(child.text)
        mangledText = re.sub(r'\W+', ' ', lowerText)  # removes non alphabet
        words = string.split(mangledText)
        numberToWords[xmlNumber].update(words)
        numberToWordCount[xmlNumber] += len(words)
  except xml.etree.ElementTree.ParseError:  # article not valid xml
    pass
#for test in authorToNumber.itervalues():
#  print test
for xmlNumber in numberToWords.iterkeys():
  print len(numberToWords[xmlNumber]), numberToWordCount[xmlNumber]
