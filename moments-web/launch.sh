#!/bin/bash
# This is an example launch script. 
# It should be easy to tailor this to various workspaces.

python /c/mindstream/mindstream/launch.py -c /c/moments-web todo moments
#app tipfy

echo "python /c/mindstream/mindstream/launch.py -c /c/moments-web setup"
echo ""

echo "cd /c/moments-web"
echo "/c/downloads/python/google_appengine/dev_appserver.py --port 8081 application/"
echo ""

echo "firefox -browser"
echo "firefox http://localhost:8081/"
echo ""
echo "/c/downloads/python/google_appengine/appcfg.py update application/"
