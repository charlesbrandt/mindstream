#!/bin/bash
# This is an example launch script. 
# It should be easy to tailor this to various workspaces.

python /c/mindstream/mindstream/launch.py -c /c/mindstream todo

echo "See also:
python /c/mindstream/mindstream/launch.py -c /c/mindstream code

python /c/mindstream/mindstream/launch.py -c /c/mindstream tagger

cd pose
./launch.sh

cd editor
./launch.sh
"
