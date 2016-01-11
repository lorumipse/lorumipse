#!/usr/bin/env python

import os
import random
import sys
import codecs
import json
from gibberize import gibberize_file


def choose_random_file(dir):
    files = os.listdir(dir)
    file = random.choice(files)
    return os.path.join(dir, file)


def generate_text(dir):
    template = choose_random_file(dir)
    with codecs.open(template, 'r', 'utf-8') as f:
        sentences = gibberize_file(f)
        sentences = [add_spacing(capitalize_sentence(sentence)) for sentence in sentences]
        text = json.dumps(sentences)
        return text


def add_spacing(sentence):

    def starts_with_any(str, prefixes):
        return any([str.startswith(pref) for pref in prefixes])

    sentence_with_spacing = []
    for word, lemma, ana in sentence:
        no_space = None
        if ana == "PUNCT":
            if word in [":", ")", "]", "}"] or starts_with_any(word, [".", ",", "!", "?"]):
                no_space = "left"
            elif word in ["(", "[", "{"]:
                no_space = "right"
        sentence_with_spacing.append((word, lemma, ana, no_space))
    return sentence_with_spacing


def capitalize_sentence(sentence):
    capitalized = []
    if len(sentence) > 0:
        word, lemma, ana = sentence[0]
        capitalized.append((word[0].upper() + word[1:], lemma, ana))
    capitalized += sentence[1:]
    return capitalized


if __name__ == '__main__':
    template_dir = sys.argv[1]
    print generate_text(template_dir)
