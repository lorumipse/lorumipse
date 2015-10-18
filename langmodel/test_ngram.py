import unittest
from ngram import NGram

class NGramTestCase(unittest.TestCase):
    def setUp(self):
        self.text = "abraka dabra, abrak a dobra, ablak a dubra"
        self.trigram = NGram(3, self.text)

    def test_calc_distr(self):
        self.assertEqual(self.trigram.ngram_order, 2)
        ngram_distr = self.trigram.ngram_distr
        (unigram_distr, bigram_distr, trigram_distr) = ngram_distr
        self.assertEqual(unigram_distr[('l',)], self.count_ngram('l', self.text))
        self.assertEqual(bigram_distr[(',',' ')], self.count_ngram(', ', self.text))
        self.assertEqual(trigram_distr[('b', 'r', 'a')], self.count_ngram('bra', self.text))

    def test_calc_trans_prob(self):
        trans_prob = self.trigram.trans_prob
        self.assertEqual(trans_prob[0][()]['a'], float(self.count_ngram('a', self.text)) / len(self.text))
        self.assertEqual(trans_prob[2][('a', 'b')]['l'], float(self.count_ngram('abl', self.text)) / self.count_ngram('ab', self.text))

    def test_generate(self):
        text = list(self.trigram.generate(1000))
        self.assertTrue(self.count_ngram("br", "".join(text)) > 0)

    def test_generate_with_history(self):
        text = list(self.trigram.generate(1000, ", "))
        self.assertTrue(self.count_ngram("br", "".join(text)) > 0)
        self.assertTrue(text[0] == 'a')

    def count_ngram(self, ngram, text):
        n = len(ngram)
        cnt = 0
        for i in xrange(len(text)-n+1):
            if text[i:i+n] == ngram:
                cnt += 1
        return cnt
        
    def tearDown(self):
        pass

