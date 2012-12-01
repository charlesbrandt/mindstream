#!/usr/bin/env python
# ----------------------------------------------------------------------------
# moments
# Copyright (c) 2009-2010, Charles Brandt
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ----------------------------------------------------------------------------
"""
# Description:

this serves as an example for setting up an extraction using manager.extract_tags function

# By: Charles Brandt [code at contextiskey dot com]
# On: *2009.07.10 10:09:38 
# License:  MIT

"""

from moments.filters import extract_tags, ExtractConfig

configs = []

#DEMO
c1 = ExtractConfig()
c1.name = "DEMO"
#following can be a directory or a file:
c1.source = "/c/outgoing/journal.txt"
#leave these tags out when finished (usually want path prefix tags here):
c1.ignores = ['c', 'outgoing']
c1.extractions = [
    (["purchased"], "/c/outgoing/purchased.txt"),
    #([""], ""),
    ]
configs.append(c1)


#BLANK
## cx = ExtractConfig()
## cx.name = "BLANK"
## cx.source = ""
## cx.ignores = []
## cx.extractions = [
##     #([""], ""),
##     ]
## configs.append(cx)

for c in configs:
    print "Running extraction for: %s" % c.name
    extract_tags(c.source, c.extractions, c.ignores, save=True)
  
