#!/usr/bin/env python
"""
#
# Description:

# wxPython based tagger / player interface

# By: Charles Brandt [code at contextiskey dot com]
# On: *2011.09.18 11:50:18 
# License:  MIT 

# Requires:
# wx, moments
"""

import wx, sys
import  wx.lib.scrolledpanel as scrolled

try:
    import json
except:
    import simplejson as json

from moments.path import load_journal
from moments.journal import Journal
#*2012.12.01 11:31:09
#recently moved out from mindstream modlue
#this was the only project using Items here...
#more common in media playlists
from medley.sources import Items

# The wx.App object must be created first!
#app = wx.App()
# this allows debugging to go to the console!
app = wx.App(0)

def OnChar(evt):
    #keyname = keyMap.get(keycode, None)
    keycode = evt.GetKeyCode()
    keyname = 'unknown'
    if keycode < 256:
        if keycode == 0:
            keyname = "NUL"
        elif keycode < 27:
            keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
        else:
            #keyname = "\"%s\"" % chr(keycode)
            keyname = chr(keycode)
    else:
        keyname = "(%s)" % keycode        

    try:
        keynum = int(keyname)
    except:
        keynum = -1

    global frame
    #global items

    if keycode == wx.WXK_ESCAPE:
        #save first
        j = Journal()
        j.update_many(frame.items)
        j.save(frame.source)

        exit()

    ## wx.WXK_LEFT : "WXK_LEFT",
    ## wx.WXK_UP : "WXK_UP",
    ## wx.WXK_RIGHT : "WXK_RIGHT",
    ## wx.WXK_DOWN : "WXK_DOWN",

    elif keycode == wx.WXK_RIGHT:
        m = frame.items.go_next()
        frame.main_panel.update_content(m)
        #this wouldn't clear content
        #seems that the wx way is to destroy then recreate
        #frame.main_panel.content.update(m)
        #doesn't seem to have an effect:
        #frame.main_panel.box.Remove(frame.main_panel.content)
        #this gets rid of it:
        #frame.main_panel.Refresh()
        #frame.main_panel.Update()
        #frame.main_panel.SetSizer(frame.main_panel.box)
        #print "right"

    elif keycode == wx.WXK_LEFT:
        m = frame.items.go_previous()
        frame.main_panel.update_content(m)

        #frame.main_panel.content.update(m)
        #print "left"
        
    elif keyname == "S":
        #do save here
        j = Journal()
        j.update_many(frame.items)
        j.save(frame.source)
        print "%s of %s" % (frame.items.position, len(frame.items))
        print "currently: %s" % (frame.items.get().created)
        
    elif keyname == "F":
        if frame.fullscreen:
            frame.fullscreen = False
            frame.ShowFullScreen(False)
            #self.GetParent().ShowFullScreen(False)
        else:
            frame.fullscreen = True
            frame.ShowFullScreen(True)
            
            #self.GetParent().ShowFullScreen(True)
        #print "fullscreen"
    elif keynum <= 9 and keynum >= 0:
        frame.find_tag(keynum)
    else:
        print keyname


    #print "key event handled"
    
class TagTally(object):
    def __init__(self, source=None):
        self.source = source
        self.tally = {}
        if self.source:
            f = open(self.source)
            try:
                self.tally = json.loads(f.read())
            except:
                pass

    def add(self, item):
        """
        look for item, add one to existing entry
        otherwise create a new one with value '1'
        """
        if self.tally.has_key(item):
            self.tally[item] += 1
        else:
            self.tally[item] = 1
            
    def reset(self):
        """
        go through all tags and reset the value to 0
        unless in tops, then give value of 1
        """
        tops = self.tops()
        for k in self.tally.keys():
            if k in tops:
                self.tally[k] = 1
            else:
                self.tally[k] = 0

    def sorted(self):
        """
        return all keys, ordered by highest tally
        """
                
        items = self.tally.items()
        swap = []
        for i in items:
            swap.append( (i[1], i[0]) )
        swap.sort()
        swap.reverse()
        result = []
        for s in swap:
            result.append(s[1])
        return result

    def tops(self):
        """
        return the top 10 keys
        """
        return self.sorted()[:10]

    def remainder(self):
        """
        everything but the tops
        """
        everything = self.sorted()
        return everything[10:]
    
    def save(self, source=None):
        if source:
            self.source = source

        if not self.source:
            print "need a source to save"
            exit()

        f = open(self.source, 'w')
        f.write(json.dumps(self.tally))
        
