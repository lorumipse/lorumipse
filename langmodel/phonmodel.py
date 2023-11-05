#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import
from builtins import range
from builtins import object
from .ngram import NGram
import sys
import codecs
import random
from collections import defaultdict

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 16
GENERATING_CONSTRAINTS_ATTEMPT_LIMIT = 100

complex_consontants = ["sz", "cs", "dz", "dzs", "gy", "ly", "ny", "ty", "zs"]
simple_consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z"]


def lengthen_letter(letter):
    if letter in complex_consontants:
        return letter[0] + letter
    else:
        return letter + letter


def is_letter_at(string, pos, letter):
    return string[pos:pos+len(letter)] == letter


def identify_letter_at(string, pos):
    for compl in complex_consontants:
        long = lengthen_letter(compl)
        if is_letter_at(string, pos, long):
            return long
        elif is_letter_at(string, pos, compl):
            return compl
    long = lengthen_letter(string[pos])
    if is_letter_at(string, pos, long):
        return long
    else:
        return string[pos]


def split_letters(string):
    letters = []
    i = 0
    while i < len(string):
        letter = identify_letter_at(string, i)
        letters.append(letter)
        i += len(letter)
    return letters


def create_model(word_sets):
    model = [(init_ngram(word_set), len(word_set), CVConstraint(word_set)) for word_set in word_sets]
    return model


def create_model_from_file(word_files):
    word_sets = []
    for path in word_files:
        with codecs.open(path, 'r', 'utf-8') as f:
            words = read_words(f)
            word_sets.append(words)
    model = create_model(word_sets)
    return model


def choose_submodel(submodels):
    total = sum(w for ngram, w, constraint in submodels)
    r = random.uniform(0, total)
    upto = 0
    for submodel in submodels:
        w = submodel[1]
        if upto + w >= r:
            return submodel
        upto += w
    assert False, "Shouldn't get here"


def generate_word(model):
    ngram, weight, cv_constraint = choose_submodel(model)  # choose vowel harmony
    candidates = list(ngram.generate_sequences(n_sequences=GENERATING_CONSTRAINTS_ATTEMPT_LIMIT))
    for w in candidates:
        if len(w) >= MIN_WORD_LENGTH and len(w) <= MAX_WORD_LENGTH:
            word = "".join(w)
            valid = cv_constraint.is_valid(word)
            if valid:
                return word
    raise Exception("could not generate a word within constraints")


def init_ngram(training_words):
    words = []
    for word in training_words:
        words.append(list(split_letters(word)))
    ngram = NGram(3, words)
    return ngram


def read_words(file):
    words = []
    for line in file:
        words.append(line.strip())
    return words


class CVConstraint(object):
    def __init__(self, word_set, validity_abs_freq_threshold=1):
        self.validity_abs_freq_threshold = validity_abs_freq_threshold
        self.c_skel_freq = defaultdict(int)
        for word in word_set:
            c_skel = CVConstraint.get_c_skel(word)
            self.c_skel_freq[c_skel] += 1

    @staticmethod
    def get_c_skel(word):
        letters = split_letters(word)
        return "".join(["c" if CVConstraint.is_consonant(letter) else letter for letter in letters])

    @staticmethod
    def is_consonant(letter):
        return letter in complex_consontants + simple_consonants

    def is_valid(self, word):
        c_skel = self.get_c_skel(word)
        freq = self.c_skel_freq.get(c_skel, 0)
        return freq >= self.validity_abs_freq_threshold


if __name__ == "__main__":
    input_files = sys.argv[1:]

    if len(input_files) == 0:
        words = read_words(sys.stdin)
        model = create_model([words])
    else:
        model = create_model_from_file(input_files)

    for i in range(10000):
        print(generate_word(model))
