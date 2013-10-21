import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART

documents = [DIV_COMM, MAG_CART]

title_search = re.compile(r'(?:title:\s*)(?P<title>((\S*(\ )?)+)((\n(\ )+)(\S*(\ )?)*)*)', re.IGNORECASE | re.VERBOSE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)

keyword_search = dict.fromkeys([keyword for keyword in sys.argv[1:]], None)

for kw in keyword_search:
  keyword_search[keyword] = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)

for item,doc in enumerate(documents):
  title = re.search(title_search, doc).group('title')
  author = re.search(author_search, doc)
  translator = re.search(translator_search, doc)
  if author:
    author = author.group('author')
  if translator:
    translator = translator.group('translator')

  print "Here's the info for file {}:".format(item)
  print "The title of the text is:  {}".format(title)
  print "The author(s) is/are: {}".format(author)
  print "The translator(s) is/are: {}".format(translator)
  print "\nHere are the counts for the keywords you searched for:"

  for keyword in keyword_search:
    print "\"{0}\": {1}".format(keyword, len(re.findall(keyword_search[keyword], doc)))
  print "***" * 25
