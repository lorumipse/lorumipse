#!/usr/bin/python
# coding=UTF-8
# vim: set fileencoding=UTF-8

import re
import copy

class Phonology :

    phonocode = {
        u'a' : 'A--1-',
        u'á' : 'A--2-',
        u'e' : 'A-I1-',
        u'é' : 'A-I2t',
        u'i' : '--I1t',
        u'í' : '--I2t',
        u'u' : '-U-1-',
        u'ú' : '-U-2-',
        u'ü' : '-UI2-',
        u'ű' : '-UI2-',
        u'o' : 'AU-1-',
        u'ó' : 'AU-2-',
        u'ö' : 'AUI1-',
        u'ő' : 'AUI2-',
    }

    @staticmethod
    def getPropagatedX(X_pattern, ortho, t_pattern) :
        X_re = re.compile(X_pattern)
        t_re = re.compile(t_pattern)
        is_propagated = None
        for chr in ortho :
            if chr in Phonology.phonocode :
                phc = Phonology.phonocode[chr]
                if t_re.match(phc) :
                    if is_propagated is not None :
                        continue
                if X_re.match(phc) :
                    is_propagated = True
                else :
                    is_propagated = False
        return is_propagated

    @staticmethod
    def getPropagatedI(ortho) :
        return Phonology.getPropagatedX('^..I', ortho, '^....t')

    @staticmethod
    def getPropagatedU(ortho) :
        return Phonology.getPropagatedX('^.U.', ortho, '^....t')

    @staticmethod
    def needSuffixI(ortho) :
        return Phonology.getPropagatedI(ortho)

    @staticmethod
    def needSuffixU(ortho) :
        return Phonology.getPropagatedU(ortho)

    vtmr_map = {
        u'á' : u'a',
        u'é' : u'e',
        u'í' : u'i',
        u'ó' : u'o',
        u'ő' : u'ö',
        u'ú' : u'u',
        u'ű' : u'ü',
    };

    amny_map = {
        u'a' : u'á',
        u'e' : u'é',
    };

    # magánhangzó-rövidülések
    @staticmethod
    def doMR(ortho) :
        return Phonology.tr(ortho, Phonology.vtmr_map);

    # utolsó alsó magánhangzó nyúlása
    @staticmethod
    def doAMNY(ortho) :
        return ortho[0:-1]+Phonology.tr(ortho[-1:], Phonology.amny_map);

    @staticmethod
    def tr(ortho, map) :
        str = ''
        for chr in ortho :
            if chr in map :
                str += map[chr]
            else :
                str += chr
        return str

    vowelmaps = {
            '--,O' : { u'A' : u'a', u'Á' : u'á', u'E' : u'o', u'O' : u'o', u'Ó' : u'ó', u'U' : u'u', u'Ú' : u'ú', u'V' : u'a', u'W' : u'o'},
            'U-,O' : { u'A' : u'a', u'Á' : u'á', u'E' : u'o', u'O' : u'o', u'Ó' : u'ó', u'U' : u'u', u'Ú' : u'ú', u'V' : u'a', u'W' : u'o'},
            '-I,O' : { u'A' : u'e', u'Á' : u'é', u'E' : u'e', u'O' : u'e', u'Ó' : u'ő', u'U' : u'ü', u'Ú' : u'ű', u'V' : u'e', u'W' : u'e'},
            'UI,O' : { u'A' : u'e', u'Á' : u'é', u'E' : u'e', u'O' : u'ö', u'Ó' : u'ő', u'U' : u'ü', u'Ú' : u'ű', u'V' : u'e', u'W' : u'e'},
            '--,-' : { u'A' : u'a', u'Á' : u'á', u'E' : u'o', u'O' : u'o', u'Ó' : u'ó', u'U' : u'u', u'Ú' : u'ú', u'V' : u'o', u'W' : u'o'},
            'U-,-' : { u'A' : u'a', u'Á' : u'á', u'E' : u'o', u'O' : u'o', u'Ó' : u'ó', u'U' : u'u', u'Ú' : u'ú', u'V' : u'o', u'W' : u'o'},
            '-I,-' : { u'A' : u'e', u'Á' : u'é', u'E' : u'e', u'O' : u'e', u'Ó' : u'ő', u'U' : u'ü', u'Ú' : u'ű', u'V' : u'e', u'W' : u'e'},
            'UI,-' : { u'A' : u'e', u'Á' : u'é', u'E' : u'ö', u'O' : u'ö', u'Ó' : u'ő', u'U' : u'ü', u'Ú' : u'ű', u'V' : u'ö', u'W' : u'e'},
    };

    @staticmethod
    def interpolateVowels(phonocode, string) :
        if phonocode in Phonology.vowelmaps :
            return Phonology.tr(string, Phonology.vowelmaps[phonocode]);
        else :
            return string

    @staticmethod
    def isOpening(string) :
        return False

    @staticmethod
    def needSuffixPhonocode(string) :
        return \
                ('U' if Phonology.needSuffixU(string) else '-') + \
                ('I' if Phonology.needSuffixI(string) else '-') + \
                (',O' if Phonology.isOpening(string) else ',-')

    skeletoncode = {
        'a' : 'V',
        'á' : 'V',
        'e' : 'V',
        'é' : 'V',
        'i' : 'V',
        'í' : 'V',
        'u' : 'V',
        'ú' : 'V',
        'ü' : 'V',
        'ű' : 'V',
        'o' : 'V',
        'ó' : 'V',
        'ö' : 'V',
        'ő' : 'V',
        'ddzs' : 'C',
        'ccs' : 'C',
        'ddz' : 'C',
        'dzs' : 'C',
        'ggy' : 'C',
        'lly' : 'C',
        'nny' : 'C',
        'ssz' : 'C',
        'tty' : 'C',
        'zzs' : 'C',
        'bb' : 'C',
        'cc' : 'C',
        'cs' : 'C',
        'dd' : 'C',
        'dz' : 'C',
        'ff' : 'C',
        'gg' : 'C',
        'gy' : 'C',
        'hh' : 'C',
        'jj' : 'C',
        'kk' : 'C',
        'll' : 'C',
        'ly' : 'C',
        'mm' : 'C',
        'nn' : 'C',
        'ny' : 'C',
        'pp' : 'C',
        'qq' : 'C',
        'rr' : 'C',
        'ss' : 'C',
        'sz' : 'C',
        'tt' : 'C',
        'ty' : 'C',
        'vv' : 'C',
        'ww' : 'C',
        'xx' : 'C',
        'zs' : 'C',
        'zz' : 'C',
        'b' : 'C',
        'c' : 'C',
        'd' : 'C',
        'f' : 'C',
        'g' : 'C',
        'h' : 'C',
        'j' : 'C',
        'k' : 'C',
        'l' : 'C',
        'm' : 'C',
        'n' : 'C',
        'p' : 'C',
        'q' : 'C',
        'r' : 'C',
        's' : 'C',
        't' : 'C',
        'v' : 'C',
        'w' : 'C',
        'x' : 'C',
        'z' : 'C',
    };

    @staticmethod
    def isVowel(char) :
        return (char in Phonology.skeletoncode) and (Phonology.skeletoncode[char] == 'V')

    consonant_regex = r'(ddzs|ccs|ddz|dzs|ggy|lly|nny|ssz|tty|zzs|bb|cc|cs|dd|dz|ff|gg|gy|h|hh|jj|k|kk|ll|ly|mm|nn|ny|pp|qq|rr|ss|sz|tt|ty|vv|ww|xx|zs|zz|b|c|d|f|g|j|l|m|n|p|q|r|s|t|v|w|x|z)$'

    @staticmethod
    def getLastConsonant(ortho) :
        regex = re.compile(Phonology.consonant_regex)
        match = regex.search(ortho)
        if match :
            return match.group(1)
        return None

    double_consonants = {
        'ddzs' : 'ddzs',
        'ccs' : 'ccs',
        'ddz' : 'ddz',
        'dzs' : 'ddzs',
        'ggy' : 'ggy',
        'lly' : 'lly',
        'nny' : 'nny',
        'ssz' : 'ssz',
        'tty' : 'tty',
        'zzs' : 'zzs',
        'bb' : 'bb',
        'cc' : 'cc',
        'cs' : 'ccs',
        'dd' : 'dd',
        'dz' : 'ddz',
        'ff' : 'ff',
        'gg' : 'gg',
        'gy' : 'ggy',
        'hh' : 'hh',
        'jj' : 'jj',
        'kk' : 'kk',
        'll' : 'll',
        'ly' : 'lly',
        'mm' : 'mm',
        'nn' : 'nn',
        'ny' : 'nny',
        'pp' : 'pp',
        'qq' : 'qq',
        'rr' : 'rr',
        'ss' : 'ss',
        'sz' : 'ssz',
        'tt' : 'tt',
        'ty' : 'tty',
        'vv' : 'vv',
        'ww' : 'ww',
        'xx' : 'xx',
        'zs' : 'zzs',
        'zz' : 'zz',
        'b' : 'bb',
        'c' : 'cc',
        'd' : 'dd',
        'f' : 'ff',
        'g' : 'gg',
        'h' : 'hh',
        'j' : 'jj',
        'k' : 'kk',
        'l' : 'll',
        'm' : 'mm',
        'n' : 'nn',
        'p' : 'pp',
        'q' : 'qq',
        'r' : 'rr',
        's' : 'ss',
        't' : 'tt',
        'v' : 'vv',
        'w' : 'ww',
        'x' : 'xx',
        'z' : 'zz',
    };

    @staticmethod
    def doubleConsonant(cons) :
        if cons in Phonology.double_consonants :
            return Phonology.double_consonants[cons]
        else :
            return None

    @staticmethod
    def doDoubleLastConsonant(ortho) :
        cons = Phonology.getLastConsonant(ortho)
        if cons :
            return ortho[0:-len(cons)]+Phonology.doubleConsonant(cons);
        else :
            return ortho

    @staticmethod
    def canAssimilate(left_ortho, right_ortho, char) :
        return not Phonology.isVowel(left_ortho[-1:]) and right_ortho[0:len(char)] == char

    is_affrikate = {
        'dz' : True,
        'ddz' : True,
        'dzs' : True,
        'ddzs' : True,
        'c' : True,
        'cc' : True,
        'cs' : True,
        'ccs' : True,
    };

    is_sybyl = {
        's' : True,
        'ss' : True,
        'sz' : True,
        'ssz' : True,
        'z' : True,
        'zz' : True,
        'zs' : True,
        'zzs' : True,
    };

    @staticmethod
    def isAffrikate(cons) :
        return (cons in Phonology.is_affrikate) and (Phonology.is_affrikate[cons])

    @staticmethod
    def isSybyl(cons) :
        return (cons in Phonology.is_sybyl) and (Phonology.is_sybyl[cons])

