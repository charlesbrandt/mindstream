#!/usr/bin/env python
"""
#
# Description:
# copy media from source to destination, splitting up source files into
# subdirectories based on media creation timestamp
#
# e.g.
# copy media from the USB device to the local filesystem (long term storage)

# By: Charles Brandt [code at contextiskey dot com]
# On: *2009.08.05 14:08:04
# License:  MIT

# Requires: moments

# originally created in Pose
python /c/code/python/scripts/import_usb.py [source_dir] [destinatin_dir]
"""
from __future__ import print_function
from builtins import str

import sys, os, subprocess

from moments.journal import Journal
from moments.path import Path
from moments.timestamp import Timestamp
from moments.tag import Tags

def _move_file(source, new_dir):
    """
    wrap the system subprocess move command
    include other tasks that need to be performed

    """
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    path_string = str(source.path)
    source = path_string.replace(' ', '\ ')

    #instead, just issue system command
    #for moving files
    command = "mv %s %s" % (source, new_dir)
    mv = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    mv.wait()

    #for copying files
    #command = 'cp %s/* %s' % (source_dir, new_dir)
    #cp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    result = "moving: %s" % source
    result += mv.stdout.read()

    return result

def _move_files(source_dir, new_dir):
    """
    move all files on camera / usb media
    to local image directory
    """
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    #following yields:
    #OSError: [Errno 18] Cross-device link
    #on Mac OS X
    #may work elsewhere
    #result = ''
    #for item in d.contents:
    #    orig = os.path.join(d.path, item)
    #    new = os.path.join(new_dir, item)
    #    result += "%s %s\n" % (orig, new)
    #    os.rename(orig, new)

    source_dir = source_dir.replace(' ', '\ ')
    print(source_dir)

    #instead, just issue system command
    #for moving files
    command = "mv %s/* %s" % (source_dir, new_dir)
    mv = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    mv.wait()

    #for copying files
    #command = 'cp %s/* %s' % (source_dir, new_dir)
    #mv = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    result = "All finished with moving files.  Any output included below:<br>\n"
    result += mv.stdout.read()
    result += "\n<br> All files moved to: %s" % new_dir
    result += "\n<br> Press Back to return <br> \n"

    return result

def _move_image_and_thumbs(source, new_dir):
    """
    move file the same as _move_file
    can be used to replace _move_file

    also, if file is an image,
    use os.rename to move thumbs in addition to image

    very similar functionality as moments.path.Image.move()
    this version is not as crossplatfrom due to subprocess
    but that is needed when moving from one device to another.
    """
    result = ''
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    path_string = str(source.path)

    #path = Path(source_path)
    #source = path.load()
    source_type = source.path.type()
    #source = make_node(source.path)

    #only want to use this for subprocess
    #do not use as a path string for Path() objects...
    #they don't need escaping
    source_path = path_string.replace(' ', '\ ')
    #just issue system command for moving files
    #(python libraries don't always work across different devices)
    command = "mv %s %s" % (source_path, new_dir)
    mv = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    mv.wait()

    #for copying files
    #command = 'cp %s/* %s' % (source_path_dir, new_dir)
    #cp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    result = "moving: %s" % source_path
    result += mv.stdout.read().decode('utf-8')

    #We have already moved/copied the files at this point.
    #Try to move thumbnails if they exist:
    if source_type == "Image" and os.path.exists(source.thumb_dir_path):

        destination = os.path.join(new_dir, source.name)
        #new_file = make_node(destination)

        #move thumbnails
        new_image = Image(destination)

        #self.make_thumb_dirs(os.path.join(new_dir, self.thumb_dir_name))
        new_image.make_thumb_dirs()

        for k in list(source.sizes.keys()):
            #may be some files/images that do not have thumbs.  check first
            if os.path.exists(source.size_path(k)):
                os.rename(source.size_path(k), new_image.size_path(k))
            else:
                result += "No thumb (size: %s) found for %s" % (k, source.path)


    #move any items in action.txt that are associated with the file
    if os.path.exists(os.path.join(os.path.dirname(str(source.path)), 'action.txt')):
        print("don't forget to move items in action.txt!! :)")

    return result

def process_batch(batch, last_date, dest_prefix, tags):
    #don't want to accumulate tags from one day to the next:
    tags_copy = tags[:]
    tags_copy.insert(0, last_date)

    #look for other tags from journal:
    # could use a remote journal
    # to connect to an already running moments.server instance
    # or could just load the journal directly
    j_path = '/c/journal'
    ts = Timestamp(last_date)
    m = "%02d" % ts.month
    j_file = os.path.join(j_path, str(ts.year), m, ts.filename())
    j = Journal(j_file)
    photo_tags = [ 'photo', 'photos' ]
    entries = []
    for pt in photo_tags:
        entries.extend(j.tag(pt))
    for e in entries:
        for t in e.tags:
            if not t in photo_tags and not t in tags_copy:
                print("Adding tag: %s" % t)
                tags_copy.append(t)

    t = Tags(tags_copy)
    dest_dir = t.to_tag_string()
    dest = os.path.join(dest_prefix, dest_dir)
    #print dest

    for item in batch:
        #print _move_file(item, dest)
        print(_move_image_and_thumbs(item, dest))
        #print item.date()

    return dest

