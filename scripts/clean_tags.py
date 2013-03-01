"""
Sometimes tags get accumulated that are not helpful
this helps remove them more easily

*2011.06.16 11:02:17
script to load a journal
then for each entry with a specified tag,
remove that tag from the entry
and save the entry to the original source
(load source, update old entry with new one, save source)
"""

from moments.path import load_journal, Path


def clean_tag(remove_tag, journal):
    """
    accept a tag and a previously loaded journal
    go through all entries in journal
    look for tag to remove
    when found in an entry
    load that entry's source (e.path)
    remove tag from those entries
    resave the log
    """
    for e in journal:
        if remove_tag in e.tags:
            log_j = load_journal(e.path)
            #go ahead and re-scan all entries in this log:
            for log_e in log_j:
                if remove_tag in log_e.tags:
                    path = Path(e.path)

                    #if we're working with date tags, and the date tag
                    #is different from the entry date, keep it around for now
                    if remove_tag != path.name:
                        print "tag (%s) different than filename (%s) date" % (remove_tag, path.name)
                    else:
                        print "REMOVING TAG: %s from: %s" % (remove_tag, e.path)
                        #print e.render()
                        #print e.path

                        log_e.tags.remove(remove_tag)

            #over-write original log with these updates
            log_j.to_file(e.path)


source = '/c/journal'
j1 = load_journal(source)

#remove_tag = '20091006'
tag_string = """20081023 20081025"""

tags = tag_string.split()
for t in tags:
    clean_tag(t, j1)
