# -*- coding: utf-8 -*-

import anchorParse
import re

# regex as article filter (dates, wikipedia: etc.)
TR_re_strings = ['\d+ (Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)$','((MÖ|MS) )?\d+$','.+? \(anlam ayrım(?:ı)?\)$']
TR_piped_re = re.compile( "|".join( TR_re_strings ) , re.DOTALL|re.IGNORECASE)

# TR_reListe = re.compile('\[\[Kategori:((?:Listeler)|(?:.+ listeleri))',re.IGNORECASE|re.DOTALL)

# regex as article filter (dates, wikipedia: etc.)
EN_re_strings = ['(January|February|March|April|May|June|July|August|September|October|November|December) \d+$','\d+( (AD|BC))?$','.+? \(disambiguation\)$','\d+ in .+$','List(?:s)? of .+$','Index of .+$']
EN_piped_re = re.compile( "|".join( EN_re_strings ) , re.DOTALL|re.IGNORECASE)


TR_reSeeAlso = re.compile('==\s*(?:Ayrıca bakınız)\s*==([^=]+)?',re.DOTALL|re.MULTILINE|re.IGNORECASE)
TR_reRelatedTemplate = re.compile('\{\{\s*(?:Bakınız)\s*\|([^}]+)?',re.DOTALL|re.MULTILINE|re.IGNORECASE)

EN_reSeeAlso = re.compile('==\s*(?:(?:See also)|(?:Related pages))\s*==([^=]+)?',re.DOTALL|re.MULTILINE|re.IGNORECASE)
EN_reRelatedTemplate = re.compile('\{\{\s*(?:(?:Related articles)|(?:See also))\s*\|([^}]+)?',re.DOTALL|re.MULTILINE|re.IGNORECASE)

# '{{Related articles|Anarchist terminology}}'
# '{{See also|anarchism in Italy|anarchism in France|anarchism in Spain}}'

def getRelatedPhrases(wtext,language):
	related_phrases = []

	if language == 'en':
		sections = EN_reSeeAlso.findall(wtext)
		templates = EN_reRelatedTemplate.findall(wtext)
	elif language == 'tr':
		sections = TR_reSeeAlso.findall(wtext)
		templates = TR_reRelatedTemplate.findall(wtext)

	for s in templates:
		for sk in s.split('|'):
			if sk.find(':') != -1:	continue
			if language == 'en' and EN_piped_re.match(sk): continue
			elif language == 'tr' and TR_piped_re.match(sk): continue
			related_phrases.append(sk)	

	related_text = ''
	for s in sections:
		related_text += s

	if not related_text:
		return related_phrases

	ls = anchorParse.getLinks(related_text)
	for l in ls:
		if l.find(':') != -1:	continue
		l = l.replace('_',' ')
		if language == 'en' and EN_piped_re.match(l): continue
		elif language == 'tr' and TR_piped_re.match(l): continue
		related_phrases.append(l)

	return related_phrases	

