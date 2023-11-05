# coding: utf-8
from __future__ import absolute_import
from builtins import str
from builtins import object
from .grammar import Phonology, Wordform
import re

class iSuffixumMorphology(object):
    def hasOptionalInterfix(): pass
    def getOptionalInterfix(): pass
    def getNonOptionalSuffix(): pass
    def getInterfix(stem): pass
    def onBeforeSuffixed(stem): pass
    def onAfterSuffixed(stem): pass

class iSuffixumPhonology(object):
    def onAssimilated(char, ortho): pass

"""
 * @todo create a NomenSuffixum descendant and move down things (e.g. hasonul-v)
"""
class Suffixum(Wordform, iSuffixumMorphology, iSuffixumPhonology):

    _input_class = 'Nomen'
    _output_class = 'Nomen'
    stop_jaje = False

    def getInputClass(self):
        return self._input_class

    def getOutputClass(self):
        return self._output_class

    def isAMNYRight(self):
        if None != self.is_amny:
            return self.is_amny
        return True

    def hasOptionalInterfix(self):
        return self.lemma[0:1] == '_'

    def getOptionalInterfix(self):
        if self.hasOptionalInterfix():
            return self.lemma[1:1+1]
        else:
            return ''

    def getNonOptionalSuffix(self):
        if self.hasOptionalInterfix():
            return self.lemma[2:]
        else:
            return self.lemma

    def getInvalidSuffixRegexList(self):
        return [
            r'[bcdfghkmptvw],t',
            r'[bcdfghklmnpqrstvwyz],[dkmn]',
            r'[bcdfghklmnpqrstvwyz]{2,},[bcdfghklmnpqrstvwyz]',
            r'[lrsy],t.+', # @see barnulástok, hoteltek
        ]

    def isValidSuffixConcatenation(self, ortho_stem, ortho_suffix):
        string = ortho_stem+u","+ortho_suffix
        for regex in self.getInvalidSuffixRegexList():
            if re.search(regex, string):
                return False
        return True

    # kötőhang
    def getInterfix(self, stem):
        interfix = ''
        if self.hasOptionalInterfix():
            _interfix = self.getOptionalInterfix()
            _interfix = Phonology.interpolateVowels(stem.needSuffixPhonocode(), _interfix)
            if stem.isOpening() and not stem.isLastVowel():
                interfix = _interfix
            elif stem.isLastVowel():
                interfix = ''
            elif isinstance(self, PossessiveSuffixum):
                interfix = _interfix
            else:
                if self.isValidSuffixConcatenation(stem.ortho, self.ortho):
                    interfix = ''
                else:
                    interfix = _interfix
        return interfix

    def onAssimilated(self, char, ortho):
        return ortho[1:]

    def onBeforeSuffixed(self, stem):
        ortho = self.getNonOptionalSuffix()
        char = u'v'
        if Phonology.canAssimilate(stem.ortho, ortho, char):
            stem.doAssimilate(char)
            ortho = self.onAssimilated(char, ortho)
        ortho = Phonology.interpolateVowels(stem.needSuffixPhonocode(), ortho)
        self.ortho = ortho

    def onAfterSuffixed(self, stem):
        if isinstance(stem, Nomen) and self.stop_jaje:
            stem.is_jaje = False


class NomenSuffixum(Suffixum): pass


class iNumPers(object):

     def makeNumPers(self, numero = 1, person = 3):
         self.numero = numero
         self.person = person
         return self

     def getNumero(self):
         return self.numero

     def getPerson(self):
         return self.person


class PossessiveSuffixum(Suffixum, iNumPers):

    _input_class = 'iPossessable'
    _output_class = 'Nomen'

    suffixmap = {
        1: {
            1: {1 : '_Vm', 2 : '_Vd', 3 : 'A'},
            3: {1 : '_Unk', 2 : '_VtEk', 3 : 'Uk'},
        },
        3: {
            1: {1 : '_Aim', 2 : '_Aid', 3 : '_Ai'},
            3: {1 : '_Aink', 2 : '_AitWk', 3 : '_Aik'},
        },
     }

    def __init__(self, numero = 1, person = 3, possessed_numero = 1):
        suffixcode = PossessiveSuffixum.suffixmap[possessed_numero][numero][person];
        super(PossessiveSuffixum, self).__init__(suffixcode)
        self.makeNumPers(numero, person)
        self.possessed_numero = possessed_numero
        self.is_opening = True
        self.is_vtmr = True
        self.is_alternating = True

    def onBeforeSuffixed(self, stem):
        super(PossessiveSuffixum, self).onBeforeSuffixed(stem);
        # birtokos A/jA
        if self.person == 3 and self.possessed_numero == 1 and stem.isJaje():
            self.ortho = 'j'+self.ortho;

    def onAfterSuffixed(self, stem):
        stem.is_opening = True;
        self.numero = stem.numero;


class PossessorSuffixum(Suffixum):
    """ 
     * Birtokjel
    """

    _input_class = 'iPossessable';
    _output_class = 'Nomen';

    def __init__(self, possessed_numero = 1):
        suffixcode = u'é' if possessed_numero == 1 else u'éi';
        super(PossessorSuffixum, self).__init__(suffixcode)
        self.possessed_numero = possessed_numero
        self.person = 3
        self.is_opening = True
        self.is_vtmr = False

    def onAfterSuffixed(self, stem):
        stem.is_opening = True
        self.numero = stem.numero


class iVerbal(iNumPers):

     def getCase(self):
         return str(self.numero) + str(self.person) + str(self.mood) + str(((10+self.tense) if self.tense < 0 else self.tense)) + str(self.definite)

     def setCase(self, code):
         self.numero = int(code[0])
         self.person = int(code[1])
         self.mood = int(code[2])
         self.tense = int(code[3])
         self.definite = int(code[4])

     def matchCase(self, regex):
         return re.match("^" + regex + "$", self.getCase())


class aVerbalSuffixum(Suffixum, iVerbal, iNumPers):

    _input_class = 'Verbum';
    _output_class = 'Verbum';

    paradigm = []

    def __init__(self, numero, person, mood=1, tense=0, definite=0):
        """
         * @param $numero = 1 egyes szám, 3 többes szám
         * @param $person = 1 első személy, 2 második személy, 3 harmadik személy
         * @param $mood = 1 kijelentő, 2 feltételes, 3 felszólító
         * @param $tense = -1 múlt, 0 jelen, 1 jövő
         * @param $definite = 0 alanyi, 3 tárgyas, 2 lAk
        """
        self.mood = mood
        self.tense = tense
        self.definite = definite
        self.numero = numero
        self.person = person

    def onAfterSuffixed(self, stem):
        stem.mood = self.mood
        stem.tense = self.tense
        stem.definite = self.definite
        stem.numero = self.numero
        stem.person = self.person
    

