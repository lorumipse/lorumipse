from __future__ import print_function
from collections import defaultdict
import random


class NGram(object):
    separator = "#"

    def __init__(self, n, sequences):
        self.ngram_order = n-1
        self.ngram_distr = self.calc_ngram_distr(n, sequences)
        self.trans_prob = self.calc_trans_prob(self.ngram_distr)

    def generate_token(self):
        work_hist = (self.separator,)
        i = 0
        while True:
            token = self.choose(self.trans_prob[len(work_hist)][work_hist])
            yield token
            if token == self.separator:
                work_hist = (self.separator,)
            else:
                work_hist = self.add_to_history(work_hist, token, self.ngram_order)
            i += 1

    def generate_sequences(self, n_sequences=None):
        seq = []
        i = 0
        if n_sequences == 0:
            return
        for sym in self.generate_token():
            if sym == self.separator:
                yield seq
                seq = []
                i += 1
                if i == n_sequences:
                    return
            else:
                seq.append(sym)

    def dump(self):
        for order in self.ngram_distr:
            for gram, freq in order.iteritems():
                print(gram, freq)
        for order in self.trans_prob:
            for gram, freq in order.iteritems():
                print(gram, freq)

    def calc_ngram_distr(self, n, sequences):
        distrib = []
        for order in range(n):
            distrib.append(defaultdict(int))
        for seq in sequences:
            history = ()
            # separator special case: equals to number of sequences
            distrib[0][(self.separator,)] += 1
            for token in [self.separator] + list(seq) + [self.separator]:
                for order in range(len(history)+1):
                    if order == 0:
                        order_history = ()
                    else:
                        order_history = history[-order:]
                    if order != 0 or token != self.separator:
                        distrib[order][(order_history + (token,))] += 1
                history = self.add_to_history(history, token, n-1)
        return distrib

    @staticmethod
    def add_to_history(old_history, new_token, n):
        return (old_history + (new_token,))[-n:]

    def calc_trans_prob(self, distr):
        total = sum([freq for ngram, freq in distr[0].iteritems() if ngram != (self.separator,)])
        trans_prob = []
        for order, order_distr in enumerate(distr):
            order_trans_distr = defaultdict(lambda: defaultdict(int))
            for ngram, freq in order_distr.iteritems():
                hist = ngram[:-1]
                item = ngram[-1]
                norm_fact = total if order == 0 else distr[order-1][hist]
                order_trans_distr[hist][item] = float(freq) / norm_fact
            trans_prob.append(order_trans_distr)
        return trans_prob

    @staticmethod
    def choose(distrib):
        rnd = random.random()
        cumul_prob = 0
        for token, prob in distrib.iteritems():
            cumul_prob += prob
            if cumul_prob > rnd:
                return token
        return token

