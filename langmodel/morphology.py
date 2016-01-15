# coding: utf-8

import re
import simplejson as json
import unittest
from elekfi import Elekfi, Szo
from grammar import Phonology, Wordform1

elek = Elekfi()
elek.load()
# todo legyen dinamikus a resource betoltes itt is
phon2elek = json.loads(open('../resource/phon2elek.json').read())

def hasonlo(phon):
    if 'A' in phon or 'v' in phon or 'b' in phon:
        return phon[:5] + "---" + phon[8:]
    if '@' in phon:
        return phon.replace('@', '~')
    return phon

def gen_szo(stem, szofaj):
    # todo ez az okossag menjen mashova
    w = Wordform1(stem)
    if w.isLastVowel():
        w.is_amny = True
        w.is_alternating = True
        stem2 = Phonology.doAMNY(w.ortho)
    else:
        stem2 = stem
    phon = w.attribstr()
    for ph in [phon, hasonlo(phon), hasonlo(hasonlo(phon))]:
        if ph in phon2elek[szofaj]:
            paradigma = phon2elek[szofaj][ph][0][1]
    return Szo(stem, szofaj, {'~': stem, '@': stem2}, paradigma)

def affix(stem, ana):
    if ana.startswith("NOUN"):
        szo = gen_szo(stem, 'FN')
        if ana == "NOUN":
            return elek.gen(szo, 'ACC')
        if ana == "NOUN<ACC>":
            return elek.gen(szo, 'ACC')
    elif ana.startswith("VERB"):
        szo = gen_szo(stem, 'IG')
        if ana == "VERB<PERS<2>><PLUR><DEF>":
            return elek.gen(szo, 'Tt2')
        return elek.gen(szo, 'e3')
    elif ana.startswith("ADJ"):
        return stem
    else:
        print "??", (stem, ana)
    return stem


def det(word):
    if re.match(ur"^[aáeéiíoóöőuúüű]", word.lower()):
        return u"az"
    else:
        return u"a"


class TestMorphology(unittest.TestCase):

    def test_affix(self):
        self.assertEqual(u'futurt', affix(u'futur', 'NOUN<ACC>'))
        self.assertEqual(u'vizecskét', affix(u'vizecske', 'NOUN<ACC>'))
        self.assertEqual(u'tapáljátok', affix(u'tapál', 'VERB<PERS<2>><PLUR><DEF>'))