class TagInput(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.WHITE)

        #sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
        #              #'this is a long item that needs a scrollbar...',
        #              'six', 'seven', 'eight']
        sampleList = self.GetParent().tally.remainder()

        self.cb = wx.ComboBox(self, 500, "tag", (0, 2), 
                         (170, -1), sampleList,
                         wx.CB_DROPDOWN
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.cb)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.cb)
        self.cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        # Once the combobox is set up, we can append some more data to it.
        #self.cb.Append("foo", "This is some client data for this item")

    def update(self, data):
        parent = self.GetParent()
        parent.update_buttons(data)
        #this should be updated after update_buttons
        items = parent.tally.remainder()
        self.cb.Clear()
        for i in items:
            self.cb.Append(i)
        parent.tally.save()
        parent.GetParent().add_tag(data)
        parent.focus_button.SetFocus()
        
    # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        #data1 = cb.GetClientData(evt.GetSelection())
        data = evt.GetString()
        #print "combobox update: %s, %s" % (data, data1)
        self.update(data)
        #self.log.WriteText('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        #if evt.GetString() == 'one':
        #    self.log.WriteText("You follow directions well!\n\n")

    # Capture events every time a user hits a key in the text entry field.
    def EvtText(self, evt):
        #self.log.WriteText('EvtText: %s\n' % evt.GetString())
        evt.Skip()

    # Capture events when the user types something into the control then
    # hits ENTER.
    def EvtTextEnter(self, evt):
        #self.log.WriteText('EvtTextEnter: %s' % evt.GetString())
        data = evt.GetString()
        self.update(data)
        #evt.Skip()

    def OnSetFocus(self, evt):
        #print "OnSetFocus"
        evt.Skip()

    def OnKillFocus(self, evt):
        #print "OnKillFocus"
        evt.Skip()

