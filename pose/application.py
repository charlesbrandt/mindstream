#!/usr/bin/env python
"""
Pose server that uses a separate server to access journal data
that way journal data does not need to be reloaded every time server restarts

does make startup more complex:

separate tab:
cd /c/moments/moments
python journal_server.py /c/journal

python application-split.py
"""

import sys, os, re, codecs
import urllib, urllib2

#redefine standard python range:
pyrange = range

from bottle import static_file
from bottle import get, post, request
from bottle import route, run
from bottle import template

#DO NOT USE THIS IN PRODUCTION!!
import bottle
bottle.debug(True)

server_root = os.path.dirname(os.path.realpath(__file__))
#print "Server root: %s" % server_root

#default is "./views/" directory
template_path = os.path.join(server_root, 'templates')
#bottle.TEMPLATE_PATH.append('./templates/')
bottle.TEMPLATE_PATH.append(template_path)

try:
    import simplejson as json
except:
    try:
        import json
    except:
        print "No json module found"
        exit()
        
from moments.log import Log
from moments.path import Path
from moments.tag import Tags
from moments.association import Association
from moments.journal import Journal
from moments.timestamp import Timerange

from moments.journal import RemoteJournal

from cloud import Cloud
#from moments.mindstream import Mindstream
from mindstream.launch import edit, file_browse


server = bottle.Bottle()


# GLOBALS:
#this is equivalent to main() function in template_script.py

#requires that at least one argument is passed in to the script itself
#(through sys.argv)
ignores = []

port = 8088
path_root = '/c/moments/tests/'
path_root = "/c/binaries/journal/2010/"
path_root = "/c/"
path_root = "/"

if len(sys.argv) > 1:
    helps = ['--help', 'help', '-h']
    for i in helps:
        if i in sys.argv:
            print "python application.py [directory to load]"
            exit()

    ports = ['--port', '-p']
    for p in ports:
        if p in sys.argv:
            i = sys.argv.index(p)
            sys.argv.pop(i)
            port = sys.argv.pop(i)

    proots = ['--root', '-r', '-c', '--context']
    for p in proots:
        if p in sys.argv:
            i = sys.argv.index(p)
            sys.argv.pop(i)
            path_root = sys.argv.pop(i)

if len(sys.argv) > 1:
    look_in = sys.argv[1]
    print "Look in: %s" % look_in
else:
    look_in = 'http://localhost:8000'


print "Path root: %s" % path_root

#should be able to call these directly if desired
@server.route('/search/data/:key')
@server.route('/search/data/:key/')
def search_data(key):
    global look_in
    j = RemoteJournal(look_in)
    entries = j.search(key, data=True)
    results = []
    for e in entries:
        results.append(e.as_dict())
    return { 'matches' : results }

@server.route('/search/:key/:limit/')
@server.route('/search/:key/:limit')
@server.route('/search/:key/')
@server.route('/search/:key')
@server.route('/search/')
@server.route('/search')
def search(key=None, limit=20):
    global look_in
    j = RemoteJournal(look_in)
    if key is None:
        key = request.GET.get('term')

    #print key
    tags = j.search(key, limit=limit)
    #return { 'matches' : tags }
    return json.dumps(tags)


# ROUTES

#Be careful when specifying a relative root-path such as root='./static/files'.
#The working directory (./) and the project directory are not always the same.
#@route('/css/:filename')
@server.route('/css/:filename#.+#')
#@route('/css/style.css')

def css_static(filename):
    css_path = os.path.join(server_root, 'css')
    print css_path
    #return static_file(filename, root='./css')
    return static_file(filename, root=css_path)

@server.route('/js/:filename#.+#')
def js_static(filename):
    js_path = os.path.join(server_root, 'js')
    return static_file(filename, root=js_path)

@server.route('/images/:filename#.+#')
def images_static(filename):
    image_path = os.path.join(server_root, 'images')
    return static_file(filename, root=image_path)
  
