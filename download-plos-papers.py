#!/usr/bin/env python

#http://www.plosone.org/article/fetchObjectAttachment.action?
# uri=info%3Adoi%2F10.1371%2Fjournal.pone.0075992&representation=XML

import sys  # always, pretty much
import string  # string handling
import urllib2  # url handling
import urllib  # url encoding
import os
import argparse

def plosOneQuery(articleNumber):
  dataDict = {
      'uri': 'info:doi/10.1371/journal.pone.' + articleNumber,
      'representation': 'XML'}
  articleEncode = urllib.urlencode(dataDict)
  request = urllib2.Request(
      url='http://www.plosone.org/article/fetchObjectAttachment.action', 
      data=articleEncode)
  result = urllib2.urlopen(request)
  dataOut = result.read()
  return dataOut

try:
  os.mkdir('xml')
except OSError:   # directory exists
  pass  # which is fine
for number in xrange(10000):  # eventually change to 100000 and get them all
  artNumber = string.zfill(number, 7)
  if not os.path.exists(os.path.join('xml', artNumber + '.xml')):
    try:
      data = plosOneQuery(artNumber)
      outxml = open(os.path.join('xml', artNumber + '.xml'), 'w')
      outxml.write(data)
      outxml.close()
    except urllib2.HTTPError:
      print artNumber + 'failed to download'
