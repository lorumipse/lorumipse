#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from builtins import range
import re
import os
import sys
import codecs
import random
from .basic_morphology import det
from .takdav_morphology import affix
from .phonmodel import create_model_from_file, generate_word

script_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.join(script_dir, "..", "resource")

NOUN_TRAINING = ['dt-noun-back.txt', 'dt-noun-front-round.txt', 'dt-noun-front-unround.txt']
ADJ_TRAINING = ['dt-adj-back.txt', 'dt-adj-front-round.txt', 'dt-adj-front-unround.txt']
VERB_TRAINING = ['dt-verb-back.txt', 'dt-verb-front-round.txt', 'dt-verb-front-unround.txt']

NON_CONTENT_NOUNS = [u"ez", u"minden", u"az", u"aki", u"amely", u"ami", u"más", u"egyik", u"saját", u"másik",
                     u"mely", u"semmi", u"senki",
                     u"bármely", u"bármi", u"bárki", u"ugyanaz", u"akárki", u"akármi", u"valaki", u"valami", u"ő", u"ők"]

KEPT_WORDS = [u'van', u'ez', u'az', u'kell', u'ő', u'sok', u'mi', u'amely', u'én', u'tud', u'aki', u'lehet', u'minden', u'ami',
'ki', u'olyan', u'ők', u'más', u'maga', u'mely', u'nincs', u'te', u'egyik', u'ilyen', u'való', u'fog', u'saját'] + NON_CONTENT_NOUNS


ARTICLE_SYMBOL = "#ART"

LORUM_IPSE_TOKENS = [("Lórum", "Lórum", "NOUN"), ("ipse", "ipse", "NOUN")]


def add_resouce_dir_prefix(filenames):
    return [os.path.join(resource_dir, filename) for filename in filenames]

noun_model = create_model_from_file(add_resouce_dir_prefix(NOUN_TRAINING))
adj_model = create_model_from_file(add_resouce_dir_prefix(ADJ_TRAINING))
verb_model = create_model_from_file(add_resouce_dir_prefix(VERB_TRAINING))


sentence_delimiter_re = re.compile(r'^# \d+$')

def read_sentence(file):
    tokens = []
    for line in file:
        stripped = line.strip()
        if sentence_delimiter_re.match(stripped):
            if tokens:
                yield tokens
                tokens = []
        else:
            fields = stripped.split("\t")
            if len(fields) != 3:
                sys.stderr.write(line)
                raise Exception(stripped)
            tokens.append(fields)
    if tokens:
        yield tokens
    

ana_re = re.compile(r'(^|.*/)([A-Z]+)([^/]*)$')
def parse_ana(ana):
    match = ana_re.match(ana)
    if match:
        return match.group(2), match.group(3)  # pos, inflection
    else:
        sys.stderr.write(ana)
        raise Exception(ana)


def gibberize_sentence(sentence, vocabulary_map=None):
    generated_sentence = [generate_word_from_token(word, lemma, ana, vocabulary_map) for word, lemma, ana in sentence]
    generated_sentence = correct_articles(generated_sentence)
    return generated_sentence


def gibberize_init_sentence(sentence):
    i = find_nom_np_end(sentence)
    gibberized = gibberize_sentence(sentence[i+1:])
    return LORUM_IPSE_TOKENS + gibberized


def find_nom_np_end(sentence):
    head_index = None
    for i, (word, lemma, ana) in enumerate(sentence):
        if ana == "NOUN" and lemma not in NON_CONTENT_NOUNS:
            head_index = i
            break
    return head_index


def generate_word_from_token(word, lemma, ana, vocabulary_map):
    pos, infl = parse_ana(ana)
    if pos in ["NOUN", "ADJ", "VERB"] and lemma not in KEPT_WORDS:
        if vocabulary_map is not None and (lemma, pos) in vocabulary_map:
            stem = vocabulary_map[(lemma, pos)]
            gen_word = affix(stem, pos + infl)
        else:
            stem, gen_word = generate_word_with_ana(pos, infl)
            if vocabulary_map is not None:
                vocabulary_map[(lemma, pos)] = stem
    elif lemma == "a" and ana == "ART":
        stem, gen_word = None, ARTICLE_SYMBOL
    else:
        stem, gen_word = lemma, word
    return gen_word, stem, ana


def generate_word_with_ana(pos, infl):
    if pos == "NOUN":
        stem = generate_word(noun_model)
    elif pos == "ADJ":
        stem = generate_word(adj_model)
    elif pos == "VERB":
        stem = generate_word(verb_model)
    word = affix(stem, pos + infl)
    return stem, word


def correct_articles(sentence):
    corrected_sentence = []
    for i in range(len(sentence)):
        word, lemma, ana = sentence[i]
        if word == ARTICLE_SYMBOL and i + 1 < len(sentence):
            next_word, _, _ = sentence[i+1]
            corrected_word = det(next_word)
        else:
            corrected_word = word
        corrected_sentence.append((corrected_word, lemma, ana))
    return corrected_sentence


def print_sentence(sentence):
    print(" ".join(sentence))


def gibberize_file(file):
    text = []
    vocabulary_map = {}
    for sentence in read_sentence(file):
        generated_sentence = gibberize_sentence(sentence, vocabulary_map)
        text.append(generated_sentence)
    return text


def gibberize_random_init_sentence_from_file(file):
    chosen_sentence = None
    for i, sentence in enumerate(read_sentence(file)):
        if chosen_sentence is None:
            chosen_sentence = sentence
        elif random.random() < 1/float(i+1):
            chosen_sentence = sentence
    return gibberize_init_sentence(chosen_sentence)


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    text = gibberize_file(sys.stdin)
    for sentence in text:
        print_sentence(sentence)

