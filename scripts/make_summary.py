#!/usr/bin/env python
"""
#
# By: Charles Brandt [code at charlesbrandt dot com]
# On: *2014.12.19 11:02:13 
# License: MIT 

# Requires:
#

# Description:
#
initially adapted from moments.server code

"""

import os, sys, codecs

from moments.path import load_journal as load_journal_path
from moments.journal import Journal
#from moment import Moment
from moments.timestamp import Timestamp, Timerange

from mindstream.summary import Summary

j = Journal()

def usage():
    print __doc__
    
def load_journal(item):
    """
    
    """
    global j
    temp_j = load_journal_path(item)
    entries = temp_j.entries()
    j.update_many(entries)
    return "%s loaded (%s entries)" % (item, len(entries))
        
        
if __name__ == '__main__':
    source = None
    destination = None
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()

        sources = sys.argv[1:]
        for s in sources:
            #this will get the first one to use as primary path_root
            if not source:
                source = s

            #this is the local load_journal function
            #not to be confused with moments.path.load_journal function
            load_journal(s)
            print "Loaded: %s entries" % len(j.entries())
            print "Load finished: %s" % Timestamp()


        #now find out what years we have in the journal
        #this is similar to pose.timeline:

        j.sort('chronological')

        #caching locally ends up taking longer, surprisingly enough
        #entries = j.entries()
        #local_j = Journal()
        #local_j.update_many(entries)
        local_j = j

        year = str(2014)
        year_range = Timerange(year)
        entries = local_j.range(year_range.start, year_range.end)
        year_j = Journal()
        year_j.update_many(entries)
        for month in range(1, 13):
            month_range = 
            compact = "%s%02d" % (year, month)
            month_range = Timerange(compact)
            m_entries = year_j.range(month_range.start, month_range.end)

        #Many different ways to create and store Summary objects
        #could make separate files in a filesystem if that would be helpful
        #or could store everything in one tree if that will always be loaded
        

        year_summary = Summary()





        counter = 0
        first = local_j.entry(counter)
        while isinstance(first.created, str) or isinstance(first.created, unicode):
            counter += 1
            first = local_j.entry(counter)

        started_at = counter

        counter = -1
        last = local_j.entry(counter)
        while isinstance(last.created, str) or isinstance(last.created, unicode):
            counter -= 1
            last = local_j.entry(counter)

        last = local_j.entry(-1)

        body = ''

        for year in range(first.created.year, last.created.year+1):
            year_range = Timerange(str(year))

            #this is expensive to do on a remote Journal
            #currently (*2011.12.31 16:10:43) takes a minute and a half to run
            #going to try loading a local copy of journal in memory
            #and see if that improves the situation
            #also 2011.12.31 16:18:58
            #caching the journal locally to this function actually takes longer
            #(2+ minutes)
            #it's an expensive operation
            year_range = Timerange(str(year))
            entries = local_j.range(year_range.start, year_range.end)

            year_j = Journal()
            year_j.update_many(entries)

            print year

            next_year = year + 1

        ##     body += '<p><a href="/range/%s/%s">%s</a> (%s entries)<br>' % (year, next_year, year, len(entries))

        ##     for month in range(1, 13):
        ##         compact = "%s%02d" % (year, month)
        ##         month_range = Timerange(compact)
        ##         m_entries = year_j.range(month_range.start, month_range.end)
        ##         body += '<a href="/range/%s/%s">%s</a> (%s entries) - ' % (compact, month_range.end.compact(), month, len(m_entries))

        ##     body += "</p>"
        ## return template('site', body=body, title="timeline")

