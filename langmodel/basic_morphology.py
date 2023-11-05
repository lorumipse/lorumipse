import re

ADD = 0
DELETE_MATCH = 1

ACC_RULES = [
    ("a", "át", DELETE_MATCH),
    ("e", "ét", DELETE_MATCH),
    ("o", "ót", DELETE_MATCH),
    (r"[aáoóuú][^eéö]*(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", "ot", ADD),
    (r"[öőüű][^aáeéiíoóuú]*(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", "öt", ADD),
    (r"(b|c|cs|d|f|g|gy|h|k|m|p|t|ty|v|x)", "et", ADD),
    ("", "t", ADD)
]


def affix(stem, ana):
    if ana == "NOUN<CAS<ACC>>":
        return apply_acc_rules(stem)
    else:
        return stem


def det(word):
    if re.match(r"^[aáeéiíoóöőuúüű]", word.lower()):
        return "az"
    else:
        return "a"


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
