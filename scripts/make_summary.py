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
from __future__ import print_function
from builtins import str
from builtins import range

import os, sys, codecs, re

from moments.path import load_journal, Path
from moments.journal import Journal
#from moment import Moment
from moments.timestamp import Timestamp, Timerange

from mindstream.summary import Summary, TimeSummary

j = Journal()

def usage():
    print(__doc__)
    
def load_journal_helper(item):
    """
    TODO:
    if not using remote journal, should be a more efficient way to do this:
    """
    global j
    temp_j = load_journal(item)
    entries = temp_j.entries()
    j.update_many(entries)
    return "%s loaded (%s entries)" % (item, len(entries))


def find_photos(cur_summary, cur_year, photo_roots, ignores=[]):
    #look for pictures
    #may require customization for each root
    #but starting with one known one for now
    for photo_root in photo_roots:
        #now look for content matching the day:
        year_path = os.path.join(photo_root, cur_year)
        options = os.listdir(year_path)
        for option in options:
            ignore = False
            for i in ignores:
                if re.search(i, option):
                    ignore = True

            if re.match(d_compact, option) and not ignore:
                #find all photos in dir:
                option_path = os.path.join(year_path, option)
                print("looking in: %s" % option_path)
                #very similar to content.Content.find_media()
                #but this is only checking one level down
                #I don't think we want to walk here:
                kind = "Image"
                image_options = os.listdir(option_path)
                for io in image_options:
                    media = os.path.join(option_path, io)
                    mpath = Path(media)
                    #if debug:
                    #    print "looking at: %s" % media
                    if mpath.type() == kind:
                        print("matched!", media)
                        if not media in cur_summary.photos:
                            cur_summary.photos.append(media)
    
        
if __name__ == '__main__':
    source = None
    destination = None
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()

        all_sources = []
        sources = sys.argv[1:]
        for s in sources:
            #this will get the first one to use as primary path_root
            if not source:
                source = s
            all_sources.append(s)

            #this is the local load_journal function
            #not to be confused with moments.path.load_journal function
            load_journal_helper(s)
            print("Loaded: %s entries" % len(j.entries()))
            print("Load finished: %s" % Timestamp())


        #now find out what years we have in the journal
        #this is similar to pose.timeline:

        j.sort('chronological')

        #caching locally ends up taking longer, surprisingly enough
        #entries = j.entries()
        #local_j = Journal()
        #local_j.update_many(entries)
        local_j = j


        root_summary = TimeSummary()
        root_summary.name = 'root'
        #seems silly to apply this to every node
        root_summary.sources = sources

        #this is the process for every year:
        #for *creating* new
        #update will be slightly different

        cur_year = str(2014)

        year_summary = TimeSummary()
        year_summary.name = cur_year

        year_range = Timerange(cur_year)
        entries = local_j.range(year_range.start, year_range.end)
        year_j = Journal()
        year_j.update_many(entries)
        for month in range(1, 13):
            m_compact = "%s%02d" % (cur_year, month)
            print("Month: %s" % m_compact)
            month_range = Timerange(m_compact)
            m_entries = year_j.range(month_range.start, month_range.end)
            month_j = Journal()
            month_j.update_many(m_entries)

            month_summary = TimeSummary()
            month_summary.name = m_compact

            for day in range(month_range.start.day, month_range.end.day+1):
                d_compact = "%s%02d%02d" % (cur_year, month, day)
                print("Day: %s" % d_compact)
                day_range = Timerange(d_compact)
                d_entries = year_j.range(day_range.start, day_range.end)
                day_j = Journal()
                day_j.update_many(d_entries)
                day_summary = TimeSummary()
                day_summary.name = d_compact

                day_summary.size = len(d_entries)
                #now generate a cloud for the day
                day_summary.cloud = day_j.tags()

                photo_roots = [ '/c/binaries/journal', ]
                ignores = [ 'cwt', ]

                find_photos(day_summary, cur_year, photo_roots, ignores=[])

                month_summary.add_summary(day_summary)
                #TODO
                #might want to check for month level photos here:
                
            year_summary.add_summary(month_summary)

        root_summary.add_summary(year_summary)
        print(year_summary.to_dict())
        
        #Many different ways to create and store Summary objects
        #could make separate files in a filesystem if that would be helpful
        #or could store everything in one tree if that will always be loaded

        #will all depend on how save is called
        #and at what levels save is called
        
        root_summary.save('root.json')


        ## exit()





        ## counter = 0
        ## first = local_j.entry(counter)
        ## while isinstance(first.created, str) or isinstance(first.created, unicode):
        ##     counter += 1
        ##     first = local_j.entry(counter)

        ## started_at = counter

        ## counter = -1
        ## last = local_j.entry(counter)
        ## while isinstance(last.created, str) or isinstance(last.created, unicode):
        ##     counter -= 1
        ##     last = local_j.entry(counter)

        ## last = local_j.entry(-1)

        ## body = ''

        ## for year in range(first.created.year, last.created.year+1):
        ##     year_range = Timerange(str(year))

        ##     #this is expensive to do on a remote Journal
        ##     #currently (*2011.12.31 16:10:43) takes a minute and a half to run
        ##     #going to try loading a local copy of journal in memory
        ##     #and see if that improves the situation
        ##     #also 2011.12.31 16:18:58
        ##     #caching the journal locally to this function actually takes longer
        ##     #(2+ minutes)
        ##     #it's an expensive operation
        ##     year_range = Timerange(str(year))
        ##     entries = local_j.range(year_range.start, year_range.end)

        ##     year_j = Journal()
        ##     year_j.update_many(entries)

        ##     print year

        ##     next_year = year + 1

        ##     body += '<p><a href="/range/%s/%s">%s</a> (%s entries)<br>' % (year, next_year, year, len(entries))

        ##     for month in range(1, 13):
        ##         compact = "%s%02d" % (year, month)
        ##         month_range = Timerange(compact)
        ##         m_entries = year_j.range(month_range.start, month_range.end)
        ##         body += '<a href="/range/%s/%s">%s</a> (%s entries) - ' % (compact, month_range.end.compact(), month, len(m_entries))

        ##     body += "</p>"
        ## return template('site', body=body, title="timeline")

