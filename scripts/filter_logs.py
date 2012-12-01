#!/usr/bin/env python
"""
#
# Description:
walk the path, looking for moment logs
for each log
scan entries
for each entry
apply filter

# By: Charles Brandt [code at contextiskey dot com]
# On: *2009.09.11 18:52:31 
# License:  MIT

this functionality is implied many places:
/c/moments/scripts/filter_logs.py
/c/moments/scripts/split_by_day.py
/c/moments/scripts/make_m3u.py
/c/moments/packages/medialist/medialist/medialist.py
/c/moments/packages/medialist/medialist/filters.py
/c/moments/moments/extract.py
"""

import sys, os
#import re
#from datetime import datetime

#from moments.journal import load_journal, Journal
#from moments.path import check_ignore

#functionality moved to /c/moments2/moments2/filters.py
from moments.filters import filter_logs

def main():
    """
    """
    source = None
    if len (sys.argv) > 1:
        if sys.argv[1] in ['--help','help'] or len(sys.argv) < 2:
            usage()
        source = sys.argv[1]

    updates = [ ['c\/media\/binaries', 'c/binaries'],
                ['^media\/', '/c/']
                ]
    filter_logs(source, updates, save=True)

if __name__ == '__main__':
    main()
