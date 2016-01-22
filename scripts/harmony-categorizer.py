#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import codecs

SUFFIXES = [u'en', u'an', u'ként', u'lag', u'leg', u'ul', u'ül']

front_unround_re = re.compile(ur"[eéíi][^aáeéiíoóuúőöűü]*$")
front_round_re = re.compile(ur"[öőüű][^aáeéiíoóuúőöűü]*$")
back_re = re.compile(ur"[aáoóuú][^aáeéiíoóuúőöűü]*$")

filename_prefix = sys.argv[1]

back_file = codecs.open(filename_prefix + '-back.txt', 'w', 'utf8')
front_round_file = codecs.open(filename_prefix + '-front-round.txt', 'w', 'utf8')
front_unround_file = codecs.open(filename_prefix + '-front-unround.txt', 'w', 'utf8')

def write_word(file, word):
    file.write(word + u"\n")

def add_to_back(word):
    write_word(back_file, word)

def add_to_front_round(word):
    write_word(front_round_file, word)

def add_to_front_unround(word):
    write_word(front_unround_file, word)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

for line in sys.stdin:
    word = line.strip()
    stem = word
    for suff in SUFFIXES:
        if word.endswith(suff):
            stem = word[:-len(suff)]
            break
    if back_re.search(stem):
        add_to_back(word)
    elif front_round_re.search(stem):
        add_to_front_round(word)
    elif front_unround_re.search(stem):
        add_to_front_unround(word)

for f in back_file, front_round_file, front_unround_file:
    f.close()
