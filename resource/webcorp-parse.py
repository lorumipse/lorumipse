#!/usr/bin/env python

import re
import sys
import codecs


ana_pattern = r'([^/]*)/([A-Z].*)$'
ana_re = re.compile(ana_pattern)
prev_pattern = r'([^/]*)/PREV\+(.*)/(VERB.*)'
prev_re = re.compile(prev_pattern)
punct_re = re.compile(r'^[?! ]+$')


def convert_token(line):
    stripped = line.strip()
    if stripped == "":
        return "EOS",
    else:
        if "\t" not in stripped:
            return stripped, stripped, "INVALID"
        (form, annot) = stripped.split('\t', 2)
        prev_match = prev_re.match(annot)
        if prev_match:
            return form, prev_match.group(1) + "+" + prev_match.group(2), prev_match.group(3) + "+PREV(" + prev_match.group(1) + ")"
        ana_match = ana_re.search(annot)
        if ana_match:
            return form, ana_match.group(1), ana_match.group(2)
        if annot == "UNKNOWN":
            return form, form, "UNKNOWN"
        if form == "+" and annot == "/+?NOUN":
            return "+", "+", "PUNCT"
        if punct_re.match(form) and annot.endswith("?NOUN"):
            return form, form, "PUNCT"
        return form, form, "INVALID"


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

for line in sys.stdin:
    fields = convert_token(line)
    if fields[0] == "EOS":
        print "#"
    else:
        print "\t".join(fields)