class VerbalSuffixum1(aVerbalSuffixum):

    def __init__(self, numero, person, mood=1, tense=0, definite=0):
         self.lemma = u''
         self.ortho = self.lemma
         super(VerbalSuffixum1, self).__init__(numero, person, mood, tense, definite)
         if self.tense == -1: # múlt idő jele
             self.lemma = u't'
             self.ortho = self.lemma
         if self.mood == 2 &self.tense == 0: # feltételes mód jele
             self.lemma = u'n'
             self.ortho = self.lemma
         if self.mood == 3: # felszólító mód jele
             self.lemma = u'j'
             self.ortho = self.lemma


    def onBeforeSuffixed(self, stem):
         if self.tense == -1: # múlt idő jele
             if stem.needVtt(self): # Vtt
                 self.ortho =  Phonology.interpolateVowels(stem.needSuffixPhonocode(), 'Vtt')
             elif stem.needTT(): # tt
                 self.ortho = u'tt'
             else: # t
                 self.ortho = u't'

         if self.mood == 2 and self.tense == 0: # feltételes mód jele
             if stem.needNN():
                 self.ortho = u'nn'
             else:
                 self.ortho = u'n'

         if self.mood == 3: # felszólító mód jele
             last = Phonology.getLastConsonant(stem.ortho)
             if stem.needJggy():
                 self.ortho = u'ggy'
             elif stem.needJgy():
                 self.ortho = u'gy'
             elif stem.needJss():
                 self.ortho = u'ss'
             elif stem.needJs():
                 self.ortho = u's'
             elif stem.needJAssim():
                 ortho = u'j'
                 char = u'j'
                 if Phonology.canAssimilate(stem.ortho, ortho, char):
                     stem.doAssimilate(char)
                     ortho = self.onAssimilated(char, ortho)
                 self.ortho = ortho
             else:
                 self.ortho = u'j'

    def getInterfix(self, stem):
         if not self.isValidSuffixConcatenation(stem.ortho, self.ortho):
             return Phonology.interpolateVowels(stem.needSuffixPhonocode(), u'A')
         return u''

    def getInvalidSuffixRegexList(self):
         return [r'lt,n',]

    def onAfterSuffixed(self, stem):
         super(VerbalSuffixum1, self).onAfterSuffixed(stem)
         if self.mood == 3:
             stem.is_opening = True


class VerbalSuffixum2(aVerbalSuffixum):

     """
      * paradigm[mood][tense][definite][numero][person]
      * mood = 1 kijelentő, 2 feltételes, 3 felszólító
      * tense = -1 múlt, 0 jelen, 1 jövő
      * definite = 0 alanyi, 3 tárgyas, 2 lAk
      * numero = 1 egyes szám, 3 többes szám
      * person = 1 első személy, 2 második személy, 3 harmadik személy
     """
     paradigm = {
         1: {
             0: {
                 0: {
                     1: {1: u'Vk', 2: u'_Asz|Vl', 3: u''},
                     3: {1: u'Unk', 2: u'_VtVk', 3: u'_AnAk'}
                 },
                 2: {
                     1: {1: u'lAk'},
                     },
                 3: {
                     1: {1: u'Vm', 2: u'Vd', 3: u'ja|i'},
                     3: {1: u'jUk', 2: u'jÁtVk|itek', 3: u'jÁk|ik'}
                 },
             },
             -1: {
                 0: {
                     1: {1: u'Am', 2: u'Ál', 3: u''},
                     3: {1: u'Unk', 2: u'_AtWk', 3: u'Ak'}
                 },
                 2: {
                     1: {1: u'AlAk'}
                 },
                 3: {
                     1: {1: u'Am', 2: u'Ad', 3: u'A'},
                     3: {1: u'Uk', 2: u'ÁtWk', 3: u'Ák'}
                 },
             },
         },
         2: {
             0: {
                 0: {
                     1: {1: u'ék', 2: u'Ál', 3: u'A'},
                     3: {1: u'Ánk', 2: u'ÁtWk', 3: u'ÁnAk'}
                 },
                 2: {
                     1: {1: u'ÁlAk'},
                     },
                 3: {
                     1: {1: u'Ám', 2: u'Ád', 3: u'Á'},
                     3: {1: u'Ánk', 2: u'ÁtWk', 3: u'Ák'}
                 },
             },
         },
         3: {
             0: {
                 0: {
                     1: {1: u'Ak', 2: u'Ál', 3: u'On'},
                     3: {1: u'Unk', 2: u'AtWk', 3: u'AnAk'}
                 },
                 2: {
                     1: {1: u'AlAk'},
                     },
                 3: {
                     1: {1: u'Am', 2: u'Ad', 3: u'A'},
                     3: {1: u'Uk', 2: u'ÁtWk', 3: u'Ák'}
                 }
             }
         }
     }

     def __init__(self, numero, person, mood=1, tense=0, definite=0):
         super(VerbalSuffixum2, self).__init__(numero, person, mood, tense, definite)
         self.lemma = self.paradigm[mood][tense][definite][numero][person]
         self.ortho = self.lemma

     def getInvalidSuffixRegexList(self):
         return [
             r'[dlstz]t,[nt]',
             r't,tt',
             r'lt,sz',
             r'lsz,[nt]'
         ]

     def getInterfix(self, stem):
         interfix = u''
         if self.hasOptionalInterfix() and not self.isValidSuffixConcatenation(stem.ortho, self.ortho):
             interfix += self.getOptionalInterfix()
             interfix = Phonology.interpolateVowels(stem.needSuffixPhonocode(), interfix)
         return interfix

     def onBeforeSuffixed(self, stem):
         lemma = self.lemma
         if lemma.find('|'):
             alters = lemma.split('|')
             # Vl/Asz
             if self.matchCase('12100') and stem.isLastAffrSyb():
                 i = 1
             elif self.matchCase('(13|32|33)103') and stem.needSuffixI():
                 i = 1
             else:
                 i = 0
             lemma = alters[i]
         self.lemma = lemma
    
         ortho = self.getNonOptionalSuffix()
         if not stem.isLastT():
             char = u'j'
             if Phonology.canAssimilate(stem.ortho, ortho, char):
                 stem.doAssimilate(char)
                 ortho = self.onAssimilated(char, ortho)
         ortho = Phonology.interpolateVowels(stem.needSuffixPhonocode(), ortho)
    
         if stem.ikes and self.matchCase('13100'):
             ortho = u'ik'
    
         self.ortho = ortho


class InfinitiveSuffixum(aVerbalSuffixum):

     paradigm = {
         1: {
             0: {
                 0: {
                     0: {0: u'ni'},
                     1: {1: u'nVm', 2: u'nVd', 3: u'niA'},
                     3: {1: u'nUnk', 2: u'nVtVk', 3: u'niUk'}
                 }
             }
         }
     }
    
     def __init__(self, numero, person, mood=1, tense=0, definite=0):
         super(InfinitiveSuffixum, self).__init__(numero, person, mood, tense, definite)
         self.lemma = self.paradigm[mood][tense][definite][numero][person]
    
     def onBeforeSuffixed(self, stem):
         lemma = self.lemma
         if stem.needInfinitivusNN():
             lemma = u'n'+lemma
         if not self.isValidSuffixConcatenation(stem.ortho, lemma):
             lemma = u'A'+lemma
             stem.is_opening = True
         self.ortho = Phonology.interpolateVowels(stem.needSuffixPhonocode(), lemma)
    
     def getInvalidSuffixRegexList(self):
         return [r'lt,n',]

