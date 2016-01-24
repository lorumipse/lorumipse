#!/usr/bin/env python

from ngram import NGram
import sys
import itertools
import codecs
import random

DECOMPOSE_LONG_CHARS = True
MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 16

complex_chars = ["sz", "cs", "dz", "dzs", "gy", "ly", "ny", "ty", "zs"]
simple_consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z"]

complex_chars_encoding = {
    "sz": u"\u015B", # s'
    "zs": u"\u017E",  # z`'
    "cs": u"\u010D", # c`'
    "dz": u"\u1E0B", # d^.
    "dzs": u"\u010F", # d`'
    "gy": u"\u01F5", # g'
    "ly": u"\u013E", # l`'
    "ny": u"\u0148", # n with caron
    "ty": u"\u0165"  # t with caron
}

def decompose_long_chars(string):
    decomp_string = string
    decomp_string = decomp_string.replace(lc, decomp + decomp)
    
def encode_complex_chars(string):
    convstring = string
    for lc in long_complex_chars:
        decomp = long_complex_chars[1:]
        decomp_encoded = complex_chars_encoding[decomp]
        convstring = convstring.replace(lc, decomp_encoded + decomp_encoded)
    for orig, conv in complex_chars_encoding.iteritems():
        convstring = convstring.replace(orig, conv)
    return convstring

def decode_complex_chars(string):
    convstring = string
    for orig, conv in complex_chars_encoding.iteritems():
        convstring = convstring.replace(conv, orig)
    return convstring

def lengthen_letter(letter):
    if letter in complex_chars:
        return letter[0] + letter
    else:
        return letter + letter

def is_letter_at(string, pos, letter):
    return string[pos:pos+len(letter)] == letter

def identify_letter_at(string, pos):
    for compl in complex_chars:
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
    model = [(init_ngram(word_set), len(word_set)) for word_set in word_sets]
    return model


def create_model_from_file(word_files):
    word_sets = []
    for path in word_files:
        with codecs.open(path, 'r', 'utf-8') as f:
            words = read_words(f)
            word_sets.append(words)
    model = create_model(word_sets)
    return model


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"


def generate_word(model):
    ngram = weighted_choice(model)  # choose vowel harmony
    max_attempt = 10
    for w in ngram.generate_sequences(n_sequences=max_attempt):
       if len(w) >= MIN_WORD_LENGTH and len(w) <= MAX_WORD_LENGTH:
           return "".join(w)
    raise Exception("could not generate a word within length boundaries")


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
 

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    input_files = sys.argv[1:]

    if len(input_files) == 0:
        sys.stdin = codecs.getreader('utf-8')(sys.stdin)
        words = read_words(sys.stdin)
        model = create_model([words])
    else:
        model = create_model_from_file(input_files)

    for i in xrange(10000):
        print generate_word(model)
