#!/bin/bash
# This is an example launch script. 
# It should be easy to tailor this to various workspaces.

python /c/mindstream/mindstream/launch.py -c /c/mindstream/pose code
python /c/mindstream/mindstream/launch.py -c /c/mindstream/pose views

echo "other common options:
python /c/mindstream/mindstream/launch.py -c /c/technical javascript

python /c/mindstream/mindstream/launch.py -c /c/mindstream/pose todo
"

#echo "python /c/moments/moments/server.py /c/journal" 

#echo "python /c/mindstream/pose/application-split.py -c /c/journal"

echo "#so script can find templates relative to script:"
echo "cd /c/mindstream/pose"
echo "python application.py -c /c/journal

http://localhost:8088/"
