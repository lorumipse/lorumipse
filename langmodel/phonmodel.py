#!/usr/bin/env python

from ngram import NGram
import sys
import itertools
import codecs

DECOMPOSE_LONG_CHARS = True

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


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

text = ['#']
for line in sys.stdin:
    text += list(split_letters(line.strip()))
    text.append('#')

ngram = NGram(3, text)

for seq in ngram.generate_sequences(length=100, sep='#'):
    print "".join(seq)