## @server.route('/js/:filename')
## def js_static(filename):
##     return static_file(filename, root='./js')

## @server.route('/css/:filename')
## def css_static(filename):
##     return static_file(filename, root='./css')

## @server.route('/images/:filename')
## def images_static(filename):
##     return static_file(filename, root='./images')



@server.route('/m3u/:name')
@server.post('/m3u/')
def m3u(name='world'):
    global look_in
    j = RemoteJournal(look_in)
    global path_root

    if name == "world" or name == '' or name is None:
        name = request.forms.get('tag')
        redirect('/tagged/%s' % name)
        
    entries = j.tag(name)

    m3u = "#EXTM3U\r\n"
    for e in entries:
        first_line = e.data.splitlines()[0] 
        title = os.path.basename(first_line)
        m3u += "#EXTINF: ,0 - %s\r\n" % (title)
        prefix = "/media/disk/"
        full_path = os.path.join(prefix, first_line)
        if not os.path.exists(full_path):
            print "Couldn't find: %s" % full_path
        m3u += full_path + '\n'
        
    return m3u

@server.route('/tagged/:name')
@server.post('/tagged/')
def tagged(name='world'):
    global look_in
    j = RemoteJournal(look_in)
    global path_root

    if name == "world" or name == '' or name is None:
        name = request.forms.get('tag')
        redirect('/tagged/%s' % name)
        
    #print "NAME: %s" % name
    #entries = j.entries_tagged(name)
    entries = j.tag(name)

    #print entries
    #print len(entries)
    #*2011.06.16 11:06:01
    #TODO:
    #related should be included here, at the top...
    #easy to scroll by
    #and if there are too many related,
    #that's probably a bigger problem (cluttered space)
    related = j.related(name)
    #return template('related', tags=related, name=name)
    
    for e in entries:
        #if hasattr(e, "path"):
        e.path = Path(e.path, relative_prefix=path_root)

    j = Journal()
    j.update_many(entries)
    j.sort('reverse-chronological')
    entries = j.entries()
    #entries.reverse()
    
    return template('entries', entries=entries, tags=related, name=name)

@server.route('/timeline')
def timeline():
    """
    display a navigatable timeline for all of the times involved
    """
    global look_in
    j = RemoteJournal(look_in)
    j.sort('chronological')

    #caching locally ends up taking longer, surprisingly enough
    #entries = j.entries()
    #local_j = Journal()
    #local_j.update_many(entries)
    local_j = j
    
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

    for year in pyrange(first.created.year, last.created.year+1):
        year_range = Timerange(str(year))

        #this is expensive to do on a remote Journal
        #currently (*2011.12.31 16:10:43) takes a minute and a half to run
        #going to try loading a local copy of journal in memory
        #and see if that improves the situation
        #also 2011.12.31 16:18:58
        #caching the journal locally to this function actually takes longer
        #(2+ minutes)
        #it's an expensive operation
        entries = local_j.range(year_range.start, year_range.end)

        year_j = Journal()
        year_j.update_many(entries)

        next_year = year + 1
        body += '<p><a href="/range/%s/%s">%s</a> (%s entries)<br>' % (year, next_year, year, len(entries))

        for month in pyrange(1, 13):
            compact = "%s%02d" % (year, month)
            month_range = Timerange(compact)
            m_entries = year_j.range(month_range.start, month_range.end)
            body += '<a href="/range/%s/%s">%s</a> (%s entries) - ' % (compact, month_range.end.compact(), month, len(m_entries))
            
        body += "</p>"
    return template('site', body=body, title="timeline")