class Verbum(Wordform, iVerbal):
     mood = None
     tense = None
     definite = None
     numero = None
     person = None

     isPlusV = False
     isSZV = False
     isSZDV = False
     ikes = False

     # Szótári alak
     def getCitationForm(self):
         return self.conjugate(1, 3, 1, 0, 0)

     def conjugate(self, numero, person, mood, tense, definite):
         # 'ragoztam volna': morfológiai szó
         if mood == 2 and tense == -1:
             clone1 = self.appendSuffix(VerbalSuffixum1(numero, person, 1, tense, definite))
             clone2 = clone1.appendSuffix(VerbalSuffixum2(numero, person, 1, tense, definite))
             #morphoword = MorphoWord(Wordform('volna'), clone2)
             return clone2 + " volna"
         else:
             clone1 = self.appendSuffix(VerbalSuffixum1(numero, person, mood, tense, definite))
             clone2 = clone1.appendSuffix(VerbalSuffixum2(numero, person, mood, tense, definite))
             return clone2
    
     def makeNumPers(self, numero = 1, person = 3):
         return self.conjugate(numero, person, 1, 0, 0)
    
     def onBeforeSuffixation(self, suffix):
    
         if self.isPlusV and suffix.matchCase('..10.') and isinstance(suffix, VerbalSuffixum2):
             # @fixme this is a bit too complex. store the results in the lexicon instead?
             if (
                         suffix.matchCase('.1..0')
                     or (
                                     suffix.matchCase('....3')
                                 and not (self.needSuffixI() and suffix.matchCase('31...'))
                             and not (not self.needSuffixI() and suffix.matchCase('13...|3....'))
                     )):
                 self.ortho = self.lemma2
    
         if self.isSZV and isinstance(suffix, VerbalSuffixum1):
             if suffix.matchCase('..[23]..|...9.'):
                 self.ortho = self.lemma2
             #if suffix.matchCase('..20.'): # nn
             #if suffix.matchCase('..3..'): # gy, ggy
    
         if self.isSZV and isinstance(suffix, InfinitiveSuffixum):
             self.ortho = self.lemma2
    
         if self.isSZDV and isinstance(suffix, VerbalSuffixum1):
             if suffix.matchCase('..[23]..|...9.'):
                 self.ortho = self.lemma2
    
         if self.isSZDV and isinstance(suffix, InfinitiveSuffixum):
             self.ortho = self.lemma2
    
         # @fixme
         if self.lemma == u'alsz' and isinstance(suffix, VerbalSuffixum2):
             if suffix.matchCase('(13|3.)103'):
                 self.ortho = u'alusz'
    
         # @fixme
         if self.lemma == u'isz' and isinstance(suffix, VerbalSuffixum1):
             if suffix.matchCase('13190'):
                 self.ortho = u'iv'

         # @fixme
         if self.lemma == u'esz' and isinstance(suffix, VerbalSuffixum1):
             if suffix.matchCase('13190'):
                 self.ortho = u'ev'


     def isLastAffrSyb(self):
         char = Phonology.getLastConsonant(self.ortho)
         return Phonology.isAffrikate(char) or Phonology.isSybyl(char)

     def isLastT(self):
         char = Phonology.getLastConsonant(self.lemma)
         return (char == u't' or char == u'tt')


     def needNN(self):
         return self.isSZV

     def needTT(self):
         return (self.isPlusV or self.isSZV)

     # ha V+t, akkor ss,
     def needJss(self):
         last = Phonology.getLastConsonant(self.ortho)
         last1 = Phonology.getLastConsonant(self.ortho[0:-len(last)])
         return Phonology.isVowel(last1) and self.isLastT()

     def needJs(self):
         last = Phonology.getLastConsonant(self.ortho)
         last1 = Phonology.getLastConsonant(self.ortho[0:-len(last)])
         return not (Phonology.isVowel(last1) or Phonology.isAffrikate(last1) or Phonology.isSybyl(last1)) \
             and self.isLastT()

     def needJgy(self):
         return self.isSZV and not (self.lemma == u'hisz')

     def needJggy(self):
         return self.lemma == u'hisz'

     # zörej+j: zörejhez hasonul
     # ha zörej+t, akkor hasonul,
     def needJAssim(self):
         last = Phonology.getLastConsonant(self.ortho)
         if Phonology.isSybyl(last):
             return True
         last1 = Phonology.getLastConsonant(self.ortho[0:-len(last)])
         return (Phonology.isAffrikate(last1) or Phonology.isSybyl(last1)) \
             and self.isLastT()

     """
      * @todo gAt, _tAt, hAt: +Vtt
      * CC (Cnot =t): ingadozók
      * @todo lexikalizálni kell: is_vtt
      """
     def needVtt(self, suffix):
         if self.isLastT(): # mindig
             return True

         cons = Phonology.getLastConsonant(self.lemma)
         arr = [u'm', u'v', u'r', u's', u'ss', u't', u'tt', u'z', u'zz', u'zs', u'zzs']
         if cons in arr:
             if suffix.matchCase('13..0'):
                 return True
             else:
                 return False

         if self.lemma == u'isz':
             if suffix.matchCase('13190'):
                 return True

         if self.lemma == u'esz':
             if suffix.matchCase('13190'):
                 return True

         return False; # általában nem

     def makeInfinitive(self, numero=0, person=0):
         suffix = InfinitiveSuffixum(numero, person)
         return self.appendSuffix(suffix)

     # iVerbInfinitive {{{

     """
      * Érdekes, hogy a feltételes mód n-je és az infinitivus n-je is ugyanúgy duplázódik az SZV igéknél.
      """
     def needInfinitivusNN(self):
         return self.isSZV

     # tAt Műveltető
     def makeCausative(self):
         pass

     # gerund, -Ás
     def makeVerbalNoun(self):
         pass

     # -Ó
     # Ott / t
     # AndÓ
     def makeParticiple(self, tense):
        pass
    
     # -hAt
     def makeModal(self):
         return self.appendSuffix(GFactory.parseSuffixum(u'hAt'))
    
     # Igekötő
     def addParticle(self, particle):
        pass
    
     # auxiliaries: kell kellene kéne muszáj szabad tilos fog tud szokott
     def addAuxiliary(self, aux):
        pass

""" Valid nominal cases in hungarian.
"""
class iNominalCases(object):
    def makeCase(self, case):
        pass
    def makeNominativus(self):
        pass
    def makeAccusativus(self):
        pass
    def makeCausalisFinalis(self):
        pass
    def makeDativus(self):
        pass
    def makeInstrumentalis(self):
        pass
    def makeTranslativusFactivus(self):
        pass
    def makeFormativus(self):
        pass
    def makeEssivusFormalis(self):
        pass
    def makeIllativus(self):
        pass
    def makeInessivus(self):
        pass
    def makeElativus(self):
        pass
    def makeSublativus(self):
        pass
    def makeSuperessivus(self):
        pass
    def makeDelativus(self):
        pass
    def makeAllativus(self):
        pass
    def makeAdessivus(self):
        pass
    def makeAblativus(self):
        pass
    def makeTerminativus(self):
        pass

""" Invalid (virtual) nominal cases in hungarian.
 """
class iVirtualNominalCases(object):
     def makeGenitivus(self): pass
     def makeCausalis(self): pass
     #def makeExessivus()
     def makePerlativus(self): pass
     def makeProlativus(self): pass
     def makeVialis(self): pass
     def makeSubessivus(self): pass
     def makeProsecutivus(self): pass
     #def makeApudessivus()
     #def makeInitiativus()
     #def makeEgressivus()

""" Invalid (virtual) temporal cases in hungarian.
 """
class iVirtualTemporalCases(object):
    def makeAntessivus(self): pass
    def makeTemporalis(self): pass # -kor

class iPossessable(object):
    def isJaje(self):
        pass