def check_dates(sources):
    """
    go through all sources and look for the days covered
    this is useful to check for media from
    devices that don't keep an accurate clock

    related to group_by_day, but not processing any batches here
    """
    dates = []
    for source in sources:
        p = Path(source)
        if p.exists():
            d = p.load()
            #print(d)
            #print(type(d))
            d.sort_by_date()

            for fpath in d.files:
                #print f.name
                f = fpath.load()
                if not f.date() in dates:
                    dates.append(f.date())

    return dates


def group_by_day(path, dest_prefix=None, tags=[]):
    """
    look at a directory, and group all files by the day they were created

    run through a supplied directory's files
    create sub-directories that correspond to the day of the files' timestamps
    move the files to their corresponding day subdirectory
    in the new_dir destination

    """
    if dest_prefix is None:
        dest_prefix = path
    p = Path(path)
    d = p.load()
    #d = make_node(path)
    d.sort_by_date()

    dates = []
    destinations = []

    last_date = None
    cur_batch = []
    print("%s Files found in %s" % (len(d.files), path))
    for fpath in d.files:
        #print f.name
        f = fpath.load()
        if f.date() != last_date:
            #check if we need to move the previous day's files:
            print("New day: %s (previously: %s)" % (f.date(), last_date))
            if cur_batch:
                dest = process_batch(cur_batch, last_date, dest_prefix, tags)
                destinations.append(dest)

            cur_batch = [ f ]
            last_date = f.date()
        else:
            cur_batch.append(f)

    #get the last one:
    if cur_batch:
        dest = process_batch(cur_batch, last_date, dest_prefix, tags)
        if not dest in destinations:
            destinations.append( dest )

    #if we need to do something else to the new directories
    #we have them all collected in destinations list

    return destinations

def import_media(sources, dest_prefix, tags=[], adjust_time=0, forced_date=None):
    """
    use group_by_day to move everything from the source into the destination
    grouped into destination directories by the day they were created

    then go through everything and process any images
    rotating them and generating thumbnails.

    forced_dates will over-ride group_by_day and use forced_date instead
    """
    start = Timestamp()

    destinations = []
    for src in sources:

        if forced_date:
            #just need to add all files from src to a cur_batch list
            #(i.e. very simplified version of group_by_day()
            cur_batch = []
            if dest_prefix is None:
                dest_prefix = src
            p = Path(src)
            d = p.load()
            d.sort_by_date()
            #print "%s Files found in %s" % (len(d.files), src)
            for fpath in d.files:
                f = fpath.load()
                cur_batch.append(f)

            if cur_batch:
                dest = process_batch(cur_batch, forced_date, dest_prefix, tags)
                if not dest in destinations:
                    destinations.append( dest )

        else:
            ## destinations = []
            new_destinations = group_by_day(src, dest_prefix, tags)
            destinations.extend(new_destinations)

    print("")
    print("")
    print("")
    #if there are multiple calls to import_media for different directories
    #this may not be the case:
    finish_move = Timestamp()
    print("%s: All done moving and grouping files for:" % finish_move)
    print(sources)
    print("If that's everything, it's OK to eject media now")
    print("")
    print("Starting rotation and thumbnail generation...")
    print("")

    ## if something goes wrong and you need to run this again:
    print("Destinations: (just in case)")
    print(destinations)
    print("")

    #it may be possible to generate destinations a different way too:

    ## dirs = os.listdir(dest_prefix)
    ## if '.DS_Store' in dirs:
    ##     dirs.remove('.DS_Store')
    ## destinations = []
    ## for d in dirs:
    ##     destinations.append(os.path.join(dest_prefix, d))

    #or specify a specific path, pre-grouped:
    #destinations = [ '/media/DATA/journal/2012/20120606' ]

    for dest in destinations:
        #run rotate, thumbnail generation
        print(dest)
        #d = make_node(dest)
        path = Path(dest)
        d = path.load()
        #print "rotating images:"
        d.auto_rotate_images()
        #adjust times:
        #-2 hours
        #for multiple calls, may want to comment out
        #(i.e. if it has been run on the directory once already... )
        #print "adjusting timestamp on images:"
        d.adjust_time(hours=adjust_time)
        #print "making thumbnails:"
        d.make_thumbs()
        #something is causing old timestamps to show up in the journal
        #trying to recreate directory object to fix
        #print "making action log:"
        d = path.load()
        #d = make_node(dest)
        d.scan_filetypes()
        d.files_to_journal(filetype="Image")
        d.files_to_journal(filetype="Sound")

    end = Timestamp()

    result = ''
    result += "From: %s To: %s,\n" % (str(start), str(end))
    if len(destinations):
        result += "Processed files from: %s to: %s\n" % (destinations[0], destinations[-1])
    else:
        result += "No files found\n"
    return result

def main():
    if len (sys.argv) > 1:
        if sys.argv[1] in ['--help','help'] or len(sys.argv) < 2:
            usage()
        src = sys.argv[1]
        dest_prefix = sys.argv[2]
        tag_str = sys.argv[3]
        tags = tag_str.split(' ')
        result = import_media([src,], dest_prefix, tags)
        print(result)
        
if __name__ == '__main__':
    main()
