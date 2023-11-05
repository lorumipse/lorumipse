#!/bin/bash

script_dir=$(dirname $0)
root_dir=$script_dir/..
template_dir=build/text_template
corpus_file=${1:-$root_dir/resource/non-pers12-xaa-10m.txt.gz}

cd $root_dir

if [ ! -d venv ]; then
    python3 -m venv venv
    . ./venv/bin/activate
    pip3 install -r requirements.txt
else
	. ./venv/bin/activate
fi

rm -rf "$template_dir"
mkdir -p "$template_dir"
gzcat -f $corpus_file | $script_dir/split_corpus.py "$template_dir/"
cp $root_dir/resource/init_sentence_template.txt "$template_dir/init.txt"