class Nomen(Wordform, iPossessable, iNominalCases, iVirtualNominalCases, iNumPers):

     def __init__(self, lemma, ortho=None):
         super(Nomen, self).__init__(lemma, ortho)
         self.lemma2 = lemma
         self.case = 'Nominativus'
         self.numero = 1
         self.person = 3
         self.is_jaje = None
         self.is_familiar = False

     """ Hint.
      """
     def isJaje(self):
         if self.is_jaje is not None:
             return self.is_jaje; # már adott lexikonban
         if self.isLastVowel():
             return True # mindig
         if re.search('(s|sz|z|zs|c|cs|dzs|gy|j|ny|ty|tor|ter|er|um)$', self.ortho):
             return False # általában
         if re.search('[bcdfghjklmnprstvxz]{2,}$', self.ortho):
             return True # általában
         return False; # egyébként általában nem

     """ Nomen is alternating only if not yet inflexed.
      """
     def isAlternating(self):
         return self.is_alternating and (self.lemma == self.ortho)

     def isAMNYRight(self):
         return False

     def makePlural(self, familiar=False):
         clone = self.appendSuffix(GFactory.parseSuffixum('_Vk' if not familiar else u'ék'))
         clone.numero = 3
         clone.is_opening = True
         clone.is_familiar = True
         return clone

     def isSingular(self):
         return (self.numero == 1)

     def isPlural(self):
         return (self.numero > 1)

     # cases helpers {{{

     def _makeCaseFromNominativusWithSuffix(self, case, suffix):
         if self.isNominativus():
             clone = self.appendSuffix(suffix)
         else:
             clone = self.makeNominativus().appendSuffix(suffix)
         clone.case = case
         return clone

     def isNominativus(self):
         return (self.case == 'Nominativus')

     def isAccusativus(self):
         return (self.case == 'Accusativus')

     def makeCase(self, case):
         method = "makecase"
         if hasattr(self, method):
             return self.method()
         else:
             raise Exception("No such case: " + case)

     def makeNominativus(self):
         if self.isNominativus():
             return self.cloneAs(Nomen)
         clone = Nomen(self.lemma)
         if self.isPlural():
             return clone.makePlural(familiar=self.is_familiar)
         else:
             return clone

     def makeAccusativus(self):
         clone = self.makeNominativus().appendSuffix(GFactory.parseSuffixum(u'_Vt'))
         clone.case = 'Accusativus'
         return clone
         return self._makeCaseFromNominativusWithSuffix('Accusativus', GFactory.parseSuffixum(u'_Vt'))

     def makeCausalisFinalis(self):
         return self._makeCaseFromNominativusWithSuffix('CausalisFinalis', GFactory.parseSuffixum(u'ért'))

     def makeDativus(self):
         return self._makeCaseFromNominativusWithSuffix('Dativus', GFactory.parseSuffixum(u'nAk'))

     def makeInstrumentalis(self):
         return self._makeCaseFromNominativusWithSuffix('Instrumentalis', GFactory.parseSuffixum(u'vAl'))

     def makeTranslativusFactivus(self):
         return self._makeCaseFromNominativusWithSuffix('TranslativusFactivus', GFactory.parseSuffixum(u'vÁ'))

     def makeFormativus(self):
         return self._makeCaseFromNominativusWithSuffix('Formativus', GFactory.parseSuffixum(u'ként'))

     def makeEssivusFormalis(self):
         return self._makeCaseFromNominativusWithSuffix('EssivusFormalis', GFactory.parseSuffixum(u'Ul'))

     def makeIllativus(self):
         return self._makeCaseFromNominativusWithSuffix('Illativus', GFactory.parseSuffixum(u'bA'))

     def makeInessivus(self):
         return self._makeCaseFromNominativusWithSuffix('Inessivus', GFactory.parseSuffixum(u'bAn'))

     def makeElativus(self):
         return self._makeCaseFromNominativusWithSuffix('Elativus', GFactory.parseSuffixum(u'bÓl'))

     def makeSublativus(self):
         return self._makeCaseFromNominativusWithSuffix('Sublativus', GFactory.parseSuffixum(u'rA'))

     def makeSuperessivus(self):
         return self._makeCaseFromNominativusWithSuffix('Superessivus', GFactory.parseSuffixum(u'_On'))

     def makeDelativus(self):
         return self._makeCaseFromNominativusWithSuffix('Delativus', GFactory.parseSuffixum(u'rÓl'))

     def makeAllativus(self):
         return self._makeCaseFromNominativusWithSuffix('Allativus', GFactory.parseSuffixum(u'hOz'))

     def makeAdessivus(self):
         return self._makeCaseFromNominativusWithSuffix('Adessivus', GFactory.parseSuffixum(u'nÁl'))

     def makeAblativus(self):
         return self._makeCaseFromNominativusWithSuffix('Ablativus', GFactory.parseSuffixum(u'tÓl'))

     def makeTerminativus(self):
         return self._makeCaseFromNominativusWithSuffix('Terminativus', GFactory.parseSuffixum(u'ig'))

     # helpers {{{

     def _makeCaseWithNU(self, case, head):
         raise NotImplemented()
         ADVP = ADVP_NU(head, self.makeNominativus())
         ADVP.case = case
         return ADVP

     def _makeCaseWithHRHSZ(self, case, head, suffix):
         raise NotImplemented()
         ADVP = ADVP_HRHSZ(head, self.makeNominativus(), suffix)
         ADVP.case = case
         return ADVP

     def _makeCaseWithHNHSZ(self, case, head):
         raise NotImplemented()
         ADVP = ADVP_HNHSZ(head, self.makeNominativus())
         ADVP.case = case
         return ADVP

     def makeGenitivus(self):
         return self.makeDativus()

     def makeCausalis(self):
         return self._makeCaseWithNU('Causalis', GFactory.parseNP(u'miatt'))

     # @skipdef makeExessivus(self)

     def makePerlativus(self):
         return self._makeCaseWithHRHSZ('Perlativus', GFactory.parseNP(u'keresztül'), GFactory.parseSuffixum(u'On'))

     def makeProlativus(self):
         return self._makeCaseWithHRHSZ('Perlativus', GFactory.parseNP(u'át'), GFactory.parseSuffixum(u'On'))

     def makeVialis(self):
         return self.makeProlativus()

     def makeSubessivus(self):
         return self._makeCaseWithNU('Perlativus', GFactory.parseNP(u'alatt'))

     def makeProsecutivus(self):
         return self._makeCaseWithHNHSZ('Prosecutivus', GFactory.parseNP(u'mentén'))

     #def makeApudessivus()
     #def makeInitiativus()
     #def makeEgressivus()

     #def makeAntessivus()
     def makeTemporalis(self):
         return self._makeCaseFromNominativusWithSuffix('Temporalis', GFactory.parseSuffixum(u'kor'))


class AdjSuffixum(Suffixum):

     _input_class = 'Adj'
     _output_class = 'Adj'


class Adj(Nomen):

    def makeComparativus(self):
         if not (self.case == "Nominativus"):
             raise Exception('Adj Comparativus needs Nominativus')
         bb = GFactory.parseSuffixum(u'_Vbb').cloneAs(AdjSuffixum)
         A = self.appendSuffix(bb)
         A.case = 'Comparativus'
         return A

    def makeSuperlativus(self):
         if not (self.case == "Nominativus"):
             raise Exception('Adj Superlativus needs Nominativus')
         A = self.makeComparativus()
         # @todo prependPrefix()
         A.ortho = u'leg'+A.ortho
         A.case = 'Superlativus'
         return A

    def makeSuperlativus2(self):
         if not (self.case == "Nominativus"):
             raise Exception('Adj Superlativus2 needs Nominativus')
         A = self.makeSuperlativus()
         A.ortho = u'leges'+A.ortho
         A.case = 'Superlativus2'
         return A

     # @fixme english/latin name
    def kiemelo(self):
         if not (self.case == "Comparativus" or self.case == "Superlativus" or self.case == "Superlativus2"):
             raise Exception('Adj "kiemelo" needs Comparativus or Superlativus or Superlativus2')
         bb = GFactory.parseSuffixum(u'ik').cloneAs(AdjSuffixum)
         A = self.appendSuffix(bb)
         A.case = '+'
         return A


class iArgumented(object):
    def addArg(self, arg): pass


class HeadedExpression(iArgumented):
     case = None
     head = None
     arg = None

     def __init__(self, head, arg):
         self.head = head
         self.addArg(arg)

     def addArg(self, arg):
         self.arg = arg

     def pronominalize(self):
         raise Exception()

     def __str__():
         return '[' + str(self.head) + ' ' + self.arg + ']'


""" Morfológiai szó
 """
class MorphoWord(HeadedExpression):

    def __str__():
         return self.arg + ' ' + self.head


