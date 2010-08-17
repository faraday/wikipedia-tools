Related Pair Extractor

Scans Wikipedia article dump (XML), finds links from "See also", 
"Related pages" sections, "Related articles" templates etc.
and creates a CSV file using every article title and these related anchors.

Sample usage:

ENGLISH

python extractRelatedConceptPairs.py ~/Data/enwiki/20090618/operate/enwiki-20090618-pages-articles.xml en > ~/Data/enwiki/20090618/operate/enwiki_related_pairs.csv
