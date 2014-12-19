#!/usr/bin/env python
"""
# By: Charles Brandt <code at contextiskey dot com>
# On: 2014.12.15 10:28:30
# License:  MIT

# Description:
collecting notes about making summaries here
"""

import sys, os, copy

from medley.helpers import load_json, save_json

class JsonStorable(object):
    """
    this pattern comes up often lately
    for storing and loading objects from disk

    might not be practical to determine what to ignore for saving
    without redefining in subclass
    
    adapted from methods in: medley.people.Person
    """
    
    def to_dict(self):
        """
        simplified version of creating a simple dict object
        """
        temp_d = copy.copy(self.__dict__)

        #make sure to ignore loaded/scanned contents on a save
        temp_d.pop("contents", None)

        if temp_d.has_key('debug'):
            #this is only used locally
            temp_d.pop("debug", None)

        return temp_d

    def as_json(self):
        """
        for using a person object in javascript
        """
        return json.dumps(self.to_dict())
    
    def save(self, destination):
        """
        make a directory if none exists
        save the results
        """
        if not destination:
            raise ValueError, "Need to know where to save: %s" % destination
         
        temp_d = self.to_dict()
        
        #print "Saving: %s to %s" % (temp_d, destination)
        save_json(destination, temp_d)
        
    def load(self, source, debug=False):
        result = load_json(source)
        
        if self.debug:
            print "Loaded: %s" % result
        self.__dict__.update(result)
    

class Summary(JsonStorable):
    """
    Summary objects are tricky.
    All objects or digital representations or any model of something...
    in some ways these are all 'summaries' of the original object they model
    They become their own thing in the process, but they are never the original.
    They are merely a copy or a map that describes the original.

    So then we end up with large Collections (see Medely) of objects
    (Contents in the case of Medley).
    Contents may represent many segments of sub sections.

    The structures are often hierarchical in nature,
    but sometimes they loop back on themselves,
    forming more of a web or network

    So rather than parse and traverse that web and network every time we're
    interested in a zone, it helps to summarize it,
    to get the highlights, the best of, the cream of the crop...

    Of course, because it is a summary, a snapshot of the original,
    the original may morph and change since the summary was created.
    And there may be gems left out of the highlights,
    or, once a perspective changes, the highlights may change focus too.
    So it helps to be able to recreate these, as needed. 

    There are many applications for this concept,
    some of which already have their own implementations.
    It would be nice to abstract where possible,
    and adapt existing solutions where possible.

    Some applications:

    Summarizing all moments and all photos (and all playlists, and?) for a year.

    Summarizing the amount of storage space being used by a given directory

    Summarizing a subset of a Collection for exporting to a portable system. 


    SEE ALSO:
    /c/alpha/disk_usage/launch.sh


    One approach is to store the whole sub-heirarchy in on json tree
    {'name': '', 'contents': [] }
    For contents, one approach is to use the media list format
    from Content objects:
    ['/path/to/file', 'dimension_x_dimension', 'size_in_bytes']

    The downside with this is that
    any change to a sub section will not be noticed.
    Said differently, there is no way to identify when a subsection changes.
    Maybe including a timestamp is sufficient.

    This might not make sense though,
    especially if the structure does not mirror a file system hierarchy


    GOALS:

    Easily rescan sub-summaries before rescanning everything.
    If a sub summary has been updated (and is different)
    since last parent summary update,
    should be able to quickly adjust parent summary with that info accordingly 
    could then re-run a scan, if desired. (alert user)
    This is similar to a version control system knowing if a file is out of sync
    Usually, structures stabilize.
    Once that happens, scans shouldn't be needed as often (if ever)

    Would be nice to be able to edit the summary manually, similar to:
    *2014.12.15 10:50:09 
    /c/charles/summary.txt
    However, it will probably be necessary to move beyond a simple moment-log
    structure for storing the meta data of a summary.
    In that case, a JSON object should suffice.
    (Those can still be edited manually, just not as conveniently)
    

    This also touches on methods for persisting data...
    right now moments server will load all available entries into memory.
    TODO: consider if redis could help with this process.
          might lend better infrastructure and utilizationi to the system

    Maybe there are ways to only check for changes,
    similar to only reloading a server when a change is observed.

    But even this, the method of persistence, becomes another representation.
    It is important to decide where the primary versions live
    and ways to keep everything in sync, or enough in sync to keep it usable.

    Changes are always happening!
    
    """
    def __init__(self):
        """
        """
        #print "object passed: %s from command line" % arg
        self.name = ''

        #aka children
        #should be able to treat this as an ordered list
        #can always sort by common orders automatically
        #(just don't save the automatically sorted result)
        self.contents = []

        #last update
        self.updated = Timestamp()

        #as of last update... only use as an estimate after that
        #size units can vary based on application
        #up to the application to make sure they're consistent
        #e.g. # of entries, # of bytes, length of time, etc
        self.size = 0

        #custom / manually created notes
        #self.details = ''
        #this might fit in highlights
        
        #this is different than contents
        #in that it can contain anything from below...
        #not just immediate children
        #might not need a default either...
        #just take as many as your layout can handle
        #these should all be manually specified?
        #similar to photos, but more generic
        self.highlights = []

        #anything specific to this node
        #might make sense to make this a JSON encoded string
        #for application specific structures
        self.notes = ''
        #sometimes use this instead (Content)
        #self.history = ''



#maybe there are 2 types of Summary objects...
# - one that keeps track of a directory structure's data
# - one that keeps track of time ranges.
# related, but might make sense to subclass for each
    

class TimeSummary(Summary):
    def __init__(self):
        """
        """

        #a compact string representation, if the summary covers a range of time
        self.timerange = ''


        #not quite sure yet about the following items...
        #brainstorming...
        #many different applications
        #trying to keep it flexible
        #and yet not bloated

        #for rendering, might want different summaries to show up differently
        #self.layout = ''
        #similar to layout, but maybe it makes sense to keep track of this?
        #self.type = ''
        #similar to layout, notes about rendering for different scales?
        #min_size, max_size... brings to mind areaui concepts
        #self.scale

        #maybe keep bytes separate... that is more of a fixed unit
        #and most digital representations still vary here:
        self.bytes = 0

        #a hash field is also used in content items
        #it implies a single file, which may not be the case...
        #also implies a path
        #which might make Content objects more suitable:
        #self.hash = ''

        #aka 'includes'
        #if there is a path associated with the Node
        #self.path = ''
        #might need a list of different sources included
        #source may be paths, may not be
        self.sources = []
        
        #tag_cloud? cloud?
        self.cloud = {}
        #not sure if this is universal enough
        #clouds are a type of summary of their own
        #but it would be nice to be able to regenerate them
        #without a complete re-scan

        #may also want to include anything that was ignored:
        self.ignores = {}


        #similar to People.photos
        #will want to associate tags, so just a list of paths is not sufficient
        #use SimpleContent... no tree structure there
        #also much overlap with moments.path.Image object
        self.photos = []
        #self.default_photo = ''
        #is something more generic, like 'highlights', sufficient?

        
def usage():
    print __doc__
    
def main():
    #requires that at least one argument is passed in to the script itself (sys.argv)
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()

        #skip the first argument (filename):
        for arg in sys.argv[1:]:
            a = Summary(arg)

    else:
        a = Summary()
        usage()
        exit()
        
if __name__ == '__main__':
    main()
