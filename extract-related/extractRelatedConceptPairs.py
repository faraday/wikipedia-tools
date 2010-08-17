#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Jul 17, 2009
Prescanner with DB writes for ID-title, redirID mappings

Writes to DB as BLOBs.

@author: cagatay
'''

import sys
import re
import MySQLdb
import signal

from related import getRelatedPhrases

## handler for SIGTERM ###
def signalHandler(signum, frame):
    sys.exit(1)

signal.signal(signal.SIGTERM, signalHandler)
#####


rePageSt = re.compile('<page>')
rePageEnd = re.compile('</page>')
reTitle = re.compile('<title>(?P<title>.+)</title>')
reId = re.compile('<id>(?P<id>.+)</id>')
reText = re.compile('<text xml:space="preserve">(?P<text>.+)</text>',re.MULTILINE | re.DOTALL)

# regex as article filter (dates, wikipedia: etc.)
TR_re_strings = ['\d+ (Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)$','((MÖ|MS) )?\d+$','.+?_\(anlam_ayrımı\)$']
TR_piped_re = re.compile( "|".join( TR_re_strings ) , re.DOTALL|re.IGNORECASE)

# TR_reListe = re.compile('\[\[Kategori:((?:Listeler)|(?:.+ listeleri))',re.IGNORECASE|re.DOTALL)

# regex as article filter (dates, wikipedia: etc.)
EN_re_strings = ['(January|February|March|April|May|June|July|August|September|October|November|December) \d+$','\d+( (AD|BC))?$','.+?_\(disambiguation\)$','\d+ in .+$','List(?:s)? of .+$','Index of .+$']
EN_piped_re = re.compile( "|".join( EN_re_strings ) , re.DOTALL|re.IGNORECASE)


reRedirect = re.compile('\#REDIRECT',re.IGNORECASE)	# simpler.. 
#reRedirect = re.compile('\#REDIRECT\s*\[{2}(?P<link>.+?)\]{2}(\s*{{(?P<type>.+?)?}})?',re.IGNORECASE) # REDIRECT
#reRedirect = re.compile('\#REDIRECT \[{2}(?P<link>.+?)\]{2}',re.IGNORECASE) # REDIRECT

RSIZE = 10000000	# read chunk size = 10 MB

def recordArticle(page,language):
   try:
       title = reTitle.search(page).groups()[0]
   except:
       return	# false

   #ltitle = title.lower() 

   if title.find(':') != -1:
       return
       
   # filter articles based on title  
   if language == 'en' and EN_piped_re.match(title):
       return	# false

   elif language == 'tr' and TR_piped_re.match(title):
       return	# false

   try:
       id = reId.search(page).groups()[0]
       text = reText.search(page).groups()[0]
   except:
       return	# false

   firstLine = text.split('\n',1)[0]
   mredir = reRedirect.search(firstLine)
   if mredir:
	return

   try:
	# test if len(text) > 1000
	text[1001]
   except:
	return	# false

   #print id, title

   phrases = getRelatedPhrases(text,language)

   for p in phrases:
	print title + '\t' + p

   return	# true


args = sys.argv[1:]
# split.py <main_wiki_file> <RSIZE>

if len(args) < 2:
    print 'Usage: extractRelatedConceptPairs <main_wiki_file> <language>'
    sys.exit()

if len(args) == 3:
    RSIZE = int(args[2])

language = args[1]	# 'en' or 'tr'

f = open(args[0],'r')
prevText = ''

firstRead = f.read(10000)
documentStart = firstRead.find('</siteinfo>') + len('</siteinfo>')

prevText = firstRead[documentStart:10000]

while True:

    newText = f.read(RSIZE)
    if not newText:
        break
    
    text = prevText + newText

    rawpages = rePageSt.split(text)
    
    for page in rawpages[:-1]:
        recordArticle(page,language)

    # last page
    mend = rePageEnd.search(rawpages[-1])
    if not mend:
    	prevText = rawpages[-1]
    else:
    	endIndex = mend.end()
    	page = rawpages[-1]
    	recordArticle(page,language)
    	prevText = page[endIndex:]

f.close()

