#!/usr/bin/python

try:
  from urllib2 import urlopen, quote
  from urlparse import urlparse
except ImportError:
  from urllib.request import urlopen, quote, urlparse
from posixpath import basename
import sys
import re
import json

if(len(sys.argv)<3):
  print('usage: python ./dwc.py url file [filter] [-r]')
  exit()
recursive = (sys.argv.count('-r')>0)
filter = sys.argv[3] if (len(sys.argv)>3) else ""
limit = 500

catscomplete = {}
def dumpcat(cat):
  if(cat in catscomplete): return #to avoid an infinite recursion
  ecat = quote(cat)
  catinfo = json.loads(urlopen(host+"/w/api.php?format=json&action=query&prop=categoryinfo&titles="+ecat).read().decode("utf-8"))
  catsize = list(catinfo[u'query'][u'pages'].values())[0][u'categoryinfo'][u'size']
  print("\n"+cat+":\n")
  tail = ""
  processed = 0
  subcats = []
  while True:
    query = host+"/w/api.php?action=query&format=json&list=categorymembers&cmlimit="+str(limit)+"&cmtitle="+ecat+tail
    data = json.loads(urlopen(query).read().decode("utf-8"))
    pages = data[u'query'][u'categorymembers']
    for page in pages:
      title = page[u'title']
      if title.startswith(u'Category:'):
        subcats.append(title)
      elif not ( (filter != "") and (re.search(filter, title)) ):
        output.write((title+'\n').encode('utf8'))
    processed += len(pages)
    sys.stdout.write("\x1b[1A"+str(processed)+"/"+str(catsize)+"\n"),
    if(not (u'continue' in data)):
      break
    tail = '&cmcontinue='+data[u'continue'][u'cmcontinue']
  catscomplete[cat] = True
  if recursive:
    for subcat in subcats:
      dumpcat(subcat)

output = open(sys.argv[2],"wb")
url = urlparse(sys.argv[1])
host = url.scheme+"://"+url.netloc
dumpcat(basename(url.path))

if(output.tell()>0):
  output.seek(-1,1)
  output.truncate()
output.close()
