#!/usr/bin/env python

#http://www.plosone.org/article/fetchObjectAttachment.action?
# uri=info%3Adoi%2F10.1371%2Fjournal.pone.0075992&representation=XML

import sys  # always, pretty much
import string  # string handling
import urllib2  # url handling
import urllib  # url encoding
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

data = plosOneQuery('0075992')
print data