class ADVP_NU(HeadedExpression):

    def __str__():
         return str(self.arg) + ' ' + self.head

    def pronominalize(self):
         return self.head.appendSuffix(PossessiveSuffixum(self.arg.numero, 3))

class ADVP_HRHSZ(HeadedExpression):
     suffix = None

     def __init__(self, head, arg, suffix):
         super(ADVP_HRHSZ, self).__init__(head, arg)
         self.suffix = suffix

     def __str__():
         return self.arg.appendSuffix(self.suffix) + ' ' + self.head

class ADVP_HNHSZ(HeadedExpression):

     def __str__():
         return str(self.arg) + ' ' + self.head


"""
 * @pattern Action
 * @principle dependency injection: a konstruktornak adjunk mindent, ami kell
 """
class SyntaxAction(object):

     """
      * @pattern Template function, kötelező implementálni
      """
     def make(arg): pass


class SyntaxActionMakeCase(SyntaxAction):

    def __init__(self, case):
         self.case = case

    def make(self, arg):
         return arg.makeCase(self.case)


class SyntaxActionVerbDefault(SyntaxAction):

     context = None

     def __init__(self, context):
         self.context = context # Caseframe

     def make(self, arg):
         S = self.context.getArg('S')
         if S:
             return arg.conjugate(S.getNumero(), S.getPerson(), 1, 0, 0); # @todo just call makeNumPers(), leave other params
         else:
             raise Exception('No S for V')
         # or (1, 3)

""" @deprecated
 * A SyntaxActionMakeArg speciális esete.
 """
class SyntaxActionMakeNU(SyntaxAction):

    def __init__(self, lemma):
         self.lemma = lemma

    def make(self, arg):
         ADVP = ADVP_NU(GFactory.parseNP(self.lemma), arg)
         return ADVP

class SyntaxActionMakeArg(SyntaxAction):

    def __init__(self, host):
         self.host = host

    def make(self, arg):
         self.host.addArg(arg)
         return self.host

"""
 * @todo(HeadedExpression ?
 * @todo fának kell lennie, ld. [ágál vki [vmi ellen]]
 """
class Caseframe(object):

    relorder = 'VSO12'; # standard rel order

    """
      * @see msd: szeged_msd_tablak.rtf
    """
    def __init__(self, description):
        self.args = {}
        self.arg_action = {}
        self.defArg('V', SyntaxActionVerbDefault(self))
        self.argdef = description

    def defArg(self, rel, action):
        self.arg_action[rel] = action

    def setArg(self, rel, arg):
         if self.checkArg(rel, arg):
             self.args[rel] = arg
         else:
             raise Exception("Invalid or no arg_action for 'rel' arg 'arg' ".var_export(arg, 1))

    def getArg(self, rel):
         return self.args[rel]

    def checkArg(self, rel, arg):
         argdef = self.argdef[rel]
         if (empty(argdef)):
             return True
         if (get_class(arg) != argdef[0]):
             return False
         if get_class(arg) == 'Nomen':
             if (arg.case != argdef[1]):
                 return False
         if get_class(arg) == 'Verbum':
             if (arg.lemma != argdef[1]):
                 return False
         return True

    def makeArg(self, rel, arg):
         action = self.arg_action[rel]
         if isinstance(action, SyntaxAction):
             arg2 = action.make(arg, self)
             self.setArg(rel, arg2)
         else:
             self.setArg(rel, arg)
         return arg2

    def __str__():
        """
          * p. 30.
        """
        strs = []
        for rel in self.relorder:
            strs.append(str(self.getArg(rel)))
        return ' '.join([x for x in strs if x])

""" 
 * @todo
 * @pattern Composite
 """
class SyntaxTree(object):

    args = []

    def addArg(self, arg):
         self.args.append(arg)

    def __str__():
         strs = []
         for arg in self.args:
             strs.append(str(arg))
         return ' '.join([x for x in strs if x])

