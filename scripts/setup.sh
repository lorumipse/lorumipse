#!/bin/bash

script_dir=$(dirname $0)
root_dir=$script_dir/..
template_dir=build/text_template

mkdir -p $template_dir
gzcat $root_dir/resource/sg3_nom_acc_sentences_xaa.txt.gz | head -1000 | $script_dir/split_corpus.py $template_dir/
