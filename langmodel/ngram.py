from collections import defaultdict
import random

class NGram(object):
    def __init__(self, n, tokens):
        self.ngram_order = n-1
        self.ngram_distr = self.calc_ngram_distr(n, tokens)
        self.trans_prob = self.calc_trans_prob(self.ngram_distr)

    def generate(self, length=None, history=()):
        work_hist = tuple(history[:])
        i = 0
        while True if length == None else i < length:
            token = self.choose(self.trans_prob[len(work_hist)][work_hist])
            yield token
            work_hist = self.add_to_history(work_hist, token, self.ngram_order)
            i += 1

    def generate_sequences(self, sep, length=None, history=()):
        seq = []
        i = 0
        if length == 0:
            return
        for sym in self.generate(history=(sep)):
            if sym == sep:
                yield seq
                seq = []
                i += 1
                if i == length:
                    return
            else:
                seq.append(sym)

    def calc_ngram_distr(self, n, tokens):
        distrib = []
        for order in range(n):
            distrib.append(defaultdict(int))
        history = ()
        for token in tokens:
            for order in range(len(history)+1):
                if order == 0:
                    order_history = ()
                else:
                    order_history = history[-order:]
                distrib[order][(order_history + (token,))] += 1
            history = self.add_to_history(history, token, n-1)
        return distrib

    @staticmethod
    def add_to_history(old_history, new_token, n):
        return (old_history + (new_token,))[-n:]

    @staticmethod
    def calc_trans_prob(distr):
        total = sum(distr[0].values())
        trans_prob = []
        for order, order_distr in enumerate(distr):
            norm_order_distr = {}
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