class GFactory(object):
    """
     * @todo Képzők
     *
     * N . N
     * _Vs s os as es ös
     * né né
     * kA ka ke
     * _VcskA cska cske ocska acska ecske öcske
     * féle féle
     *
     * N . ADJ
     * i i
     * _Vs s os es ös as ás és
     * _jÚ ú ű jú jű
     * ...
     *
     * V . N
     * Ás ás és
     * Ó ó ő
     *
     * V . ADJ
     * Ós ós ős
     * _AtlAn tlan tlen atlan etlen
     * tAlAn
     * hAtÓ ható hető
     * hAtAtlAn hatatlan hetetlen
     *
     * V . NV
     * ni
     * Ó ó ő
     * t t
     * Vtt tt ott ett ött
     * AndÓ andó endő
     * vA va ve
     *
     * V . V
     * _VgAt gat get ogat eget öget
     * _tAt at et tat tet
     * _tAtik 
     * ...
     """

    # full list
    N_vtmr_list = [
        u'híd', u'ín', u'nyíl', u'víz',
        u'szűz', u'tűz', u'fű', u'nyű',
        u'kút', u'lúd', u'nyúl', u'rúd', u'úr', u'út', u'szú',
        u'cső', u'kő', u'tő',
        u'ló',
        u'kéz', u'réz', u'mész', u'ész', u'szén', u'név', u'légy', u'ég', u'jég', u'hét', u'tér', u'dér', u'ér', u'bél', u'nyél', u'fél', u'szél', u'dél', u'tél', u'lé',
        u'nyár', u'sár',
        # A kéttagúak első mghja mindig rövid - egyszerűen az egész alakot lehet rövidíteni.
        u'egér', u'szekér', u'tenyér', u'kenyér', u'levél', u'fedél', u'fenék', u'kerék', u'cserép', u'szemét', u'elég', u'veréb', u'nehéz', u'tehén', u'derék',
        u'gyökér', u'kötél', u'közép',
        u'fazék',
        u'madár', u'szamár', u'agár', u'kanál', u'darázs', u'parázs',
        u'bogár', u'kosár', u'mocsár', u'mozsár', u'pohár', u'fonál',
        u'sugár', u'sudár',
        ]

    # @todo tő és toldalék elkülönítése: mít|osz, ennek konstruálásakor legyen lemma=mít, és legyen a "nominális toldalék" osz, képzéskor pedig nem a nominálisból, hanem a lemmából képezzünk. (?)
    # not full list
    N_btmr_list = [
        u'aktív', u'vízió', u'miniatűr', u'úr', u'fúzió', u'téma', u'szláv', u'privát',
        u'náció', u'analízis', u'mítosz', u'motívum', u'stílus',
        u'kultúra', u'múzeum', u'pasztőr', u'periódus', u'paródia',
        u'kódex', u'filozófia', u'história', u'prémium', u'szintézis',
        u'hérosz', u'matéria', u'klérus', u'május', u'banális',
        u'elegáns',
        ]

    # not full list
    # not opening e.g.: gáz bűz rés
    N_opening_list = [u'út', u'nyár', u'ház', u'tűz', u'víz', u'föld', u'könyv', u'zöld', u'nyúl', u'híd', u'nyíl', u'bátor', u'ajak', u'kazal', u'ló', u'hó', u'fű', u'hazai']

    # not full list
    N_jaje = {
        u'nagy': True,
        u'pad': True,
        u'sárkány': True,
        u'kupec': True,
        u'kortes': True,
        u'macesz': True,
        u'trapéz': True,
        u'rassz': True,
        u'miatt': False,
        }

    # is full list? latin/english name?
    N_alternating_list = {
        u'ajak': u'ajk',
        u'bagoly': u'bagly',
        u'bajusz': u'bajsz',
        u'bátor': u'bátr',
        u'dolog': u'dolg',
        u'haszon': u'haszn',
        u'izom': u'izm',
        u'kazal': u'kazl',
        u'lepel': u'lepl',
        u'majom': u'majm',
        u'piszok': u'piszk',
        u'torony': u'torny',
        u'tücsök': u'tücsk',
        u'tükör': u'tükr',
        u'tülök': u'tülk',
        u'vacak': u'vack',
        u'álom': u'álm',
        # v-vel bővülő tövek, nem teljes lista
        u'ló': u'lov',
        u'fű': u'füv',
        u'hó': u'hav',
        # hangátvetéses váltakozás, nem teljes lista
        u'teher': u'terh',
        u'pehely': u'pelyh',
        u'kehely': u'kelyh',
        }

    need_suffix_I_Nomen_list = {
        u'híd': False,
        u'nyíl': False,
        u'oxigén': True,
        u'valami': True,
        u'valaki': True,
        }

    @staticmethod
    def parseNP(string):
        if string == u'fia':
            return Fia(u'fia')
        obj = Nomen(string)
        obj.is_vtmr = string in GFactory.N_vtmr_list
        obj.is_btmr = string in GFactory.N_btmr_list
        obj.is_opening = string in GFactory.N_opening_list
        if string in GFactory.N_jaje:
            obj.is_jaje = GFactory.N_jaje[string]
        if string in GFactory.need_suffix_I_Nomen_list:
            obj.need_suffix_I = GFactory.need_suffix_I_Nomen_list[string]
        obj.is_alternating = string in GFactory.N_alternating_list
        if obj.is_alternating:
            obj.lemma2 = GFactory.N_alternating_list[string]
        return obj


    @staticmethod
    def parseADJ(string):
        obj = GFactory.parseNP(string).cloneAs(Adj)
        obj.is_opening = True; # a melléknevek túlnyomó többsége nyitótővű
        return obj

    # not full list
    suffixum_vtmr_list = [
        u'_Vk', # többesjel
        u'_Vt', # tárgyrag
        # birtokos személyragok
        u'Vs', # melléknévképző
        u'Az', # igeképző
        u'_VcskA', # kicsinyítő képző
        ]

    # not full list
    suffixum_btmr_list = [
        u'ista',
        u'izál',
        u'izmus',
        u'ikus',
        u'atív',
        u'itás',
        u'ális',
        u'íroz',
        u'nál', # ? fuzionál
        ]

    # is full list?
    suffixum_opening_list = [
        u'_Vk', # többesjel
        # birtokos személyjelek
        u'_Vbb', # középfok jele 
        # múlt idő jele 
        # felszólító j 
        ]

    suffixum_not_AMNY_right_list = [
        u'kor', u'ista', u'izmus', # stb. átlátszatlan toldalékok
        u'szOr', u'sÁg', u'i', u'ként',
        ]

    # is full list? latin/english name?
    suffixum_alternating_list = [
        u'_Vt', # tárgyrag
        u'On', # Superessivus
        u'_Vk', # többesjel
        # birtokos személyragok
        u'VstUl',
        u'Vs', # melléknévképző
        u'Vnként',
        u'_VcskA', # kicsinyítő képző
        ]

    suffixum_classes = {
        u'Ás': ['Verbum', 'Nomen'],
        u'Ul': ['Nomen', 'Verbum'],
        }

    suffixum_stop_jaje_list = [u'sÁg']

    @staticmethod
    def parseSuffixum(string, cls=Suffixum):
        obj = cls(string)
        obj.is_vtmr = string in GFactory.suffixum_vtmr_list
        obj.is_btmr = string in GFactory.suffixum_btmr_list
        obj.is_opening = string in GFactory.suffixum_opening_list
        obj.is_amny = not string in GFactory.suffixum_not_AMNY_right_list
        obj.is_alternating = string in GFactory.suffixum_alternating_list
        obj.stop_jaje = string in GFactory.suffixum_stop_jaje_list

        if string in GFactory.suffixum_classes:
            (_input_class, _output_class) = GFactory.suffixum_classes[string]
        else:
            _input_class = 'Nomen'
            _output_class = 'Nomen'
        obj._input_class = _input_class
        obj._output_class = _output_class
        return obj

    # vtmr verbs, not full list: 
    # ir-at sziv-attyú tür-elem bün-tet szur-ony buj-kál huz-at usz-oda szöv-és vag-dal
    V_btmr_list = [
            u'ír',
            u'szív',
            u'tűr',
            u'bűn',
            u'szúr',
            u'búj',
            u'húz',
            u'úsz',
            u'sző',
            u'vág',
            ]

    V_opening_list = [
            u'zöldül',
            ]

    # full list: lő nő sző fő ró
    plusV_list = {u'lő': u'löv', u'nő': u'növ', u'sző': u'szöv', u'fő': u'föv', u'ró': u'rov'}

    # full list: tesz lesz vesz hisz visz eszik iszik
    # @todo -Ó -Ás: evő, evés, alvó, alvás ; -ni: enni, aludni
    SZV_list = {u'tesz': u'te', u'lesz': u'le', u'vesz': u've', u'hisz': u'hi', u'visz': u'vi', u'esz': u'e', u'isz': u'i'}

    # @todo alszik ; -Ó -Ás: alvó, alvás ; -ni: aludni
    SZDV_list = {
            # @corpus sok -kVd(ik) képzős ige
            u'alsz': [u'alud', u'alv'],
            u'feksz': [u'feküd', u'fekv'],
            u'haragsz': [u'haragud', u'haragv'],
            u'cseleksz': [u'cseleked', u'cselekv'],
            u'dicseksz': [u'dicseked', u'dicsekv'],
            u'töreksz': [u'töreked', u'törekv'],
            # @corpus csak deverb és denom -Vd és -kOd képzős igék között
            u'öregsz': [u'öreged', u'öreged'],
            u'veszeksz': [u'veszeked', u'veszeked'],
            }

    # @corpus hangkivetéses igék: vándorol/vándorlunk
    # _Vl _Vz dVkVl _Vg képzős igék többsége, pl. vándorol, céloz, haldokol, mosolyog, és még söpör, sodor
    # u'szerez': u'szerző',
    # u'töröl': u'törlő',
    # u'becsül': u'becsl',
    # u'őriz': u'őrz',

    need_suffix_I_verb_list = {
        u'isz': False,
        }

    # @corpus -z képzős igék általában, sok -kVd(ik) képzős ige
    ikes = {
        u'esz': True,
        u'isz': True,
        u'alsz': True,
        u'feksz': True,
        u'haragsz': True,
        u'cseleksz': True,
        u'dicseksz': True,
        u'töreksz': True,
        u'öregsz': True,
        u'veszeksz': True,
        u'kardoskod': True,
        }

    @staticmethod
    def parseV(string):
        ikes = (string[-2:] == 'ik')
        if ikes:
            string = string[:-2]
        obj = Verbum(string)
        obj.setCase('13100')
        obj.is_btmr = string in GFactory.V_btmr_list
        obj.is_opening = string in GFactory.V_opening_list
        if obj.lemma in GFactory.plusV_list:
            obj.isPlusV = True
            obj.lemma2 = GFactory.plusV_list[obj.lemma]
        if obj.lemma in GFactory.SZV_list:
            obj.isSZV = True
            obj.lemma2 = GFactory.SZV_list[obj.lemma]
        if obj.lemma in GFactory.SZDV_list:
            obj.isSZDV = True
            obj.lemma2 = GFactory.SZDV_list[obj.lemma][0]
            obj.lemma3 = GFactory.SZDV_list[obj.lemma][1]
        if string in GFactory.need_suffix_I_verb_list:
            obj.need_suffix_I = GFactory.need_suffix_I_verb_list[string]
        if string in GFactory.ikes:
            obj.ikes = GFactory.ikes[string]
        elif ikes: # temporarily
            obj.ikes = True
        return obj

    @staticmethod
    def createCaseframe(description):
        return Caseframe(description)


