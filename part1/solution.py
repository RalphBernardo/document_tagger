import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART

documents = [DIV_COMM, MAG_CART]

title_search = re.compile(r'(?:title:\s*)(?P<title>((\S*(\ )?)+)((\n(\ )+)(\S*(\ )?)*)*)', re.IGNORECASE | re.VERBOSE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)

kws = dict.fromkeys([kw for kw in sys.argv[1:]], None)

for kw in kws:
  kws[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)

for i,doc in enumerate(documents):
  title = re.search(title_search, doc).group('title')
  author = re.search(author_search, doc)
  translator = re.search(translator_search, doc)
  if author:
    author = author.group('author')
  if translator:
    translator = translator.group('translator')

  print "\nHere's the info for file {}:".format(i)
  print "***" * 25
  print "The title of the text is:  {}".format(title)
  print "The author(s) is/are: {}".format(author)
  print "The translator(s) is/are: {}".format(translator)
  print "\nHere are the counts for the keywords you searched for:\n"

  for kw in kws:
    print "\"{0}\": {1}".format(kw, len(re.findall(kws[kw], doc)))
  print "***" * 25
