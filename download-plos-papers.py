#!/usr/bin/env python

#run this script at your own risk. i can't find anything about how many
# articles PLOS would like you to limit yourself to grabbing at once,
# but if they have a limit, this script will break it.

#http://www.plosone.org/article/fetchObjectAttachment.action?
# uri=info%3Adoi%2F10.1371%2Fjournal.pone.0075992&representation=XML

import sys  # always, pretty much
import string  # string handling
import urllib2  # url handling
import urllib  # url encoding
import socket  # for error catching
import os
import argparse
import bz2
import httplib

def plosOneQuery(articleNumber):
  dataDict = {
      'uri': 'info:doi/10.1371/journal.pone.' + articleNumber,
      'representation': 'XML'}
  articleEncode = urllib.urlencode(dataDict)
  request = urllib2.Request(
      url='http://www.plosone.org/article/fetchObjectAttachment.action', 
      data=articleEncode)
  result = urllib2.urlopen(request, timeout=5.0)  # timeout can be changed
  dataOut = result.read()
  return dataOut

try:
  os.mkdir('xml')
except OSError:   # directory exists
  pass  # which is fine
for number in xrange(100000):  # eventually raise once plos adds more papers
  artNumber = string.zfill(number, 7)   # hard coded 7 digit number, won't last
  if not os.path.exists(os.path.join('xml', artNumber + '.xml.bz2')):
    if not os.path.exists(os.path.join('xml', artNumber + '.xml')):
      try:
        data = plosOneQuery(artNumber)
        outxml = bz2.BZ2File(os.path.join('xml', artNumber + '.xml.bz2'), 'wb')
        outxml.write(data)
        outxml.close()
      except socket.timeout:
        print artNumber, 'timeout error'
      except socket.error:
        print artNumber, 'connection reset by peer error'
      except urllib2.HTTPError:
        print artNumber, 'failed to download'
      except urllib2.URLError:
        print artNumber, 'url open error'
      except httplib.BadStatusLine:
        print artNumber, ' bad status line'
