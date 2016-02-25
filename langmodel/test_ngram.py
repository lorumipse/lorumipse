import unittest
import itertools
from ngram import NGram


class NGramTestCase(unittest.TestCase):
    def setUp(self):
        self.text = ["abraka dabra", "abrak a dobra", "ablak a dubra"]
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
        self.assertEqual(trans_prob[0][()]['a'], float(self.count_ngram('a', self.text)) / self.total_seqs_length(self.text))
        self.assertEqual(trans_prob[1][('#',)]['a'], 1)
        self.assertEqual(trans_prob[2][('a', 'b')]['l'], float(self.count_ngram('abl', self.text)) / self.count_ngram('ab', self.text))

    def test_generate(self):
        text = list(itertools.islice(self.trigram.generate_token(), 1000))
        self.assertTrue(self.count_ngram("br", ["".join(text)]) > 0)

    def count_ngram(self, ngram, seqs):
        n = len(ngram)
        cnt = 0
        for seq in seqs:
            separated_seq = ["#"] + list(seq) + ["#"]
            for i in xrange(len(separated_seq)-n+1):
                if tuple(separated_seq[i:i+n]) == tuple(ngram):
                    cnt += 1
        return cnt

    def total_seqs_length(self, seqs):
        s = sum([len(seq) for seq in seqs])
        return s
        
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