@server.route('/range/:start/:end/')
@server.route('/range/:start/:end')
@server.route('/range/:start/')
@server.route('/range/:start')
@server.route('/range/')
@server.route('/range')
def range(start=None, end=None):
    global look_in
    j = RemoteJournal(look_in)
    if start:
        entries = j.range(start, end)

        ignores = []

        range_j = Journal()
        range_j.update_many(entries)
        tags = range_j.tags()

        cloud = Cloud(tags, ignores=ignores)
        cloud.make()

        body = ''
        body += "<p>%s total tags" % len(tags.keys())
        body += " --- %s total entries</p>" % len(entries)
        body += cloud.render("/tagged/%s")

        for entry in entries:
            entry.path = Path(entry.path)
            body += template('entry', entry=entry)

        return template('site', body=body, title=start)

        ## results = []
        ## for e in entries:
        ##     results.append(e.as_dict())
            
        ## return { 'entries' : results }
    else:
        return str(j.range())



@server.route('/clouds')
def clouds():
    """
    look up all available clouds and provide links to them
    """
    global path_root

    cloud_file = os.path.join(path_root, 'clouds.txt')
    if not os.path.exists(cloud_file):
        print "couldn't find cloud file: %s" % cloud_file
        exit()

    clouds = Journal(cloud_file)

    body = ''

    tags = clouds.tags().keys()
    #body = str(tags)
    tags.sort()

    for name in tags:
        tags_found = clouds.tags(name)[0].data.split()

        body += '<p><a href="/cloud/%s">%s</a> <a href="/cloud/ignore/%s">(ignore)</a> [%s tags in cloud]</p>' % (name, name, name, len(tags_found))

    return template('site', body=body, title="clouds")


@server.route('/cloud/ignore/:name#.+#')
@server.route('/cloud/ignore/')
@server.route('/cloud/ignore')
def ignore_cloud(name="ignores"):
    return cloud(name=name, ignore_cloud=True, preserve_order=False)

@server.route('/cloud/:name#.+#')
def cloud(name='world', ignore_cloud=False, preserve_order=True):
    """
    ignore_cloud will toggle whethere the supplied name cloud
    contains only tags for use
    or only tags to be ignored.
    """
    global look_in
    j = RemoteJournal(look_in)
    global path_root
    global ignores

    all_tags = j.tags()
    
    if name != 'world':
        #look for a cloud with the name we were passed
        #cloud file should be passed in
        #or local 'clouds.txt'
        cloud_file = os.path.join(path_root, 'clouds.txt')
        if not os.path.exists(cloud_file):
            print "couldn't find cloud file: %s" % cloud_file
            exit()
            
        clouds = Journal(cloud_file)

        tags = Association()
        order = []
        if clouds.tag(name):
            tags_found = clouds.tags(name)[0].data.split()

            if ignore_cloud:
                #this should ignore any tags found in the loaded list
                ignore_tags = tags_found
                for t in all_tags.keys():
                    if not t in ignore_tags:
                        tags[t] = all_tags[t]
                        order.append(t)
            else:
                #this assumes the tags in clouds are what we want
                for t in tags_found:
                    if all_tags.has_key(t):
                        tags[t] = all_tags[t]
                        order.append(t)            

    else:
        tags = all_tags
        order = all_tags.keys()
        order.sort()
        
    #return template('site', body=str(tags))
    
    if preserve_order:
        cloud = Cloud(tags, ignores=ignores, ordered_list=order)
    else:
        cloud = Cloud(tags, ignores=ignores)
    cloud.make()

    body = ''
    body += "<p>%s total tags</p>" % len(tags.keys())
    body += cloud.render("/tagged/%s")

    title = "%s - cloud" % name
    return template('site', body=body, title=title)

    #cloud2 = Cloud(j.tags, ignores=['python'])
    #cloud2.make_logarithmic()
    #body += "<h1>Log</h1>"
    #body += cloud2.render()


@server.route('/reload')
def reload():
    global look_in
    j = RemoteJournal(look_in)
    j.reload()
    redirect('/')
    




## @server.route('/path/launch/:timestamp#.+#')
## def launch_time(timestamp):
##     """
##     rather than launch a path
##     look up the moments at a given timestamp
##     and determine the path from the moment.path attribute

##     this avoids needing to determine the root for a relative path

