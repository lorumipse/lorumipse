# coding: utf-8

from scratch import GFactory, PossessiveSuffixum, PossessorSuffixum
import re

def affix(stem, ana):

    if ana.startswith('NOUN') or ana.startswith('ADJ'):
        if ana.startswith('NOUN'):
            w = GFactory.parseNP(stem)
            ana = 'X' + ana[4:]
        elif ana.startswith('ADJ'):
            w = GFactory.parseADJ(stem)
            ana = 'X' + ana[3:]
        if 'X<PLUR>' in ana and not 'X<PLUR><POSS' in ana: w = w.makePlural()
        if 'X<PLUR<FAM>>' in ana: w = w.makePlural(familiar=True)
        if 'X<PLUR><POSS>' in ana: w = w.appendSuffix(PossessiveSuffixum(1, 3, 3))
        if 'X<PLUR><POSS<PLUR><1>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 1, 3))
        if 'X<PLUR><POSS<PLUR><2>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 2, 3))
        if 'X<PLUR><POSS<PLUR>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 3, 3))
        if 'X<POSS>' in ana: w = w.appendSuffix(PossessiveSuffixum(1, 3, 1))
        if 'X<POSS<PLUR><1>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 1, 1))
        if 'X<POSS<PLUR><2>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 2, 1))
        if 'X<POSS<PLUR>>' in ana: w = w.appendSuffix(PossessiveSuffixum(3, 3, 1))
        if '<ANP>' in ana: w = w.appendSuffix(PossessorSuffixum(1))
        if '<ANP<PLUR>>' in ana: w = w.appendSuffix(PossessorSuffixum(3))
        if '<CAS<ACC>>' in ana: w = w.makeAccusativus()
        if '<CAS<DAT>>' in ana: w = w.makeDativus()
        if '<CAS<DEL>>' in ana: w = w.makeDelativus()
        if '<CAS<ELA>>' in ana: w = w.makeElativus()
        if '<CAS<ABL>>' in ana: w = w.makeAblativus()
        if '<CAS<SUE>>' in ana: w = w.makeSuperessivus()
        if '<CAS<INE>>' in ana: w = w.makeInessivus()
        if '<CAS<ADE>>' in ana: w = w.makeAdessivus()
        if '<CAS<SBL>>' in ana: w = w.makeSublativus()
        if '<CAS<ILL>>' in ana: w = w.makeIllativus()
        if '<CAS<ALL>>' in ana: w = w.makeAllativus()
        if '<CAS<TER>>' in ana: w = w.makeTerminativus()
        if '<CAS<INS>>' in ana: w = w.makeInstrumentalis()
        if '<CAS<CAU>>' in ana: w = w.makeCausalisFinalis()
        if '<CAS<FOR>>' in ana: w = w.makeFormativus()
        if '<CAS<TRA>>' in ana: w = w.makeTranslativusFactivus()
        if '<CAS<TEM>>' in ana: w = w.makeTemporalis()
        return w.ortho

    elif ana.startswith('VERB'):
        w = GFactory.parseV(stem)
        if '<MODAL>' in ana:
            w = w.makeModal()
        tense = 0
        if '<PAST>' in ana:
            tense = -1
        numero = 1
        if '<PLUR>' in ana:
            numero = 3
        definite = 0
        person = 3
        if '<DEF>' in ana:
            definite = 3
        if '<PERS<1>>' in ana:
            person = 1
        elif '<PERS<1<OBJ2>>>' in ana:
            person = 1
            definite = 2
        elif '<PERS<2>>' in ana:
            person = 2
        mood = 1
        if '<COND>' in ana:
            mood = 2
        elif '<SUBJUNC-IMP>' in ana:
            mood = 3
        if '<INF>' in ana:
            return w.makeInfinitive(numero, person).ortho
        else:
            return w.conjugate(numero, person, mood, tense, definite).ortho

    return stem


import unittest


