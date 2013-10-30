import os
import sys
import re

# title = ''
# author = ''
# translator = ''

title_search = re.compile(r'(?:title:\s*)(?P<title>((\S*(\ )?)+)((\n(\ )+)(\S*(\ )?)*)*)', re.IGNORECASE | re.VERBOSE)

author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)

translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)

#meta_search_dictionary = {title: title_search, author: author_search, translator:translator_search}

meta_search_dictionary = dict(title = title_search, author = author_search, translator = translator_search)

#print meta_search_dictionary

# Iterating over and opening files
def file_opener(file_path):
    """Given a full path to a file, open the file and returns its contents"""
    with open(file_path, 'r') as f:
        return f.read()

def file_path_maker(directory, file_name):
    return os.path.join(directory, file_name)

# Compiling user supplied keywords into regular expressions
def keyword_pattern_maker(keyword_search):
    """Return dictionary of keyword regular expression patterns"""
    result = {}
    for keyword in keyword_search:
        result[keyword] = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)
    #print type(result)
    #result = {keyword: re.compile(r'\b' + keyword + r'\b') for keyword in keyword_search}
    #print result
    return result

# Counting keywords in a document
def keyword_counter(pattern, text):
    """Returns matches count for a keyword in a given text"""
    matches = re.findall(pattern, text)
    return len(matches)

# Stripping out metadata from Project Gutenberg documents
def meta_search(meta_search_dictionary, text):
    """Returns results of metadata search from text"""
    results = {}
    for meta in meta_search_dictionary:
        result = re.search(meta_search_dictionary[meta], text)
        if result:
            results[meta] = result.group(meta)
            #print results[meta]
        else:
            results[meta] = None
    #print results
    return results

def doc_tag_reporter(directory, keyword_search):
    """
    Iterates over a directory of Project Gutenberg documents
    Print title, author, translator, keyword counts
    """
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            file_path = file_path_maker(directory, file_name)
            text = file_opener(file_path)
            meta_searches = meta_search(meta_search_dictionary, text)
            keyword_searches = keyword_pattern_maker(keyword_search)

            print "File: {}".format(file_name)
            for meta in meta_searches:
                print "{0}: {1}".format(meta.capitalize(), meta_searches[meta])
            print "\nKeyword counts for your search:"
            for keyword in keyword_searches:
                print "\"{0}\": {1}".format(keyword, keyword_counter(keyword_searches[keyword], text))
            print "***" * 25

# main function that calls the other functions, supplying them with the necessary user supplied arguments at run time
def main():
    directory = sys.argv[1]
    keyword_search = []
    for keyword in sys.argv[2:]:
        keyword_search.append(keyword)
    #print type(keyword_search)
    #keyword_search = [keyword for keyword in sys.argv[2:]]
    doc_tag_reporter(directory, keyword_search)

if __name__ == '__main__':
    main()

