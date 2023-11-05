#!/usr/bin/env python

from __future__ import print_function
import re
import sys
import codecs

history_window = 2

ana_pattern = r'/((NOUN|VERB|ADJ).*)$'
ana_re = re.compile(ana_pattern)
prev_pattern = r'/(PREV)\+'
prev_re = re.compile(prev_pattern)
pron_pattern = ur'^\u0151/NOUN'
pron_re = re.compile(prev_pattern)
pers12_pattern = r'(PERS|POSS)<[12]'
pers12_re = re.compile(pers12_pattern)

def convert_token(line):
    stripped = line.strip()
    if stripped == "":
        return "#"
    else:
        if "\t" not in stripped:
            return None
        (form, annot) = stripped.split('\t', 2)
        if not is_token_enabled(form, annot):
            return None
        if pron_re.search(annot):
            return form
        ana_match = ana_re.search(annot)
        if ana_match:
            if ana_match.group(2) == "VERB":
                if prev_re.search(annot):
                    return "/PREV+" + ana_match.group(1)
            return "/" + ana_match.group(1)
        elif annot == 'a/ART':
            return form + "/ART"
        else:
            return form

def is_token_enabled(form, annot):
    # digits? brackets?
    # end of sentence without punct?
    if pers12_re.search(annot):
        return False
    return True

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
history = ()

skip_next = 0
for line in sys.stdin:
    if skip_next == 0:
        token = convert_token(line)
        if token is None:
            skip_next = history_window
        else:
            print(token)
    else:
        skip_next -= 1
