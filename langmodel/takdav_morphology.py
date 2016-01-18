from scratch import GFactory

def affix(stem, ana):
    if ana == "NOUN<CAS<ACC>>":
        return GFactory.parseNP(stem).makeAccusativus().ortho
    else:
        return stem
