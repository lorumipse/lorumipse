#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import re
from collections import defaultdict

def read_corpus(file):
    converter = TokenConverter()
    for sentence in read_sentences(file):
        converted_sentence = [converter.convert_token(token) for token in sentence]
        print " ".join([form if form else str(lemma) + "/" + morph for form, lemma, morph in converted_sentence])


def read_sentences(file):
    sentence = []
    for token in read_tokens(file):
        if token:
            sentence.append(token)
        else:
            yield sentence
            sentence = []


prev_re = re.compile(r"([^/]+)/PREV\+([^/]+)/(VERB.*)")
ana_re = re.compile(r"(.+?)/([A-Z].*)")

def read_tokens(file):
    for line in file:
        stripped = line.rstrip()
        if stripped == "":
            yield None
        else:
            try:
                form, ana = stripped.split("\t")
                if ana == "UNKNOWN":
                    yield form, form, ana
                else:
                    ana = clean_ana(form, ana)
                    prev_match = prev_re.match(ana)
                    if prev_match:
                        yield form, prev_match.group(2), \
                            u"{ana}+PREV({prev})".format(prev=prev_match.group(1), ana=prev_match.group(3))
                    else:
                        ana_match = ana_re.match(ana)
                        lemma, morph = ana_match.group(1), ana_match.group(2)
                        yield form, lemma, morph
            except:
                sys.stderr.write(line)
                raise


question_noun_re = re.compile(r"(.*)\?NOUN")
def clean_ana(form, ana):
    if ana == "/+?NOUN":
        return "+/PUNCT"
    elif form == "|" and ana == "/NOUN":
        return "|/PUNCT"
    elif question_noun_re.match(ana):
        return form + "/NOUN"
    else:
        return ana


class TokenConverter(object):

    NON_CONTENT_NOUNS = [u"ez", u"minden", u"az", u"aki", u"amely", u"ami", u"más", u"egyik", u"saját", u"másik",
        u"mely", u"semmi", u"senki",
        u"bármely", u"bármi", u"bárki", u"ugyanaz", u"akárki", u"akármi", u"valaki", u"valami", u"ő", u"ők"]
    pos_re = re.compile(r"([A-Z]+)")

    def __init__(self):
        self.lexicon_mapping = defaultdict(lambda: self.get_next_id())
        self.next_id = 0

    def get_next_id(self):
        next = self.next_id
        self.next_id += 1
        return next

    @staticmethod
    def get_pos(morph):
       match = TokenConverter.pos_re.match(morph)
       if match:
           return match.group(1)
       else:
           raise ValueError(morph)

    def convert_token(self, token):
        """
        Replaces content lexemes by id numbers
        token : (form, lemma, morph) tuple
        """

        if self.content_token(token):
            form, lemma, morph = token
            lex_key = "_".join((lemma, self.get_pos(morph)))
            lex_id = self.lexicon_mapping[lex_key]
            return None, lex_id, morph
        else:
            return token

    @staticmethod
    def content_token(token):
        form, lemma, morph = token
        pos = TokenConverter.get_pos(morph)
        return pos in (u"ADJ", u"NOUN", u"VERB") and lemma not in TokenConverter.NON_CONTENT_NOUNS
        

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

read_corpus(sys.stdin)
