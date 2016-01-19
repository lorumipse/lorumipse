# coding: utf-8

from scratch import GFactory

def affix(stem, ana):
    if ana.startswith("NOUN"):
        w = GFactory.parseNP(stem)
        if ana == "NOUN":
            return w.ortho
        if ana == "NOUN<CAS<ACC>>":
            return w.makeAccusativus().ortho
    elif ana.startswith("VERB"):
        w = GFactory.parseV(stem)
        if ana == "VERB<PERS<2>><PLUR><DEF>":
            return w.conjugate(3, 2, 1, 0, 3).ortho
        if ana == "VERB<PERS<2>><PLUR>":
            return w.conjugate(3, 2, 1, 0, 0).ortho
        return w.getCitationForm().ortho
    return stem


import unittest


class TestMorphology(unittest.TestCase):

    def test_affix(self):
        self.assertEqual(u'futurt', affix(u'futur', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'vizecskét', affix(u'vizecske', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'tapáljátok', affix(u'tapál', 'VERB<PERS<2>><PLUR><DEF>'))
        self.assertEqual(u'tapáltok', affix(u'tapál', 'VERB<PERS<2>><PLUR>'))
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

