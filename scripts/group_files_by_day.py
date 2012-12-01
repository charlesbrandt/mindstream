#!/usr/bin/env python
"""
#
# Description:
# script to run through a supplied directory's files
# create sub-directories that correspond to the day of the files' timestamps
# move the files to their corresponding day subdirectory
# in the new_dir destination

# By: Charles Brandt [code at contextiskey dot com]
# On: *2009.08.18 21:50:51 
# License:  MIT

# Requires: moments
#

$Id$ (???)
"""
import sys

#import os, subprocess
#from moments.node import Image, make_node
#from moments.path import Path
#from moments.tags import Tags

# functionality moved to mindstream.import_media
from mindstream.import_media import group_by_day

def main():
    if len (sys.argv) > 1:
        if sys.argv[1] in ['--help','help'] or len(sys.argv) < 2:
            usage()
        f1 = sys.argv[1]
        print f1
        group_by_day(f1)
        
if __name__ == '__main__':
    main()
