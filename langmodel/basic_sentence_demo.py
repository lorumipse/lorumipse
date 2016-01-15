#!/usr/bin/env python

import os
from morphology import affix, det
from phonmodel import create_model_from_file, generate_word

script_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.join(script_dir, "..", "resource")

NOUN_TRAINING = ['elekfi-nounstems-A.txt', 'elekfi-nounstems-B.txt', 'elekfi-nounstems-C.txt']
ADJ_TRAINING = ['elekfi-adjstems-A.txt', 'elekfi-adjstems-B.txt', 'elekfi-adjstems-C.txt']
VERB_TRAINING = ['elekfi-verbstems-a.txt', 'elekfi-verbstems-b.txt', 'elekfi-verbstems-c.txt']

def add_resouce_dir_prefix(filenames):
    return [os.path.join(resource_dir, filename) for filename in filenames]

noun_model = create_model_from_file(add_resouce_dir_prefix(NOUN_TRAINING))
adj_model = create_model_from_file(add_resouce_dir_prefix(ADJ_TRAINING))
verb_model = create_model_from_file(add_resouce_dir_prefix(VERB_TRAINING))


def generate_sentence():
    subj_stem = generate_word(noun_model)
    subj = affix(subj_stem, "NOUN")
    subj_det = det(subj)
    verb_stem = generate_word(verb_model)
    verb = affix(verb_stem, "VERB")
    adj_stem = generate_word(adj_model)
    adj = affix(adj_stem, "ADJ")
    obj_stem = generate_word(noun_model)
    obj = affix(obj_stem, "NOUN<ACC>")
    return [subj_det, subj, verb, u"egy", adj, obj]


for i in xrange(1000):
    print " ".join(generate_sentence())
