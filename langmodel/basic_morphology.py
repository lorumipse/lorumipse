# -*- coding: utf-8 -*-

import re

ADD = 0
DELETE_MATCH = 1

ACC_RULES = [
    (u"a", u"át", DELETE_MATCH),
    (u"e", u"ét", DELETE_MATCH),
    (u"o", u"ót", DELETE_MATCH),
    (ur"[aáoóuú][^eéö]*(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", u"ot", ADD),
    (ur"[öőüű][^aáeéiíoóuú]*(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", u"öt", ADD),
    (ur"(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", u"et", ADD),
    ("", u"t", ADD)
]


def affix(stem, ana):
    if ana == "NOUN<ACC>":
        return apply_acc_rules(stem)
    else:
        return stem


def det(word):
    if re.match(ur"^[aáeéiíoóöőuúüű]", word.lower()):
        return u"az"
    else:
        return u"a"


def apply_acc_rules(stem):
    for pattern, suffix, operation in ACC_RULES:
        match = re.search(pattern + "$", stem)
        if match:
            if operation == DELETE_MATCH:
                return stem[:match.start()] + suffix
            elif operation == ADD:
                return stem + suffix
            else:
                raise ValueError(("invalid operation", operation))
