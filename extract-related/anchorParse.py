# -*- coding: utf-8 -*-
'''
Created on Jul 23, 2009

@author: cagatay
'''

import re
from htmlentitydefs import name2codepoint as n2cp


# modified for finding only anchors
reLink = re.compile('\[\[([^\]\[]+?)(?:\|([^\[\]]+?))?\]\]',re.DOTALL)


#text = htmldecode(wikitext).replace('&nbsp;',u' ').replace('&mdash;',u'—').replace('&ndash;',u'—')
#reSymbol = re.compile('(&(?:(?:nbsp;)|(?:mdash;)|(?:ndash;)))')
reSymbol = re.compile('((?:&nbsp;)|(?:&mdash;)|(?:&ndash;))')

symbolDict = {'&nbsp;': u' ',
		'&mdash;': u'—',
		'&ndash;': u'—'}

def repl(matchobj):
	al = matchobj.groups()[0]
	return symbolDict[al]

def replURL(matchobj):
	al = matchobj.groups()[0]
	if al:
		return al
	return ''

def htmldecode(s):
	return re.sub('&(%s);' % '|'.join(n2cp), lambda m: unichr(n2cp[m.group(1)]), s)


def getLinks(s):
	links = []
	ls = reLink.findall(s)
	for l in ls:
		if l[0].find(':') != -1:
			continue
		lk = l[0].split('#',1)[0].strip().replace(' ','_')
		if not lk:
			continue
		lk = lk[0].capitalize() + lk[1:]
		if l[1]:
			anchor = l[1]
		else:
			anchor = lk

		anchor = htmldecode(anchor)

		if len(lk) <= 255 and len(anchor) <= 255:
			#links.append((lk,anchor))
			links.append(lk)
	return links
