#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

def read_sentence(file):
    sentence_id = 1
    tokens = []
    for line in file:
        stripped = line.strip()
        if stripped == "#":
            if tokens:
                yield sentence_id, tokens
                sentence_id += 1
                tokens = []
        else:
            fields = stripped.split("\t")
            if len(fields) != 3:
                sys.stderr.write(stripped)
                raise Exception(stripped)
            tokens.append(fields)
    if tokens:
        yield sentence_id, tokens


def write_sentence(sentence_id, tokens):
    print "# {id}".format(id=sentence_id)
    for token in tokens:
        print "\t".join(token)


verb_re = re.compile(r'^.*VERB[^[]*$')
verb_sg3_re = re.compile(r'^.*VERB(\+PREV.*)?$')
pers12_re = re.compile(r'^.*<PERS<[12]>')
noun_re = re.compile(r'^.*(NOUN|ADJ)[^[]*$')
noun_nom_acc_re = re.compile(r'^.*(NOUN|ADJ)(<CAS<ACC>>)?$')

def token_only_sg3_nom_acc(word, lemma, ana):
    return token_only_sg3(word, lemma, ana) and token_only_nom_acc(word, lemma, ana)


def token_only_sg3(word, lemma, ana):
    return not (verb_re.match(ana) and not verb_sg3_re.match(ana))

def token_no_pers12(word, lemma, ana):
    return not pers12_re.match(ana)

def token_only_nom_acc(word, lemma, ana):
    return not (noun_re.match(ana) and not noun_nom_acc_re.match(ana))
    

def only_sg3_nom_acc(tokens):
    for word, lemma, ana in tokens:
         if not token_only_sg3_nom_acc(word, lemma, ana):
             return False
    return True


def only_sg3(tokens):
    for word, lemma, ana in tokens:
        if not token_only_sg3(word, lemma, ana):
            return False
    return True

def no_pers12(tokens):
    for word, lemma, ana in tokens:
        if not token_no_pers12(word, lemma, ana):
            return False
    return True


def headline(tokens):
    words = [word for word, lemma, ana in tokens if ana != 'PUNCT']
    return len(words) <= 6


NON_CONTENT_NOUNS = [u"ez", u"minden", u"az", u"aki", u"amely", u"ami", u"más", u"egyik", u"saját", u"másik",
    u"mely", u"semmi", u"senki",
    u"bármely", u"bármi", u"bárki", u"ugyanaz", u"akárki", u"akármi", u"valaki", u"valami", u"ő", u"ők"]

def starts_with_nom_np(tokens):
    head_index = None
    sentence_start = tokens[:6]
    for i, (word, lemma, ana) in enumerate(sentence_start):
        if ana == "NOUN" and lemma not in NON_CONTENT_NOUNS:
            head_index = i
            break
    if head_index is None:
        return False
    for word, lemma, ana in sentence_start[:head_index]:
        if ana not in ["ART", "ADJ"]:
            return False
    return True


def choose(tokens):
    return not headline(tokens) and no_pers12(tokens)  #and only_sg3_nom_acc(tokens) and starts_with_nom_np(tokens)


for sentence_id, tokens in read_sentence(sys.stdin):
    if choose(tokens):
        write_sentence(sentence_id, tokens)
