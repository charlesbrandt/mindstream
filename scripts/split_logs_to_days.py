#!/usr/bin/env python3
"""
#
# Description:
# script to run through a supplied directory's moment logs
# (parse sub directories too) (similar to load journal)
# rather than loading into a large journal
# iterate over eacy file individually
# make a journal
# export entries based on day
# to a YYYY/MM/YYYYMMDD.txt structure

# By: Charles Brandt [code at contextiskey dot com]
# On: *2010.02.13 12:15:51 
# License:  MIT

# Requires: moments
#

see also:
/c/moments/moments/launcher.py
/c/moments/moments/journal.py
/c/moments/moments/timestamp.py
/c/moments/scripts/split_by_day.py

$Id$ (???)
"""
from __future__ import print_function
from builtins import input
from builtins import str

import sys, os, subprocess, re
from moments.journal import Journal
from moments.path import Path, check_ignore
from moments.timestamp import Timestamp
from moments.filters import omit_date_tags

def split_log(path, add_tags, destination='/c/journal/'):
    print(path)
    j = Journal()
    j.load(path, add_tags=add_tags)
    if len(j.entries()):
        ## for e in j:
        ##     #make sure they're all moments, otherwise we might want to look
        ##     #at what is going on.
        ##     try:
        ##         assert e.created
        ##     except:
        ##         print e.render()
        ##         exit()
            
        for e in j.entries():
            #print str(e.render())
            if hasattr(e, "created") and e.created:
                month = "%02d" % e.created.month
                dest_path = os.path.join(destination, str(e.created.year), month)
                dest = os.path.join(dest_path, e.created.filename())
                #print e.render()
            else:
                dest = os.path.join(destination, "no_date.txt")
            print(dest)

            existing = Journal()
            if not os.path.exists(dest):
                print("no log %s" % dest)
                if not os.path.exists(dest_path):
                    print("missing directory: %s" % dest_path)
                    os.makedirs(dest_path)
                existing.save(dest)
                
            existing.load(dest)
            print("entries before: %s" % len(existing.entries()))
            existing.update(e)
            print("entries after update: %s" % len(existing.entries()))
            existing.sort('chronological')
            existing.save(dest)
            print("entries after: %s" % len(existing.entries()))

        print(path)
        input('Ok to remove?')
        
        #get rid of the source to avoid confusion
        os.remove(path)
        #rather than removing, remove from mercurial:
        #command = "hg rm %s" % path
        #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        #                           stderr=subprocess.PIPE)

        input('Press Enter to continue...')

        print("")

#def walk_logs(source, add_tags=["people"], subtract_tags=[],
def walk_logs(source, destination='/c/journal/', add_tags=[], subtract_tags=[],
              include_all_path_tags=False, include_some_path_tags=True):
    """
    walk the given path and
    load a journal object for each log encountered in the path
    then split it up using split_logs function

    based on moments.journal.load_journal

    """

    #ignore_items = [ 'downloads', 'index.txt' ]
    ignore_items = [ ]
    log_check = re.compile('.*\.txt$')
    if os.path.isdir(source):
        for root,dirs,files in os.walk(source):
            for f in files:
                current_file = os.path.join(root, f)
                
                #make sure it is a log file (.txt):
                if not log_check.search(f):
                    continue

                if not check_ignore(current_file, ignore_items):
                    these_tags = add_tags[:]
                    filename_tags = []
                    if include_all_path_tags:
                        filename_tags = Path(current_file).to_tags()
                    elif include_some_path_tags:
                        #rather than include all tags from path
                        #check relative path only
                        #include those tags that are not a date tag
                        #otherwise ok to skip
                        full_path = Path(current_file)
                        relative_path = full_path.to_relative(source)
                        filename_tags = Path(os.path.join('/', relative_path)).to_tags()
                        filename_tags = omit_date_tags(filename_tags)
                        #typically this is not really the appropriate tag.
                        #used more as a generic file
                        #for history in a given context.  
                        if 'journal' in filename_tags:
                            filename_tags.remove('journal')

                    these_tags.extend(filename_tags)

                    #subtract tags last:
                    for tag in subtract_tags:
                        if tag in these_tags:
                            these_tags.remove(tag)

                    print("add_tags: %s" % these_tags)
                            
                    split_log(current_file, add_tags=these_tags, destination=destination)

    else:
        print("pass in a directory")


#walk_logs('/path/to/logs', subtract_tags=['c'])
#walk_logs('/c/incoming', subtract_tags=['c', 'incoming'])
#walk_logs('/c/journal/incoming')
def usage():
    print("split_logs_to_days.py source dest")
    
def main():
    #requires that at least one argument is passed in to the script itself (sys.argv)
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()

        source = sys.argv[1]
        if len(sys.argv) > 2:
            dest = sys.argv[2]
        else:
            dest = '/c/journal'
        #walk_logs('/c/journal/incoming', '/c/journal/')
        walk_logs(source, dest)

    else:
        usage()
        exit()
        
if __name__ == '__main__':
    main()
    