class iWordformMorphology :

    def appendSuffix(self, suffix) : pass 
    def onBeforeSuffixation(self, suffix) : pass

class iWordformPhonology :

    def isLastVowel(self) : pass
    def isVTMR(self) : pass
    def isBTMR(self) : pass 
    def isOpening(self) : pass 
    def isAMNYLeft(self) : pass 
    def isAMNYRight(self) : pass 
    def isAlternating(self) : pass 
    def needSuffixU(self) : pass 
    def needSuffixI(self) : pass 
    def needSuffixPhonocode(self) : pass 
    def doAssimilate(self, char) : pass

class Wordform (iWordformMorphology, iWordformPhonology) :

    def __init__(self, lemma=None, ortho=None) :
        self.lemma = lemma;
        self.ortho = ortho if ortho else lemma;
        self.is_vtmr = False
        self.is_btmr = False
        self.is_opening = False
        self.is_amny = None
        self.is_alternating = False
        self.needSuffixI = None

    def __repr__(self) :
        return self.ortho

    def cloneAs(self, className) :
        clone = className(self.lemma, self.ortho)
        for key in self.__dict__ :
            setattr(clone, key, self.__dict__[key])
        return clone

    def appendSuffix(self, suffix) :
        stem = self.cloneAs(Wordform)
        stem.ortho += suffix.ortho
        return stem

    # iWordformPhonology {{{

    def isLastVowel(self) :
        return Phonology.isVowel(self.ortho[-1:])

    def isAMNYLeft(self) :
        return self.is_amny

    def isAlternating(self) :
        return self.is_alternating

    def needSuffixPhonocode(self) :
        return Phonology.needSuffixPhonocode(self.ortho)

    def isVTMR(self) :
        return self.is_vtmr

    def isBTMR(self) :
        return self.is_btmr

    def attribstr(self):
        return self.needSuffixPhonocode() + \
            ('V' if self.isLastVowel() else 'C') + \
            ('A' if self.isAMNYLeft() else '-') + \
            ('v' if self.isVTMR() else '-') + \
            ('b' if self.isBTMR() else '-') + \
            ('@' if self.isAlternating() else '~')

