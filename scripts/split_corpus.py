#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

SENTENCES_IN_PART = 7

output_filename_prefix = sys.argv[1] if len(sys.argv) > 1 else "part"

sentence_delimiter_re = re.compile(r'^# \d+$')


def read_sentence(file):
    lines = []
    for line in file:
        stripped = line.strip()
        if sentence_delimiter_re.match(stripped):
            print "sentence", stripped
            if lines:
                yield lines
                lines = []
        lines.append(stripped)
    if lines:
        yield lines


def read_n_sentences(file, n):
    sentence_iter = read_sentence(file)
    sentences = []
    eof = False
    while not eof:
        for i in xrange(n):
            try:
                sentence = next(sentence_iter)
                sentences.append(sentence)
            except StopIteration:
                eof = True
                break
        if validate_sentences(sentences):
            yield sentences
        else:
            sys.stderr.write("omitting " + " ".join(map(lambda s: " ".join(s), sentences)) + "\n")
        sentences = []


def validate_sentences(sentences):
    # wrong tokenization of html entities
    for sentence in sentences:
        for i in xrange(len(sentence) - 3):
            if sentence[i].startswith("&\t") and sentence[i+1].startswith("#\t") and sentence[i+2].endswith("\tNUM"):
                return False
    # too many numbers
    num_numbers = len([token for sentence in sentences for token in sentence if token.endswith("\tNUM")])
    if num_numbers >= 10:
        return False
    return True


part_index = 0
for sentences in read_n_sentences(sys.stdin, SENTENCES_IN_PART):
    filename = output_filename_prefix + "{0:04d}".format(part_index)
    with codecs.open(filename, "w", "utf-8") as outf:
        for sentence in sentences:
            for line in sentence:
                outf.write(line + "\n")
    part_index += 1