class Fia(Nomen):

    def __init__(self, lemma, ortho=None):
        super(Fia, self).__init__(lemma, ortho)
        self.is_jaje = False

    def onBeforeSuffixation(self, suffix):
        if isinstance(suffix, PossessiveSuffixum):
            nums = (self.numero, self.person, suffix.numero, suffix.person, suffix.possessed_numero)
            if nums in [(1, 3, 1, 3, 1), (1, 3, 3, 3, 1)]:
                self.ortho = u'fi'
        else:
            super(Fia, self).onBeforeSuffixation(suffix)


import unittest

class Test (unittest.TestCase) :

    def testLexikon(self):
        N = GFactory.parseNP(u'ember');
        self.assertFalse(N.isVTMR());

        N = GFactory.parseNP(u'út');
        self.assertTrue(N.isVTMR());

        su = GFactory.parseSuffixum(u'_Vk');
        self.assertTrue(su.isVTMR());

        self.assertEquals(u'aktivista', str(GFactory.parseNP(u'aktív').appendSuffix(GFactory.parseSuffixum(u'ista'))))
        self.assertEquals(u'aktivizál', str(GFactory.parseNP(u'aktív').appendSuffix(GFactory.parseSuffixum(u'izál'))))
        self.assertEquals(u'aktivizmus', str(GFactory.parseNP(u'aktív').appendSuffix(GFactory.parseSuffixum(u'izmus'))))
        self.assertEquals(u'aktivitás', str(GFactory.parseNP(u'aktív').appendSuffix(GFactory.parseSuffixum(u'itás'))))
        self.assertEquals(u'miniatürizál', str(GFactory.parseNP(u'miniatűr').appendSuffix(GFactory.parseSuffixum(u'izál'))))
        self.assertEquals(u'urizál', str(GFactory.parseNP(u'úr').appendSuffix(GFactory.parseSuffixum(u'izál'))))
        self.assertEquals(u'fuzionál', str(GFactory.parseNP(u'fúzió').appendSuffix(GFactory.parseSuffixum(u'nál'))))
        self.assertEquals(u'szlavista', str(GFactory.parseNP(u'szláv').appendSuffix(GFactory.parseSuffixum(u'ista'))))
        self.assertEquals(u'privatizál', str(GFactory.parseNP(u'privát').appendSuffix(GFactory.parseSuffixum(u'izál'))))

    def testPlural(self):
        cases = [
                (u'ember', u'emberek'),
                (u'föld', u'földek'),
                (u'könyv', u'könyvek'),
                (u'út', u'utak'),
                (u'nyár', u'nyarak'),
                (u'ház', u'házak'),
                (u'gáz', u'gázok'),
                (u'tök', u'tökök'),
                # todo (u'férfi', u'férfiak'),
                ]
        for singular, plural in cases:
            self.assertEqual(plural, GFactory.parseNP(singular).makePlural().ortho)

    def checkPossessive(self, form, lemma, num, pers):
        self.assertEquals(form, str(GFactory.parseNP(lemma).appendSuffix(PossessiveSuffixum(num, pers))))

    def checkPossessives(self, lemma, forms):
        i = 0
        for num in [1, 3]:
            for pers in [1, 2, 3]:
                self.checkPossessive(forms[i], lemma, num, pers)
                i += 1

    def testPossessive(self):
        self.assertEquals(u'katonasága', str(GFactory.parseNP(u'katona').appendSuffix(GFactory.parseSuffixum(u'sÁg', NomenSuffixum)).appendSuffix(PossessiveSuffixum(1, 3))))
        self.checkPossessives(u'barnulás', [u'barnulásom', u'barnulásod', u'barnulása', u'barnulásunk', u'barnulásotok', u'barnulásuk'])
        self.checkPossessives(u'pad', [u'padom', u'padod', u'padja', u'padunk', u'padotok', u'padjuk'])

        self.checkPossessive(u'ladája', u'lada', 1, 3)
        self.checkPossessive(u'ládája', u'láda', 1, 3)
        self.checkPossessive(u'ládánk', u'láda', 3, 1)
        self.checkPossessive(u'bikája', u'bika', 1, 3)
        self.checkPossessive(u'bikánk', u'bika', 3, 1)
        self.checkPossessive(u'királya', u'király', 1, 3)
        self.checkPossessive(u'olaja', u'olaj', 1, 3)
        self.checkPossessive(u'báránya', u'bárány', 1, 3)
        self.checkPossessive(u'sasa', u'sas', 1, 3)
        self.checkPossessive(u'perece', u'perec', 1, 3)
        self.checkPossessive(u'nagyja', u'nagy', 1, 3)
        self.checkPossessive(u'sárkányja', u'sárkány', 1, 3)
        self.checkPossessive(u'kupecje', u'kupec', 1, 3)
        self.checkPossessive(u'kortesje', u'kortes', 1, 3)
        self.checkPossessive(u'maceszje', u'macesz', 1, 3)
        self.checkPossessive(u'trapézja', u'trapéz', 1, 3)
        self.checkPossessive(u'rasszja', u'rassz', 1, 3)
        self.checkPossessive(u'padja', u'pad', 1, 3)
        self.checkPossessive(u'embere', u'ember', 1, 3)
        self.checkPossessive(u'szenátora', u'szenátor', 1, 3)
        self.checkPossessive(u'minisztere', u'miniszter', 1, 3)
        self.checkPossessive(u'slágere', u'sláger', 1, 3)
        self.checkPossessive(u'jubileuma', u'jubileum', 1, 3)
        self.checkPossessive(u'galambja', u'galamb', 1, 3)
        self.checkPossessive(u'kertje', u'kert', 1, 3)
        self.checkPossessive(u'barackja', u'barack', 1, 3)
        self.checkPossessive(u'csontja', u'csont', 1, 3)
        self.checkPossessive(u'fánkja', u'fánk', 1, 3)
        self.checkPossessive(u'gondja', u'gond', 1, 3)
        self.checkPossessive(u'futballja', u'futball', 1, 3)
        self.checkPossessive(u'címzettje', u'címzett', 1, 3)
        self.checkPossessive(u'sakkja', u'sakk', 1, 3)
        self.checkPossessive(u'cseppje', u'csepp', 1, 3)

    def checkPossPoss(self, form, lemma, a, b, c, d):
        self.assertEquals(form, str(GFactory.parseNP(lemma).appendSuffix(PossessiveSuffixum(a, b, c)).appendSuffix(PossessorSuffixum(d))))

    def checkPossessor(self, form, lemma, d):
        self.assertEquals(form, str(GFactory.parseNP(lemma).appendSuffix(PossessorSuffixum(d))))

    def testPossessor(self):
        self.checkPossPoss(u'őseimé', u'ős', 1, 1, 3, 1)
        self.checkPossPoss(u'őseidéi', u'ős', 1, 2, 3, 3)
        self.checkPossPoss(u'őseié', u'ős', 1, 3, 3, 1)
        self.checkPossPoss(u'őseiéi', u'ős', 1, 3, 3, 3)
        self.checkPossPoss(u'házaimé', u'ház', 1, 1, 3, 1)
        self.checkPossPoss(u'házaiméi', u'ház', 1, 1, 3, 3)
        self.checkPossPoss(u'házaié', u'ház', 1, 3, 3, 1)
        self.checkPossessor(u'Vargáé', u'Varga', 1)

    def testiVerbal(self):
        V = GFactory.parseV(u'olvas');
        self.assertTrue(V.matchCase('13100'));
        self.assertTrue(V.conjugate(1, 1, 1, 0, 0).matchCase('11100'));
        self.assertTrue(V.conjugate(1, 2, 3, 0, 3).matchCase('.23.[23]'));
        self.assertTrue(V.conjugate(3, 2, 1, 0, 0).matchCase('13100|32100'));
        self.assertTrue(V.conjugate(1, 1, 1, -1, 0).matchCase('..[23]..|...9.'));

    def testInfinitiveConjugation(self):
        self.checkInfinitiveConjugation(u'olvas', [u'olvasni', u'olvasnom', u'olvasnod', u'olvasnia', u'olvasnunk', u'olvasnotok', u'olvasniuk']);
        self.checkInfinitiveConjugation(u'tesz', [u'tenni', u'tennem', u'tenned', u'tennie', u'tennünk', u'tennetek', u'tenniük'])
        self.checkInfinitiveConjugation(u'hisz', [u'hinni', u'hinnem', u'hinned', u'hinnie', u'hinnünk', u'hinnetek', u'hinniük'])
        self.checkInfinitiveConjugation(u'esz', [u'enni', u'ennem', u'enned', u'ennie', u'ennünk', u'ennetek', u'enniük'])
        self.checkInfinitiveConjugation(u'isz', [u'inni', u'innom', u'innod', u'innia', u'innunk', u'innotok', u'inniuk'])
        self.checkInfinitiveConjugation(u'űz', [u'űzni', u'űznöm', u'űznöd', u'űznie', u'űznünk', u'űznötök', u'űzniük'])
        self.checkInfinitiveConjugation(u'költ', [u'költeni', u'költenem', u'költened', u'költenie', u'költenünk', u'költenetek', u'költeniük'])
        self.checkInfinitiveConjugation(u'lő', [u'lőni', u'lőnöm', u'lőnöd', u'lőnie', u'lőnünk', u'lőnötök', u'lőniük'])
        self.checkInfinitiveConjugation(u'ró', [u'róni', u'rónom', u'rónod', u'rónia', u'rónunk', u'rónotok', u'róniuk'])
        self.checkInfinitiveConjugation(u'alsz', [u'aludni', u'aludnom', u'aludnod', u'aludnia', u'aludnunk', u'aludnotok', u'aludniuk'])

    def testVerbConjugation(self):
        self.checkConjugation(u'olvas', [
            u'olvasok', u'olvasol', u'olvas', u'olvasunk', u'olvastok', u'olvasnak',
            u'olvasom', u'olvasod', u'olvassa', u'olvassuk', u'olvassátok', u'olvassák',
            u'', u'olvastál', u'olvasott', u'olvastunk', u'olvastatok', u'olvastak', # todo u'olvastam'
            u'', u'olvastad', u'olvasta', u'olvastuk', u'olvastátok', u'olvasták', # todo u'olvastam'
            u'olvasnék', u'olvasnál', u'olvasna', u'olvasnánk', u'olvasnátok', u'olvasnának',
            u'olvasnám', u'olvasnád', u'olvasná', u'olvasnánk', u'olvasnátok', u'olvasnák',
            u'olvassak', u'olvassál', u'olvasson', u'olvassunk', u'olvassatok', u'olvassanak',  # todo olvass
            u'olvassam', u'olvassad', u'olvassa', u'olvassuk', u'olvassátok', u'olvassák', # todo olvasd
            u'olvaslak', u'olvastalak', u'olvasnálak', u'olvassalak',
            ]
        )

    def checkInfinitiveConjugation(self, lemma, verbforms):
        conjugations = [[0, 0], [1, 1], [1, 2], [1, 3], [3, 1], [3, 2], [3, 3]]
        V = GFactory.parseV(lemma)
        i = 0
        for conjugation in conjugations:
            if not verbforms[i]:
                continue;
            expected = verbforms[i]
            actual = str(V.makeInfinitive(* conjugation))
            self.assertEquals(expected, actual)
            i += 1


    def checkConjugation(self, lemma, verbforms):
        conjugations = [
            [1, 1, 1, 0, 0],
            [1, 2, 1, 0, 0],
            [1, 3, 1, 0, 0],
            [3, 1, 1, 0, 0],
            [3, 2, 1, 0, 0],
            [3, 3, 1, 0, 0],

            [1, 1, 1, 0, 3],
            [1, 2, 1, 0, 3],
            [1, 3, 1, 0, 3],
            [3, 1, 1, 0, 3],
            [3, 2, 1, 0, 3],
            [3, 3, 1, 0, 3],

            [1, 1, 1, -1, 0],
            [1, 2, 1, -1, 0],
            [1, 3, 1, -1, 0],
            [3, 1, 1, -1, 0],
            [3, 2, 1, -1, 0],
            [3, 3, 1, -1, 0],

            [1, 1, 1, -1, 3],
            [1, 2, 1, -1, 3],
            [1, 3, 1, -1, 3],
            [3, 1, 1, -1, 3],
            [3, 2, 1, -1, 3],
            [3, 3, 1, -1, 3],

            [1, 1, 2, 0, 0],
            [1, 2, 2, 0, 0],
            [1, 3, 2, 0, 0],
            [3, 1, 2, 0, 0],
            [3, 2, 2, 0, 0],
            [3, 3, 2, 0, 0],

            [1, 1, 2, 0, 3],
            [1, 2, 2, 0, 3],
            [1, 3, 2, 0, 3],
            [3, 1, 2, 0, 3],
            [3, 2, 2, 0, 3],
            [3, 3, 2, 0, 3],

            [1, 1, 3, 0, 0],
            [1, 2, 3, 0, 0],
            [1, 3, 3, 0, 0],
            [3, 1, 3, 0, 0],
            [3, 2, 3, 0, 0],
            [3, 3, 3, 0, 0],

            [1, 1, 3, 0, 3],
            [1, 2, 3, 0, 3],
            [1, 3, 3, 0, 3],
            [3, 1, 3, 0, 3],
            [3, 2, 3, 0, 3],
            [3, 3, 3, 0, 3],
            [1, 1, 1, 0, 2],
            [1, 1, 1, -1, 2],
            [1, 1, 2, 0, 2],
            [1, 1, 3, 0, 2],
        ]

        V = GFactory.parseV(lemma)
        i = 0
        for conjugation in conjugations:
            if not verbforms[i]:
                continue;
            expected = verbforms[i]
            actual = str(V.conjugate(* conjugation))
            self.assertEquals(expected, actual)
            i += 1


