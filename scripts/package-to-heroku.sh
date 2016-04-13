#!//bin/bash

TARGET="${1:-heroku-deploy}"
TO_INSTALL=(build langmodel webapp requirements.txt Procfile resource/dt-*)

rm -rf $TARGET/*
mkdir -p $TARGET

for source in ${TO_INSTALL[@]}; do
	target_dir=$TARGET/$(dirname "$source")
	mkdir -p "$target_dir"
    cp -a "$source" "$target_dir"/
done
