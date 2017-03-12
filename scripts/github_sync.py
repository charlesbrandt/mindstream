#!/usr/bin/env python
"""
# By: Charles Brandt [code at contextiskey dot com]
# On: *2014.06.18 07:42:57 
# License:  MIT

#
# Description:
I like to keep track of items todo for a project in a simple text (moments) list.  However, it is useful to share this with others involved with the project.

This script takes a moment todo list and automatically synchronizes it with a github issues list.

python /c/mindstream/scripts/github_sync.py [source_log] [target_repository] [github personal access token]

target_repository should include :owner/:repo
"""
from __future__ import print_function

import sys, os, re
import json

import requests

from moments.journal import Journal
from moments.log import Log

def usage():
    print(__doc__)
    
def sync_log(source, repo, token):
    """
    """
    result = ''
    
    #r = requests.get('https://github.com/timeline.json')
    headers = {
        #this should be your own github username:
        #https://developer.github.com/v3/#user-agent-required
        'User-Agent': 'charlesbrandt',
        }

    #issues = 'https://api.github.com/repos/:owner/:repo/issues' % 
    issues = 'https://api.github.com/repos/%s/issues' % (repo)

    j = Journal()
    j.load(source)
    print(len(j.entries()))
    public = j.tag("public")
    print(len(public))
    #for entry in public[:2]:
    for entry in public[:]:
        #check if entry already has an issues:# tag in it...
        #if so we don't need to re-add it
        added = False
        for tag in entry.tags:
            if re.search('issue', tag):
                print("SKIPPING: ", entry.data.splitlines()[0])
                print("item already added as: %s" % tag)
                added = True

        if not added:
            print("ADDING: ", entry.data.splitlines()[0])

            
            ## values = { 'title': 'test issue',
            ##            'body': 'more details here',
            ##            'assignee': 'charlesbrandt'
            ##            }

            values = { 'title': entry.data.splitlines()[0],
                       'body': '\n'.join(entry.data.splitlines()[1:]),
                       'assignee': 'charlesbrandt'
                       }
            print(values)

            r = requests.post(issues, headers=headers, auth=(token, 'x-oauth-basic'), data=json.dumps(values))
            #print r
            #print r.text
            result = r.json()
            print(list(result.keys()))

            #now add an 'issue:#' tag to the entry, so it can be associated
            issue_tag = "issue:%s" % result['number']
            entry.tags.append(issue_tag)


    #now go through and mark items complete
    #if they are not in github issues any longer

    r = requests.get(issues, headers=headers, auth=(token, 'x-oauth-basic'))

    #print dir(r)
    #print r
    #print r.json()


    #similarly, should go through local list
    #show any open issues on github that are not in local list
    #these may need to be managed manually...
    #they could be open items added by some other mechanism
    #or they could be items that were completed locally and should be closed

    j.save(source)
    #j.save('temp.txt')

    
def main():
    if len (sys.argv) > 1:
        if sys.argv[1] in ['--help','help'] or len(sys.argv) < 2:
            usage()
        source = sys.argv[1]
        if len(sys.argv) > 3:
            repo = sys.argv[2]
            #the personal access token, available:
            #https://github.com/settings/applications#personal-access-tokens
            token = sys.argv[3]
            sync_log(source, repo, token)

        else:
            usage()

    else:
        usage()
        
if __name__ == '__main__':
    main()
