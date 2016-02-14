#!/bin/bash

script_dir=$(dirname $0)
root_dir=$script_dir/..
template_dir=build/text_template
corpus_file=${1:-$root_dir/resource/sg3_nom_acc_sentences_xaa.txt.gz}

cd $root_dir

if [ ! -d virtualenv ]; then
    virtualenv virtualenv
    . ./virtualenv/bin/activate
    pip install -r requirements.txt
else
	. ./virtualenv/bin/activate
fi

rm -r "$template_dir"
mkdir -p "$template_dir"
gzcat -f $corpus_file | $script_dir/split_corpus.py "$template_dir/"
cp $root_dir/resource/init_sentence_template.txt "$template_dir/init.txt"