class TestMorphology(unittest.TestCase):

    def test_affix(self):
        self.assertEqual(u'tapáljátok', affix(u'tapál', 'VERB<PERS<2>><PLUR><DEF>'))
        self.assertEqual(u'tapáltok', affix(u'tapál', 'VERB<PERS<2>><PLUR>'))
        self.assertEqual(u'tapállak', affix(u'tapál', 'VERB<PERS<1<OBJ2>>>'))

        self.assertEqual(u'futuroknak', affix(u'futur', 'NOUN<PLUR><CAS<DAT>>'))
        self.assertEqual(u'futurt', affix(u'futur', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'vizecskét', affix(u'vizecske', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'anatot', affix(u'anat', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'idülelcsit', affix(u'idülelcsi', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'számeiséget', affix(u'számeiség', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'hátlatikukanipolyát', affix(u'hátlatikukanipolya', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'bangót', affix(u'bangó', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'reklojátumust', affix(u'reklojátumus', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'érmelletet', affix(u'érmellet', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'kasztát', affix(u'kaszta', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'ejtőt', affix(u'ejtő', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'ijedeliletinimberherűségeszténét', affix(u'ijedeliletinimberherűségeszténe', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'tát', affix(u'ta', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'likforanosztást', affix(u'likforanosztás', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'karhalicskát', affix(u'karhalicska', 'NOUN<CAS<ACC>>'))

        self.assertEqual(u'fiú', affix(u'fiú', 'NOUN')) # nominativus
        self.assertEqual(u'fiút', affix(u'fiú', 'NOUN<CAS<ACC>>')) # accusativus
        self.assertEqual(u'fiúnak', affix(u'fiú', 'NOUN<CAS<DAT>>')) # dativus
        self.assertEqual(u'fiúról', affix(u'fiú', 'NOUN<CAS<DEL>>')) # delativus
        self.assertEqual(u'fiúból', affix(u'fiú', 'NOUN<CAS<ELA>>')) # elativus
        self.assertEqual(u'fiútól', affix(u'fiú', 'NOUN<CAS<ABL>>')) # ablativus
        self.assertEqual(u'fiún', affix(u'fiú', 'NOUN<CAS<SUE>>')) # superessivus
        self.assertEqual(u'fiúban', affix(u'fiú', 'NOUN<CAS<INE>>')) # inessivus
        self.assertEqual(u'fiúnál', affix(u'fiú', 'NOUN<CAS<ADE>>')) # adessivus
        self.assertEqual(u'fiúra', affix(u'fiú', 'NOUN<CAS<SBL>>')) # sublativus
        self.assertEqual(u'fiúba', affix(u'fiú', 'NOUN<CAS<ILL>>')) # illativus
        self.assertEqual(u'fiúhoz', affix(u'fiú', 'NOUN<CAS<ALL>>')) # allativus
        self.assertEqual(u'fiúig', affix(u'fiú', 'NOUN<CAS<TER>>')) # terminativus
        self.assertEqual(u'fiúval', affix(u'fiú', 'NOUN<CAS<INS>>')) # instrumentalis-comitativus
        self.assertEqual(u'fiúért', affix(u'fiú', 'NOUN<CAS<CAU>>')) # causalis-finalis
        self.assertEqual(u'fiúként', affix(u'fiú', 'NOUN<CAS<FOR>>')) # formativus
        self.assertEqual(u'fiúvá', affix(u'fiú', 'NOUN<CAS<TRA>>')) # translativus-factivus
        self.assertEqual(u'húsvétkor', affix(u'húsvét', 'NOUN<CAS<TEM>>')) # temporalis

        self.assertEqual(u'fiúé', affix(u'fiú', 'NOUN<ANP>'))
        self.assertEqual(u'fiúké', affix(u'fiú', 'NOUN<PLUR><ANP>'))
        self.assertEqual(u'fiúéi', affix(u'fiú', 'NOUN<ANP<PLUR>>'))
        self.assertEqual(u'fiúkéi', affix(u'fiú', 'NOUN<PLUR><ANP<PLUR>>'))
        self.assertEqual(u'házakéi', affix(u'ház', 'NOUN<PLUR><ANP<PLUR>>'))
        self.assertEqual(u'fia', affix(u'fia', 'NOUN<POSS>'))
        self.assertEqual(u'fiáéi', affix(u'fia', 'NOUN<POSS><ANP<PLUR>>'))
        self.assertEqual(u'házáéi', affix(u'ház', 'NOUN<POSS><ANP<PLUR>>'))
        self.assertEqual(u'háza', affix(u'ház', 'NOUN<POSS>'))
        self.assertEqual(u'házunk', affix(u'ház', 'NOUN<POSS<PLUR><1>>'))
        self.assertEqual(u'házatok', affix(u'ház', 'NOUN<POSS<PLUR><2>>'))
        self.assertEqual(u'házuk', affix(u'ház', 'NOUN<POSS<PLUR>>'))
        self.assertEqual(u'fiai', affix(u'fia', 'NOUN<PLUR><POSS>'))
        self.assertEqual(u'fiaiéi', affix(u'fia', 'NOUN<PLUR><POSS><ANP<PLUR>>'))
        self.assertEqual(u'házaiéi', affix(u'ház', 'NOUN<PLUR><POSS><ANP<PLUR>>'))
        self.assertEqual(u'fiukéi', affix(u'fia', 'NOUN<POSS<PLUR>><ANP<PLUR>>'))
        self.assertEqual(u'házukéi', affix(u'ház', 'NOUN<POSS<PLUR>><ANP<PLUR>>'))
        self.assertEqual(u'fiaikéi', affix(u'fia', 'NOUN<PLUR><POSS<PLUR>><ANP<PLUR>>'))
        self.assertEqual(u'házaikéi', affix(u'ház', 'NOUN<PLUR><POSS<PLUR>><ANP<PLUR>>'))
        self.assertEqual(u'fiainkéinak', affix(u'fia', 'NOUN<PLUR><POSS<PLUR><1>><ANP<PLUR>><CAS<DAT>>'))
        self.assertEqual(u'fiaitokéinak', affix(u'fia', 'NOUN<PLUR><POSS<PLUR><2>><ANP<PLUR>><CAS<DAT>>'))
        self.assertEqual(u'fiúék', affix(u'fiú', 'NOUN<PLUR<FAM>>'))
        self.assertEqual(u'fiáék', affix(u'fia', 'NOUN<PLUR<FAM>><POSS>'))
        self.assertEqual(u'fiúéké', affix(u'fiú', 'NOUN<PLUR<FAM>><ANP>'))
        self.assertEqual(u'fiáéké', affix(u'fia', 'NOUN<PLUR<FAM>><POSS><ANP>'))

        # kiváncsijaitokét kivácsi/ADJ<PLUR><POSS<PLUR><2>><ANP><CAS<ACC>>
        # kétezreinkével kétezer/NUM<PLUR><POSS<PLUR><1>><ANP><CAS<INS>>

        self.assertEqual(u'ad', affix(u'ad', 'VERB'))
        self.assertEqual(u'adhat', affix(u'ad', 'VERB<MODAL>'))
        self.assertEqual(u'adja', affix(u'ad', 'VERB<DEF>'))
        self.assertEqual(u'adhatja', affix(u'ad', 'VERB<MODAL><DEF>'))
        self.assertEqual(u'adod', affix(u'ad', 'VERB<PERS<2>><DEF>'))
        self.assertEqual(u'adhatod', affix(u'ad', 'VERB<MODAL><PERS<2>><DEF>'))
        self.assertEqual(u'adjátok', affix(u'ad', 'VERB<PLUR><PERS<2>><DEF>'))
        self.assertEqual(u'adhatjátok', affix(u'ad', 'VERB<MODAL><PLUR><PERS<2>><DEF>'))
        self.assertEqual(u'adtátok', affix(u'ad', 'VERB<PAST><PLUR><PERS<2>><DEF>'))
        self.assertEqual(u'adhattátok', affix(u'ad', 'VERB<MODAL><PAST><PLUR><PERS<2>><DEF>'))

        self.assertEqual(u"árlánokat", affix(u"árlán", "NOUN<PLUR><CAS<ACC>>"))
        self.assertEqual(u"könyésszel", affix(u"könyész", "NOUN<CAS<INS>>"))

        self.assertEqual(u"pirosakat", affix(u"piros", "ADJ<PLUR><CAS<ACC>>"))

if __name__ == '__main__':
    unittest.main()