##     also [2012.01.01 10:00:14]
##     unfortunately, not all entries have a timestamp
##     so this becomes very difficult for that specific case...
##     back to paths, but just not relative
##     """
##     global look_in
##     j = RemoteJournal(look_in)
##     entries = j.range(timestamp, timestamp)

##     response = ''
##     for e in entries:
##         path = e.path
##         if path.type() == "Log":
##             edit(path)
##             response += "editing: %s" % path
##         elif path.type() == "Directory":
##             file_browse(path)
##             response += "browsing: %s" % path
##         else:
##             response += "unknown type: %s for: %s" % (path.type(), path)

##     response += "LAUNCH STAMP: %s" % timestamp
##     return response

 
@server.route('/path/launch/:source#.+#')
def launch_path(source=''):
    global path_root
    path = Path(path_root + source, relative_prefix=path_root)

    #just assume the whole thing has been sent
    #path = Path(source)

    response = ''
    if path.type() == "Log":
        edit(path)
        response += "editing: %s<br>" % path
    elif path.type() == "Directory":
        file_browse(path)
        response += "browsing: %s<br>" % path
    else:
        response += "unknown type: %s for: %s<br>" % (path.type(), path)

    response += "LAUNCH PATH: %s<br>" % source
    return response


## @post('/path/edit/:relative#.+#')
## def rename_path(relative=''):
##     #if using get, will need to update the regular expression...
##     #relative eats up any get form parameters in the URL
##     #post works though
    
##     tags_string = request.forms.get('tags')
##     #return "EDIT PATH: %s" % (tags_string)
##     global path_root
##     path = Path(path_root + relative, relative_prefix=path_root)
##     tags = Tags().from_spaced_string(tags_string)
##     new_path = Path(path_root + relative, relative_prefix=path_root)
##     new_path.name = tags.to_tag_string()
##     if new_path.name != path.name:
##         path.rename(new_path)
##         return "RENAMED PATH: from: %s, to: %s" % (path, new_path)
##     else:
##         return "SAME NAMES: from: %s, to: %s" % (path, new_path)

## @server.route('/path/dupe/:relative#.+#')
## def dupe_path(relative=''):
##     global path_root
##     path = Path(path_root + relative, relative_prefix=path_root)
##     name = path.name
##     name_tags = path.to_tags(include_parent=False)
##     name_tags.insert(1, "2")
##     path.name = name_tags.to_tag_string()
##     #name = name + "-2"
##     #path.name = name
##     if not path.exists():
##         path.create()

##     return template('directory_summary', path=path, admin=True)
##     #return "DUPE PATH: %s" % path

#to serve files in subdirectories, loosen the wildcard as follows
#@route('/static/:path#.+#')
#def server_static(path):
#    return static_file(path, root='/path/to/your/static/files')

#to force a download, use the following:
#    return static_file(filename, root='/path/to/static/files', download=filename)

@server.route('/image/:relative#.+#')
def image(relative=''):
    global path_root

    #if not re.match('/', relative):
    #    relative = os.path.join(path_root, relative)

    print "SHOWING IMAGE: %s" % relative
    path = Path(relative, relative_prefix=path_root)
    if path.type() == "Image":
        return static_file(relative, root=path_root)
    else:
        #TODO: raise 404
        pass


