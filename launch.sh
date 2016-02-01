#!/bin/bash
# This is an example launch script. 
# It should be easy to tailor this to various workspaces.

export ROOT=/c/public/mindstream
launch.py -c $ROOT todo

echo "See also:
launch.py -c $ROOT code

launch.py -c $ROOT tagger

cd pose
./launch.sh

cd editor
./launch.sh
"
