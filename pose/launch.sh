#!/bin/bash
# This is an example launch script. 
# It should be easy to tailor this to various workspaces.

launch.py -c /c/public/mindstream/pose code
launch.py -c /c/public/mindstream/pose views

echo "other common options:
launch.py -c /c/technical javascript

launch.py -c /c/public/mindstream/pose todo
"

#echo "python /c/moments/moments/server.py /c/journal" 

#echo "python /c/mindstream/pose/application-split.py -c /c/journal"

echo "#so script can find templates relative to script:"
#echo "cd /c/mindstream/pose"


echo "
#new tab:
cd /c/public/sortable_list/web
python application.py -c /c/journal

#new browser
http://localhost:8088/
"
