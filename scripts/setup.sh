#!/bin/bash

script_dir=$(dirname $0)
root_dir=$script_dir/..
template_dir=build/text_template

rm -r "$template_dir"
mkdir -p "$template_dir"
gzcat $root_dir/resource/sg3_nom_acc_sentences_xaa.txt.gz | $script_dir/split_corpus.py "$template_dir/"