if __name__ == '__main__':
    iSuffixumMorphology()
    iSuffixumPhonology()
    Suffixum()
    aVerbalSuffixum(1, 3, 1, 0, 0)
    iNumPers()
    iVerbal()
    VerbalSuffixum1(1, 3, 1, 0, 0)
    VerbalSuffixum2(1, 3, 1, 0, 0)
    InfinitiveSuffixum(1, 3, 1, 0, 0)
    Verbum()
    iNominalCases()
    iVirtualNominalCases()
    iVirtualTemporalCases()
    iPossessable()
    Nomen(u'ember', u'ember')
    AdjSuffixum()
    Adj(u'emberes')
    iArgumented()
    HeadedExpression(u'volna', u'<ige>')
    MorphoWord(u'volna', u'<ige>')
    ADVP_NU(u'<head>', u'<arg>')
    ADVP_HRHSZ(u'<head>', u'<arg>', u'<suffix>')
    ADVP_HNHSZ(u'<head>', u'<arg>')
    SyntaxAction()
    SyntaxActionMakeCase('Nominativus')
    SyntaxActionVerbDefault(Caseframe('<desc>'))
    SyntaxActionMakeNU(u'mellett')
    SyntaxActionMakeArg(u'<host>')
    Caseframe('<desc>')
    SyntaxTree()
    GFactory()

    import sys
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
    unittest.main()
