import os
import sys
import re

directory = sys.argv[1]

title_search = re.compile(r'(?:title:\s*)(?P<title>((\S*(\ )?)+)((\n(\ )+)(\S*(\ )?)*)*)', re.IGNORECASE | re.VERBOSE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)

keyword_search = dict.fromkeys([keyword for keyword in sys.argv[2:]], None)

for keyword in keyword_search:
  keyword_search[keyword] = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)

for file_name in os.listdir(directory):
    if file_name.endswith('.txt'):
        file_path = os.path.join(directory, file_name)

        with open(file_path, 'r') as f:
            full_text = f.read()

            title = re.search(title_search, full_text).group('title')
            author = re.search(author_search, full_text)
            translator = re.search(translator_search, full_text)
            if author:
                author = author.group('author')
            if translator:
                translator = translator.group('translator')

            print "File: {}".format(file_name)
            print "Title:  {}".format(title)
            print "Author(s): {}".format(author)
            print "Translator(s): {}".format(translator)
            print "\nKeyword counts for your search:"

            for keyword in keyword_search:
                print "\"{0}\": {1}".format(keyword, len(re.findall(keyword_search[keyword], full_text)))
            print "\n" + '-' * 50 + "\n"