class Wordform1 (Wordform) : 

    def appendSuffix(self, suffix) :
        # @todo check input class
        stem = self.cloneAs(Wordform)
        output_class = Wordform
        affix = copy.copy(suffix)
        stem.onBeforeSuffixation(affix)
        affix.onBeforeSuffixed(stem)
        interfix_ortho = affix.getInterfix(stem)
        stem.ortho += suffix.ortho
        affix.onAfterSuffixed(stem)
        return stem

import unittest

class GrammarTest (unittest.TestCase) :

    def testVowelHarmony(self) :
        self.assertEqual(True , Phonology.getPropagatedI('ember'), 'ember')
        self.assertEqual(False, Phonology.getPropagatedI(u'ház'), u'ház')
        self.assertEqual(True , Phonology.getPropagatedI(u'föld'), u'föld')
        self.assertEqual(True , Phonology.getPropagatedI(u'kert'), u'kert')
        self.assertEqual(True , Phonology.getPropagatedI(u'kéz'), u'kéz')
        self.assertEqual(False, Phonology.getPropagatedI(u'út'), u'út')
        self.assertEqual(True , Phonology.getPropagatedI(u'kövér'), u'kövér')
        self.assertEqual(True , Phonology.getPropagatedI(u'sofőr'), u'sofőr')
        self.assertEqual(False, Phonology.getPropagatedI(u'kőfal'), u'kőfal')
        self.assertEqual(False, Phonology.getPropagatedI(u'bika'), u'bika')
        self.assertEqual(False, Phonology.getPropagatedI(u'nüansz'), u'nüansz')

        self.assertEqual(False, Phonology.getPropagatedU(u'ház'), u'ház')
        self.assertEqual(False, Phonology.getPropagatedU(u'kert'), u'kert')
        self.assertEqual(True , Phonology.getPropagatedU(u'föld'), u'föld')
        self.assertEqual(False, Phonology.getPropagatedU(u'kéz'), u'kéz')

        self.assertEqual(False, Phonology.needSuffixI(u'ház'), u'ház');
        self.assertEqual(True , Phonology.needSuffixI(u'kert'), u'kert');
        self.assertEqual(True , Phonology.needSuffixI(u'föld'), u'föld');
        self.assertEqual(True , Phonology.needSuffixI(u'tök'), u'tök');
        self.assertEqual(True , Phonology.needSuffixI(u'kéz'), u'kéz');

        self.assertEqual(False, Phonology.needSuffixU(u'ház'), u'ház');
        self.assertEqual(False, Phonology.needSuffixU(u'kert'), u'kert');
        self.assertEqual(True , Phonology.needSuffixU(u'föld'), u'föld');
        self.assertEqual(True , Phonology.needSuffixU(u'tök'), u'tök');
        self.assertEqual(False, Phonology.needSuffixU(u'kéz'), u'kéz');

    def testAMNY(self) :
        self.assertEqual(u'fá', Phonology.doAMNY(u'fa'))
        self.assertEqual(u'almá', Phonology.doAMNY(u'alma'))
        self.assertEqual(u'medvé', Phonology.doAMNY(u'medve'))

    def testMR(self) :
        self.assertEqual(u'aktiv', Phonology.doMR(u'aktív'))
        self.assertEqual(u'ur', Phonology.doMR(u'úr'))
        self.assertEqual(u'fuzio', Phonology.doMR(u'fúzió'))

    def testInterpolateVowels(self) :
        self.assertEqual(u'UI,-', Phonology.needSuffixPhonocode(u'fül'))
        self.assertEqual(u'hoz', Phonology.interpolateVowels(Phonology.needSuffixPhonocode(u'fal'), u'hOz'))
        self.assertEqual(u'hez', Phonology.interpolateVowels(Phonology.needSuffixPhonocode(u'fék'), u'hOz'))
        self.assertEqual(u'höz', Phonology.interpolateVowels(Phonology.needSuffixPhonocode(u'fül'), u'hOz'))

    def testPhonologyRest(self) :
        self.assertEqual(False, Phonology.isVowel('b'))
        self.assertEqual(True, Phonology.isVowel('a'))
        self.assertEqual(False, Phonology.isAffrikate('b'))
        self.assertEqual(True, Phonology.isAffrikate('cs'))
        self.assertEqual(False, Phonology.isSybyl('b'))
        self.assertEqual(True, Phonology.isSybyl('s'))

    def testDoubleConsonant(self) :
        self.assertEqual(u'bb', Phonology.doubleConsonant(u'b'))
        self.assertEqual(u'bb', Phonology.doubleConsonant(u'bb'))
        self.assertEqual(u'cc', Phonology.doubleConsonant(u'c'))
        self.assertEqual(u'ccs', Phonology.doubleConsonant(u'cs'))
        self.assertEqual(u'ccs', Phonology.doubleConsonant(u'ccs'))
        self.assertEqual(u'dd', Phonology.doubleConsonant(u'd'))
        self.assertEqual(u'ddz', Phonology.doubleConsonant(u'dz'))
        self.assertEqual(u'ddz', Phonology.doubleConsonant(u'ddz'))
        self.assertEqual(u'ddzs', Phonology.doubleConsonant(u'dzs'))
        self.assertEqual(u'ddzs', Phonology.doubleConsonant(u'ddzs'))
        self.assertEqual(u'ff', Phonology.doubleConsonant(u'f'))
        self.assertEqual(u'ff', Phonology.doubleConsonant(u'ff'))
        self.assertEqual(u'gg', Phonology.doubleConsonant(u'g'))
        self.assertEqual(u'gg', Phonology.doubleConsonant(u'gg'))
        self.assertEqual(u'ggy', Phonology.doubleConsonant(u'gy'))
        self.assertEqual(u'ggy', Phonology.doubleConsonant(u'ggy'))
        self.assertEqual(u'hh', Phonology.doubleConsonant(u'h'))
        self.assertEqual(u'jj', Phonology.doubleConsonant(u'j'))
        self.assertEqual(u'jj', Phonology.doubleConsonant(u'jj'))
        self.assertEqual(u'kk', Phonology.doubleConsonant(u'k'))
        self.assertEqual(u'kk', Phonology.doubleConsonant(u'kk'))
        self.assertEqual(u'll', Phonology.doubleConsonant(u'l'))
        self.assertEqual(u'll', Phonology.doubleConsonant(u'll'))
        self.assertEqual(u'lly', Phonology.doubleConsonant(u'ly'))
        self.assertEqual(u'lly', Phonology.doubleConsonant(u'lly'))
        self.assertEqual(u'mm', Phonology.doubleConsonant(u'm'))
        self.assertEqual(u'mm', Phonology.doubleConsonant(u'mm'))
        self.assertEqual(u'nn', Phonology.doubleConsonant(u'n'))
        self.assertEqual(u'nn', Phonology.doubleConsonant(u'nn'))
        self.assertEqual(u'nny', Phonology.doubleConsonant(u'ny'))
        self.assertEqual(u'nny', Phonology.doubleConsonant(u'nny'))
        self.assertEqual(u'pp', Phonology.doubleConsonant(u'p'))
        self.assertEqual(u'pp', Phonology.doubleConsonant(u'pp'))
        self.assertEqual(u'qq', Phonology.doubleConsonant(u'q'))
        self.assertEqual(u'rr', Phonology.doubleConsonant(u'r'))
        self.assertEqual(u'rr', Phonology.doubleConsonant(u'rr'))
        self.assertEqual(u'ss', Phonology.doubleConsonant(u's'))
        self.assertEqual(u'ss', Phonology.doubleConsonant(u'ss'))
        self.assertEqual(u'ssz', Phonology.doubleConsonant(u'sz'))
        self.assertEqual(u'ssz', Phonology.doubleConsonant(u'ssz'))
        self.assertEqual(u'tt', Phonology.doubleConsonant(u't'))
        self.assertEqual(u'tt', Phonology.doubleConsonant(u'tt'))
        self.assertEqual(u'tty', Phonology.doubleConsonant(u'ty'))
        self.assertEqual(u'tty', Phonology.doubleConsonant(u'tty'))
        self.assertEqual(u'vv', Phonology.doubleConsonant(u'v'))
        self.assertEqual(u'vv', Phonology.doubleConsonant(u'vv'))
        self.assertEqual(u'ww', Phonology.doubleConsonant(u'w'))
        self.assertEqual(u'xx', Phonology.doubleConsonant(u'x'))
        self.assertEqual(u'zz', Phonology.doubleConsonant(u'z'))
        self.assertEqual(u'zz', Phonology.doubleConsonant(u'zz'))
        self.assertEqual(u'zzs', Phonology.doubleConsonant(u'zs'))
        self.assertEqual(u'zzs', Phonology.doubleConsonant(u'zzs'))

        self.assertEqual(u'bika', Phonology.doDoubleLastConsonant(u'bika'))
        self.assertEqual(u'házz', Phonology.doDoubleLastConsonant(u'ház'))
        self.assertEqual(True, Phonology.canAssimilate(u'ház', u'val', u'v'))
        self.assertEqual(False, Phonology.canAssimilate(u'bika', u'val', u'v'))

    def testLastConsonant(self) :
        self.assertEqual(u'b', Phonology.getLastConsonant(u'galamb'))
        self.assertEqual(u'bb', Phonology.getLastConsonant(u'szebb'))
        self.assertEqual(u'c', Phonology.getLastConsonant(u'léc'))
        self.assertEqual(u'cs', Phonology.getLastConsonant(u'mécs'))
        self.assertEqual(u'ccs', Phonology.getLastConsonant(u'meccs'))
        self.assertEqual(u'd', Phonology.getLastConsonant(u'fajd'))
        self.assertEqual(u'dz', Phonology.getLastConsonant(u'edz'))
        self.assertEqual(u'ddz', Phonology.getLastConsonant(u'xeddz'))
        self.assertEqual(u'dzs', Phonology.getLastConsonant(u'bridzs'))
        self.assertEqual(u'ddzs', Phonology.getLastConsonant(u'briddzs'))
        self.assertEqual(u'f', Phonology.getLastConsonant(u'xef'))
        self.assertEqual(u'ff', Phonology.getLastConsonant(u'xeff'))
        self.assertEqual(u'g', Phonology.getLastConsonant(u'ág'))
        self.assertEqual(u'gg', Phonology.getLastConsonant(u'agg'))
        self.assertEqual(u'gy', Phonology.getLastConsonant(u'megy'))
        self.assertEqual(u'ggy', Phonology.getLastConsonant(u'meggy'))
        self.assertEqual(u'h', Phonology.getLastConsonant(u'düh'))
        self.assertEqual(u'j', Phonology.getLastConsonant(u'díj'))
        self.assertEqual(u'jj', Phonology.getLastConsonant(u'fejj'))
        self.assertEqual(u'k', Phonology.getLastConsonant(u'mák'))
        self.assertEqual(u'kk', Phonology.getLastConsonant(u'makk'))
        self.assertEqual(u'l', Phonology.getLastConsonant(u'ál'))
        self.assertEqual(u'll', Phonology.getLastConsonant(u'áll'))
        self.assertEqual(u'ly', Phonology.getLastConsonant(u'mély'))
        self.assertEqual(u'lly', Phonology.getLastConsonant(u'gally'))
        self.assertEqual(u'm', Phonology.getLastConsonant(u'ham'))
        self.assertEqual(u'mm', Phonology.getLastConsonant(u'hamm'))
        self.assertEqual(u'n', Phonology.getLastConsonant(u'mén'))
        self.assertEqual(u'nn', Phonology.getLastConsonant(u'benn'))
        self.assertEqual(u'ny', Phonology.getLastConsonant(u'lány'))
        self.assertEqual(u'nny', Phonology.getLastConsonant(u'szenny'))
        self.assertEqual(u'p', Phonology.getLastConsonant(u'szép'))
        self.assertEqual(u'pp', Phonology.getLastConsonant(u'csepp'))
        self.assertEqual(u'q', Phonology.getLastConsonant(u'faq'))
        self.assertEqual(u'r', Phonology.getLastConsonant(u'dir'))
        self.assertEqual(u'rr', Phonology.getLastConsonant(u'durr'))
        self.assertEqual(u's', Phonology.getLastConsonant(u'dés'))
        self.assertEqual(u'ss', Phonology.getLastConsonant(u'ess'))
        self.assertEqual(u'sz', Phonology.getLastConsonant(u'ész'))
        self.assertEqual(u'ssz', Phonology.getLastConsonant(u'xessz'))
        self.assertEqual(u't', Phonology.getLastConsonant(u'lát'))
        self.assertEqual(u'tt', Phonology.getLastConsonant(u'lőtt'))
        self.assertEqual(u'ty', Phonology.getLastConsonant(u'báty'))
        self.assertEqual(u'tty', Phonology.getLastConsonant(u'xetty'))
        self.assertEqual(u'v', Phonology.getLastConsonant(u'hamv'))
        self.assertEqual(u'vv', Phonology.getLastConsonant(u'xevv'))
        self.assertEqual(u'w', Phonology.getLastConsonant(u'how'))
        self.assertEqual(u'x', Phonology.getLastConsonant(u'bix'))
        self.assertEqual(u'z', Phonology.getLastConsonant(u'bűz'))
        self.assertEqual(u'zz', Phonology.getLastConsonant(u'bízz'))
        self.assertEqual(u'zs', Phonology.getLastConsonant(u'bézs'))
        self.assertEqual(u'zzs', Phonology.getLastConsonant(u'xezzs'))

    def testWordform(self) :
        w = Wordform(u'ember')
        self.assertEqual(u'ember', str(w))
        x = w.cloneAs(Wordform)
        self.assertEqual(u'ember', str(x))

    def testPhonology1(self) :
        w = Wordform(u'ember')
        s = Wordform(u'ke')
        self.assertEqual(u'emberke', str(w.appendSuffix(s)))

