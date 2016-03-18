#!/bin/bash -x

script_dir=$(dirname $0)
root_dir=$script_dir/..
"$root_dir/webapp/server.py"
