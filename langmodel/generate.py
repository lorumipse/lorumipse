#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import
import os
import random
import sys
import codecs
import json
import logging
from .gibberize import gibberize_file, gibberize_random_init_sentence_from_file


INIT_TEMPLATE_FILENAME = "init.txt"
logger = logging.getLogger("langmodel")

_template_files = None
_template_dir = None


def init(template_dir):
    global _template_dir
    _template_dir = template_dir
    global _template_files
    _template_files = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if f != INIT_TEMPLATE_FILENAME]


def choose_random_template():
    path = random.choice(_template_files)
    return path


def gibberize_random_template():
    logger.debug("gibberize_random_template start")
    template = choose_random_template()
    logger.debug("chosen template")
    with codecs.open(template, 'r', 'utf-8') as f:
        sentences = gibberize_file(f)
        logger.debug("gibberized template")
        sentences = [add_spacing(capitalize_sentence(sentence)) for sentence in sentences]
        logger.debug("result completed")
        return sentences


def generate_init_sentence():
    init_file_path = os.path.join(_template_dir, INIT_TEMPLATE_FILENAME)
    with codecs.open(init_file_path, 'r', 'utf-8') as f:
        init_sentence = gibberize_random_init_sentence_from_file(f)
    formatted = add_spacing(capitalize_sentence(init_sentence))
    return formatted


def generate_text(init):
    sentences = []
    if init:
        init_sentence = generate_init_sentence()
        sentences.append(init_sentence)
    sentences += gibberize_random_template()
    text = json.dumps(sentences)
    return text


def add_spacing(sentence):

    def starts_with_any(str, prefixes):
        return any([str.startswith(pref) for pref in prefixes])

    sentence_with_spacing = []
    quote_open = False
    for word, lemma, ana in sentence:
        result_word = word
        no_space = None
        if ana == "PUNCT":
            if word in [":", ")", "]", "}"] or starts_with_any(word, [".", ",", "!", "?"]):
                no_space = "left"
            elif word in ["(", "[", "{"]:
                no_space = "right"
            elif word == '"':
                if quote_open:
                    no_space = "left"
                    result_word = u"\u201d"
                    quote_open = False
                else:
                    no_space = "right"
                    result_word = u"\u201e"
                    quote_open = True
            elif word in ["&ldquo;", "&raquo;", "&bdquo;"]:
                no_space = "right"
            elif word in ["&rdquo;", "&laquo;"]:
                no_space = "left"
        sentence_with_spacing.append((result_word, lemma, ana, no_space))
    return sentence_with_spacing


def capitalize_sentence(sentence):
    capitalized = []
    if len(sentence) > 0:
        word, lemma, ana = sentence[0]
        capitalized.append((word[0].upper() + word[1:], lemma, ana))
    capitalized += sentence[1:]
    return capitalized


if __name__ == '__main__':
    _template_dir = sys.argv[1]
    print(generate_text(_template_dir))
