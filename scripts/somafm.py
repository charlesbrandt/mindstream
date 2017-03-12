#!/usr/bin/env python
"""
script to scrape what is currently playing on somafm and make a note (moment) for it.

requires BeautifulSoup

for other screen scraping related tasks, see my 'communicate' python module
"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
import urllib.request, urllib.error, urllib.parse, os, sys
import BeautifulSoup

#should allow the script to find moments module without installing it to python library
sys.path.append(os.path.dirname(os.getcwd()))

from moments.timestamp import Timestamp
from moments.journal import Journal
from moments.path import Path

def lookup_playing(channel_id="groovesalad"):
    url = "http://somafm.com/%s/played" % channel_id
    response = urllib.request.urlopen(url)
    html = response.read()    
    soup = BeautifulSoup.BeautifulSoup(html)
    #print soup.prettify()
    #tags = soup.findAll('div')
    #tags = soup.findAll('div', 'playinc')
    #container = soup.find('div', 
    #                      tags = soup.findAll('posts')
    tags = soup.findAll('div', attrs={'id':'playinc'})
    #print len(tags)
    #print tags
    parts = []
    url = ''
    for t in tags:
        rows = t.findAll('tr')
        #print len(rows)
        first = rows[2]
        tds = first.findAll('td')
        for td in tds:
            #print td
            if td and len(td.contents):
                link = td.findAll('a')
                if len(link):
                    #print link
                    if len(link[0].contents):
                        text = link[0].contents[0]
                        url = link[0]['href']
                    else:
                        print("No link: %s" % link)
                        text = ''
                else:
                    text = td.contents[0]
                    text = text.replace('&nbsp; ', ' ')
                parts.append(text)
                #print content

    #print parts
    #print url

    if os.path.exists('/c/music'):
        dest = '/c/music/radio/somafm.txt'
        j = Journal(dest)
        tags = [ channel_id ]
    else:
        now = Timestamp()
        today = now.compact(accuracy="day")
        today_log = Path(os.path.join('/c/outgoing', now.filename()))
        dest = str(today_log)
        j = today_log.load_journal()
        tags = [ 'music', 'radio', 'somafm', channel_id, 'plus' ]


    data = " - ".join(parts)
    #print data

    data += '\n' + url

    e = j.make(data, tags)
    j.save(dest)

    print("")
    print(e.render())    
    print("Saved to: %s" % dest)

def main():
    #valid channel_ids are:
    # groovesalad, u80s, ...
    # (the part that shows up in the url of the currently playing page)
    if len(sys.argv) > 1:
        #skip the first argument (filename):
        for arg in sys.argv[1:]:
            lookup_playing(arg)
    else:
        lookup_playing()
            
if __name__ == '__main__':
    main()
    
