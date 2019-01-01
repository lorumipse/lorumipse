#!/bin/bash

script_dir=$(dirname $0)
root_dir=$script_dir/..
(sleep 5; python -m webbrowser -t http://localhost:9999/) &
export PYTHONPATH="$root_dir"
"$root_dir/webapp/server.py"