class ButtonPanel(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.SetBackgroundColour(wx.WHITE)

        self.buttons = []

        box = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(1, 11):
            value = i % 10
            b = wx.Button(self, i, '%s.' % value)

            b.Bind(wx.EVT_CHAR, OnChar)
            b.Bind(wx.EVT_KEY_DOWN, OnChar)

            self.Bind(wx.EVT_BUTTON, self.OnClick, b)
            box.Add(b, 1, wx.EXPAND)
            self.buttons.append(b)

        self.SetSizer(box)
        self.SetAutoLayout(True)

            
    def OnClick(self, event):
        #print "Click! (%d)\n" % event.GetId()
        value = event.GetId() % 10
        self.GetParent().GetParent().find_tag(value)
                
class Content(scrolled.ScrolledPanel):
    def __init__(self, parent, moment, **kwargs):
        scrolled.ScrolledPanel.__init__(self, parent, -1)

        self.SetBackgroundColour(wx.WHITE)
        #self.log = log

        self.font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        s = moment.render()
        self.text = wx.StaticText(self, -1, s, (20, 120))
        self.text.SetFont(self.font)
        self.vbox.Add(self.text, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.SetSizer(self.vbox)
        
        self.SetAutoLayout(True)
        self.SetupScrolling()

        self.Bind(wx.EVT_CHAR, OnChar)
        self.Bind(wx.EVT_KEY_DOWN, OnChar)

        #*2011.09.20 09:25:44
        # if events are triggered by the panel by key 
        # that lead to deleting this panel
        # causes segmentation fault when it is no longer available. 
        #This works (maybe too well)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

    def OnMouse(self, evt):
        self.SetFocus()
        
    ## def update(self, moment):
    ##     #self.vbox = wx.BoxSizer(wx.VERTICAL)
    ##     #self.vbox.Clear()
    ##     s = moment.render()
    ##     new_text = wx.StaticText(self, -1, s, (20, 120))
    ##     new_text.SetFont(self.font)
    ##     self.vbox.Replace(self.text, new_text)
    ##     self.text = new_text
    ##     #self.SetSizer(self.vbox, deleteOld=True)
    
class MainPanel(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        self.tally = TagTally("tags.txt")

        self.Bind(wx.EVT_CHAR, OnChar)
        self.Bind(wx.EVT_KEY_DOWN, OnChar)
        
        self.SetBackgroundColour(wx.WHITE)


        self.box = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.back_button = wx.Button(self, label="<", size=(25,35))
        self.Bind(wx.EVT_BUTTON, self.back, self.back_button)
        hbox.Add(self.back_button, 0, wx.EXPAND)
        self.back_button.Bind(wx.EVT_CHAR, OnChar)
        self.back_button.Bind(wx.EVT_KEY_DOWN, OnChar)

        #also using as forward button now
        #way to bind OnChar hotkeys without triggering a real tag event
        self.focus_button = wx.Button(self, label=">", size=(25,35))
        self.Bind(wx.EVT_BUTTON, self.forward, self.focus_button)
        hbox.Add(self.focus_button, 0, wx.EXPAND)
        self.focus_button.Bind(wx.EVT_CHAR, OnChar)
        self.focus_button.Bind(wx.EVT_KEY_DOWN, OnChar)

        self.tag_input = TagInput(self, size=(140,35))
        hbox.Add(self.tag_input, 0, wx.EXPAND)

        self.button_panel = ButtonPanel(self, size=(350,35))
        self.update_buttons()

        hbox.Add(self.button_panel, 1, wx.EXPAND)        

        self.box.Add(hbox, 0, wx.EXPAND)
        m = self.GetParent().items.get()
        #global items
        #m = items.get()
        self.content = Content(self, m, size=(200,35))
        self.box.Add(self.content, 1, wx.EXPAND)

        self.SetSizer(self.box)


        self.SetAutoLayout(True)
        self.SetFocus()

    def update_buttons(self, data=None):
        #print "UPDATE BUTTONS"

        if data:
            self.tally.add(data)

        #    #not going to make a button unless it becomes frequent enough
        #    self.button_panel.buttons[0].SetLabel(label="1.%s" % data)
        tops = self.tally.tops()
        for i in range(0,10):
            val = (i+1) % 10
            if len(tops) > i:
                text = tops[i]
            else:
                text = ''
            label = "%s.%s" % (val, text)
            self.button_panel.buttons[i].SetLabel(label)
        self.tally.save()


    def update_content(self, moment):
        """
        updates the content
        """
        ## frame.main_panel.content.Destroy()
        ## frame.main_panel.content = Content(frame.main_panel, m, size=(200,35))
        ## frame.main_panel.box.Add(frame.main_panel.content, 1, wx.EXPAND)
        ## frame.main_panel.Layout()

        self.content.Destroy()
        self.content = Content(self, moment, size=(200,35))
        self.box.Add(self.content, 1, wx.EXPAND)
        self.Layout()

    def forward(self, evt):
        m = self.GetParent().items.go_next()
        self.update_content(m)
        
    def back(self, evt):
        m = self.GetParent().items.go_previous()
        self.update_content(m)
        
class MyFrame(wx.Frame):
    def __init__(self, parent, source="/c/private/journal.txt"):
        wx.Frame.__init__(self, parent, -1, 'tag', size=(1000,400))

        self.fullscreen = False

        self.source = source
        j = load_journal(self.source)
        self.items = Items(j.entries())

        #panel = wx.Panel(self, -1)
        self.main_panel = MainPanel(self, size=(400,400))
            
        #show should come after bind:
        #self.ShowFullScreen(True)
        self.Show(True)
        
    def find_tag(self, number):
        """
        add the tag to the current moment
        """
        #global items
        #global frame
        #print "Adding tag in space: %s" % number
        label = self.main_panel.button_panel.buttons[number-1].GetLabel()
        #print "Label is: %s" % label
        (prefix, tag) = label.split('.')
        tag.strip()
        self.add_tag(tag)

    def add_tag(self, tag):
        moment = self.items.get()
        #print "to moment: %s" % moment.render()
        if tag and not tag in moment.tags:
            moment.tags.append(tag)
        #print "replacing on screen"
        self.items.replace(moment)
        #print "updating buttons"
        self.main_panel.update_content(moment)
        #print "buttons updated"

def usage():
    print "pass in the journal source you want to tag"

if len(sys.argv) > 1:
    helps = ['--help', 'help', '-h']
    for i in helps:
        if i in sys.argv:
            usage()
            exit()
    #skip the first argument (filename):
    frame = MyFrame(None, sys.argv[1])
else:
    frame = MyFrame(None)

app.MainLoop()