def load_groups(full_source):
    """
    allows for custom editing of json files if needed
    """
    groups = []
    if not os.path.exists(full_source):
        #to get original version started
        #collections.scenes should have been loaded already
        #and star_order calculated

        raise ValueError, "No order file: %s" % full_source

        #comment this out if you want to initialize a list from scratch:
        #groups = [ self.scenes.star_order, [], [], [], [], [], [], [], [], [], [], ]
    else:
        #destination = "order.txt"
        json_file = codecs.open(full_source, 'r', encoding='utf-8', errors='ignore')
        lines = json_file.readlines()
        #split up the object so it is easier to edit
        split = ''
        for line in lines:
            line = line.replace(',]', ']')
            line = line.replace(', ]', ']')
            split += line.strip() + ' '

        #split = json_file.read()
        #split.replace('\r\n', '')
        #split.replace('\r', '')
        #split.replace('\n', '')
        #print split
        try:
            groups = json.loads(split)
        except:
            #try to pinpoint where the error is occurring:
            print split

            #get rid of outer list:
            split = split[1:-1]
            parts = split.split('], ')
            assert len(parts) == 11
            count = 0
            for p in parts:
                p = p + ']'
                try:
                    group = json.loads(p)
                except:
                    new_p = p[1:-1]
                    tags = new_p.split('", "')
                    summary = ''
                    for tag in tags:
                        summary += tag + "\n"

                    #print count
                    #print summary
                    print "%s - %s" % (count, summary)
                    #raise ValueError, "Trouble loading JSON in part %s: %s" % (count, p)
                    raise ValueError, "Trouble loading JSON in part %s: %s" % (count, summary)
                count += 1


            #raise ValueError, "Trouble loading JSON: %s" % split
        json_file.close()
        #groups = load_json(destination)

    return groups


def save_groups(destination, ordered_list):
    """
    similar to save json, but custom formatting to make editing easier

    to load, use collection.load_groups
    
    """
    #print "Saving: %s" % ordered_list
    #print "To: %s" % destination
    #journal = merge_simple(ordered_list, cloud_file)

    json_file = codecs.open(destination, 'w', encoding='utf-8', errors='ignore')
    #print "JSON FILE OPEN"
    split = json.dumps(ordered_list)
    split = split.replace('], ', ', ], \n')
    split = split.replace(']]', ', ]]')
    #print "Split version: %s" % split
    json_file.write(split)
    json_file.close()    
        

@server.post('/save_tabs/:relative#.+#')
@server.post('/save_tabs/')
@server.post('/save_tabs')
def save_tabs(relative=''):
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)

    if not relative:
        #could set a default here if it is desireable
        print "NO DESTINATION SENT!"
    elif not re.match('/', relative):
        relative = path_root + relative

    
    #destination = Path(relative, relative_prefix=path_root)
    destination = relative

    #print destination
    
    #debug:
    #print dir(request.forms)
    #print "Keys: %s" % (request.forms.keys())
    #print "Values: %s" % (request.forms.values())
    
    #gets a string
    cloud    = request.forms.get('cloud')
    #gets a list
    #cloud    = request.forms.getlist('cloud[]')
    
    #print cloud
    ordered_list = json.loads(cloud)

    #print ordered_list

    #save_json(destination, ordered_list)
    save_groups(destination, ordered_list)
    
    #d = open(destination, 'w')
    #d.write(' '.join(ordered_list))
    
    #return "Name: %s, Password: %s" % (name, password)
    return "Success!"

