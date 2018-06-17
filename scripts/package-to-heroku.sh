#!//bin/bash

TARGET="${1:-heroku-deploy}"

if [ "$2" == "-quick" ]; then
    QUICK=1
fi

TO_INSTALL=(runtime.txt langmodel webapp requirements.txt Procfile resource/dt-*)

if [ -z $QUICK ]; then
    TO_INSTALL+=(build)
    rm -rf $TARGET/*
fi

mkdir -p $TARGET

for source in ${TO_INSTALL[@]}; do
	target_dir=$TARGET/$(dirname "$source")
	mkdir -p "$target_dir"
    cp -a "$source" "$target_dir"/
done
