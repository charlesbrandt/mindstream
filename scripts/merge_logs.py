#!/usr/bin/env python
"""
#
# Description:
# takes two moment logs and merges them

# By: Charles Brandt [code at contextiskey dot com]
# On: 2009.01.29 18:15:01 
# License:  MIT

# Requires: moments

*2011.08.17 22:17:02
primarily used with export_logs
incorporating it there
and including with moments

"""

import sys, os
from moments.journal import Journal
from moments.path import load_journal, Path
from moments.timestamp import Timestamp
from moments.export import merge_many, merge_logs

## def merge_many(source, destination, add_tags=[]):
##     """
##     use load journal to load the source directory
##     then save the resulting journal to the temporary destination
##     """
##     j = load_journal(source, add_tags)
##     j.sort_entries('reverse-chronlological')
##     j.to_file(destination)
    
## def merge_logs(f1, f2, add_tags=[], ofile="", verbose=False):
##     """
##     this is a common operation involving two log files or two Journal objects

##     it is fairly simple with the Journal object,
##     but this handles all of the calls
##     for creating those Journal objects from files
    
##     add tags will only apply to the first file
##     it is being merged into the second
##     """
##     #shouldn't need osbrowser here... we know the absolute paths via shellx
##     #n1 = osbrowser.meta.make_node(f1)

##     result = ''
    
##     j = Journal()
##     j.from_file(f1, add_tags)
##     len1 = len(j)

    
##     j2 = Journal()
##     j2.from_file(f2)
##     len2 = len(j2)

##     j.from_file(f2)
##     len3 = len(j)
    
##     result += "merge resulted in %s entries from %s and %s\n" % (len3, len1, len2)

##     f2_obj = Path(f2)
##     if not ofile:
##         now = Timestamp(now=True)
##         temp_name = "merge-%s-%s.txt" % (now.compact(), f2_obj.name)
##         ofile = os.path.join(str(f2_obj.parent()), temp_name)
##     result += "SAVING as: %s\n" % ofile
##     j.to_file(ofile)

##     if verbose:
##         print result

##     #if there are dupes the two totals may not add up to the new total
##     # (does not necessarily mean a conflict)
##     #and now journal can handle multiple entries with the same timestamp,
##     # (so it will not discard subsequent entries with the same timestamp)
##     #so it may be ok to always accept a merge
##     # (as long as both files consisted of actual moment entries)
##     #
##     #if (len1+len2 == len3):
##     #    return (ofile, 1)        
##     #else:
##     #    result += "WARNING: dupes/conflicts encountered<br>"
##     #    return (ofile, 0)

##     return (ofile, 1)

    
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help','help'] or len(sys.argv) < 2:
            usage()
        f1 = sys.argv[1]
        f2 = sys.argv[2]
        merge_logs(f1, f2, verbose=True)
        
if __name__ == '__main__':
    main()
