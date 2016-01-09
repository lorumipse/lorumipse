#!/usr/bin/env python

import os
import random
import sys
import codecs
from gibberize import gibberize_file


def choose_random_file(dir):
    files = os.listdir(dir)
    file = random.choice(files)
    return os.path.join(dir, file)


def generate_text(dir):
    template = choose_random_file(dir)
    with codecs.open(template, 'r', 'utf-8') as f:
        sentences = gibberize_file(f)
        text = " ".join([" ".join(sentence) for sentence in sentences])
        return text


if __name__ == '__main__':
    template_dir = sys.argv[1]
    print generate_text(template_dir)