@server.route('/sort/:relative#.+#')
def sort(relative=''):
    """
    accept a path to a moment log and enable sorting on the items
    using jquery ui for a drag and drop interface
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    if not re.match('/', relative):
        relative = path_root + relative

    #set some defaults here...
    #if they've been changed, this will get over written on load
    groups = { "all":[], "edit":[], "slide1":[], "slide2":[], "slide3":[], "slide4":[], "slide5":[], "slide6":[], "slide7":[], "slide8":[], "slide9":[], }

    tab_order = ['all', 'edit', "slide1", "slide2", "slide3", "slide4", "slide5", "slide6", "slide7", "slide8", "slide9"]

    path = Path(relative, relative_prefix=path_root)
    print path
    if path.exists() and path.type() == "Directory":
        response = "Error: need a file name to store the meta data in<br>"
        response = "You supplied a directory path: %s<br>" % path
        return response
    else:
        parent_directory = path.parent()
        if path.extension == ".txt":
            #create a text journal if we don't have one
            if not path.exists():
                #convert images to journal
                #print "PARENT: %s" % parent_directory
                directory = parent_directory.load()
                #print "directory: %s, of type: %s" % (directory, type(directory))
                directory.create_journal(journal=path.filename)
                #journal = path.load_journal(create=True)

            journal = path.load_journal()
            items = []
            for e in journal.entries():
                new_p = os.path.join(str(parent_directory), e.data.strip())
                #print new_p
                p = Path(new_p)
                #print p.exists()
                items.append(p)

            #initial version of groups:
            destination = Path(relative)
            destination.extension = '.json'

            groups['all'] = items
            
        elif path.extension == ".json":
            #we can make the initial version here...
            #skip the generation of a moments log step
            if not path.exists():
                directory = parent_directory.load()
                #print "directory: %s, of type: %s" % (directory, type(directory))
                directory.sort_by_date()
                directory.scan_filetypes()
                
                groups['all'] = directory.images
                
            else:
                loaded = load_groups(str(path))
                #template expects all items in groups to be Path objects.
                #do that now
                groups = {}
                for key, value in loaded.items():
                    groups[key] = []
                    for v in value:
                        groups[key].append(Path(v))
            
            destination = Path(relative)

        else:
            #dunno!
            print "UNKNOWN FILE TYPE: %s" % relative
            groups = {}
            destination = None

        #clean up tab_order as needed
        for key in groups.keys():
            if not key in tab_order:
                tab_order.append(key)
        for item in tab_order[:]:
            if item not in groups.keys():
                tab_order.remove(item)

        print tab_order
        
        #return template('sort', path=path, items=items)
        return template('sort', path=path, groups=groups, destination=destination, tab_order=tab_order)
    
@server.route('/series/:type/:relative#.+#')
@server.route('/series/:relative#.+#')
@server.route('/series/')
@server.route('/series')
def series(type="Image", relative=''):
    """
    show the current item in a series
    along with links to previous and next
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    if not re.match('/', relative):
        relative = os.path.join(path_root, relative)

    path = Path(relative, relative_prefix=path_root)
    if path.type() != "Directory":
        parent = path.parent()
        parent_dir = parent.load()
        #parent_dir.sort_by_date()
        parent_dir.scan_filetypes()
        if path.type() == "Image":
            count = 0
            position = None
            for i in parent_dir.images:
                if str(i) == str(path):
                    position = count
                    break
                count += 1

            if position is None:
                raise ValueError, "Couldn't find matching image in directory: %s" % str(parent)
            else:
                if position != 0:
                    prev_pos = position-1
                else:
                    prev_pos = 0
                previous = parent_dir.images[prev_pos]

                nexts = []
                next_len = 5
                end = position + next_len
                if end >= len(parent_dir.images):
                    nexts = parent_dir.images[position+1:]
                else:
                    nexts = parent_dir.images[position+1:end]

                return template('series', path=path, parent=parent, previous=previous, nexts=nexts)

@server.route('/path/:relative#.+#')
@server.route('/path/')
@server.route('/path')
def path(relative=''):
    """
    serve a static file

    this also allows pose to function as a customizable file system browser

    be careful with what you set path_root to
    if the machine you run this on has sensitive information
    and is connected to a public network
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    ## else:
    ##     relative = os.path.join('/', relative)
    ##     full = os.path.abspath(relative)
    ## print full

    full_path = os.path.join(path_root, relative)
 
    path = Path(full_path, relative_prefix=path_root)
    if path.type() == "Directory":
        node = path.load()
        #will depend what we want to sort by here:
        node.sort_by_path()
        #node.sort_by_date()
        return template('directory', path=path, contents=node.contents)
    else:
        #this is equivalent to a view...
        #indicate it in the log:
        #path.log_action()
        return static_file(relative, root=path_root)

@server.route('/now')
def now(relative=''):
    return template('now')

@server.route('/')
def index():
    global path_root
    return template('home', path_root=path_root)
    
#port = 8088
#start the server loop
#run(host='localhost', port=8088)
run(app=server, host='localhost', port=port)
