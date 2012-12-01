#!/usr/bin/env python
"""
#
# Description:

# a simple wxpython application

# By: Charles Brandt [code at contextiskey dot com]
# On: [date]
# License:  MIT 

# Requires:
# wx

# TODO:
*2011.11.15 04:26:55
incorporate commands from areui.examples.text_input
no need to reinvent the wheel (but the editor is needed)

*2011.11.15 04:28:11
breathe
"""
import os, time, re
import wx

from moments.timestamp import Timestamp
from moments.journal import Journal

# The wx.App object must be created first!
#app = wx.App()
# this allows debugging to go to the console!
app = wx.App(0)

class Buffer(object):
    """
    provide common tasks for navigating a text buffer
    similar in concept to a moment.log item (once saving happens here)
    """
    def __init__(self, text):
        self.text = text

    def make_words(self):
        temps = self.text.split()
        print temps

    ## def previous_word(self, position):
    ##     """
    ##     find the starting position of the previous word
    ##     """
    ##     self.make_words()
        
    ## def next_word(self, position):
    ##     """
    ##     find the starting position of the next word
    ##     """
    ##     self.make_words()
        

    def make_lines(self):
        temps = self.text.splitlines()
        self.lines = []
        #want to add the newline character back in, so that the count is accurate
        for l in temps:
            l += '\n'
            self.lines.append(l)
            #unicode has no append
            #l.append('\n')

        #print self.lines
    def find_line_number(self, position):
        self.make_lines()
        line_number = -1
        looking_position = 0
        while (looking_position <= position) and (line_number <= len(self.lines)):
            line_number += 1
            line = self.lines[line_number]
            looking_position += len(line)
        #print line_number
        return line_number
                                                  
    def start_of_line(self, cur_position):
        """
        find the position of the start of the requested line
        (in total characters from buffer start)
        lines are indexed from 0
        """
        line_number = self.find_line_number(cur_position)
        self.make_lines()
        position = 0
        for i in range(line_number):
            position += len(self.lines[i])
        return position

    def end_of_line(self, cur_position):
        """
        find the position of the end of the requested line
        (in total characters from buffer start)
        lines are indexed from 0
        """
        line_number = self.find_line_number(cur_position)
        self.make_lines()
        position = 0
        for i in range(line_number+1):
            position += len(self.lines[i])
        return position

class MainPanel(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        #initialize cur_stamp to be empty
        self.cur_stamp = None
        
        #self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundColour(wx.BLACK)

        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_KEY_DOWN, self.OnChar)

        self.box = wx.BoxSizer(wx.VERTICAL)

        self.textbox = wx.TextCtrl(self, -1, "",
                                   #size=(200, 100),
                                   style=wx.TE_MULTILINE|wx.TE_RICH2|wx.BORDER_NONE|wx.TE_CENTRE)
        self.textbox.SetBackgroundColour(wx.BLACK)
        self.textbox.SetForegroundColour(wx.WHITE)
        #second color is for text background
        #no effect
        #self.textbox.SetDefaultStyle(wx.TextAttr("WHITE", "BLACK"))
        #self.textbox.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        #no effect
        #self.textbox.SetStyle(0, 100, wx.TextAttr("WHITE", "BLACK"))
        
        self.textbox.Bind(wx.EVT_KEY_DOWN, self.OnChar)
        self.textbox.Bind(wx.EVT_MOTION, self.OnMotion)
        #s = moment.render()
        #self.text = wx.StaticText(self, -1, s, (20, 120))
        #self.text.SetFont(self.font)
        #self.box.Add(self.textbox, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        self.box.Add(self.textbox, 1, wx.EXPAND)

        self.SetSizer(self.box)

        self.new_stamp()

        self.SetAutoLayout(True)
        self.SetFocus()

    def check_first_line(self):
        """
        add our saved timestamp in if it wasn't there already
        """
        buf = Buffer(self.textbox.GetValue())
        buf.make_lines()
        if not buf.lines or not re.match('\*', buf.lines[0]):
            self.textbox.SetInsertionPoint(0)
            self.textbox.WriteText( "*%s \n" % (str(self.cur_stamp)) )
            
    def new_stamp_pt2(self):
        """
        this does the actual timestamping
        """
        self.textbox.SetBackgroundColour(wx.BLACK)
        self.SetBackgroundColour(wx.BLACK)
        self.Refresh()
        #self.textbox.SetBackgroundColour(wx.WHITE)
        #self.textbox.SetForegroundColour(wx.BLACK)

        #if we have data, or we've already set the cur_stamp previously
        #then we're ready to add a new visible stamp
        if self.textbox.GetValue() or self.cur_stamp:
            self.check_first_line()
            self.textbox.SetInsertionPoint(0)
            #WriteText inserts automatically. no need to duplicate manually
            self.cur_stamp = Timestamp()
            self.textbox.WriteText( "*%s \n\n" % (str(self.cur_stamp)) )
            # +2 is for '*' and trailing space (' ')
            insert = len(str(self.cur_stamp)) + 2 
            #print insert
            self.textbox.SetInsertionPoint(insert)
            self.cur_stamp = None
        else:
            #print "No content in buffer... keeping timestamp locally"
            #just keep track of current stamp in memory..
            #we can add it on subsequent entries
            self.cur_stamp = Timestamp()

    def new_stamp(self):
        """
        start by flashing the screen momentarily
        """
        #self.SetBackgroundColour(wx.LIGHT_GRAY)
        #self.textbox.SetBackgroundColour(wx.LIGHT_GRAY)
        #self.SetBackgroundColour(wx.Colour(192, 192, 192, 255))
        #self.textbox.SetBackgroundColour(wx.Colour(192, 192, 192, 255))
        self.SetBackgroundColour(wx.Colour(128, 128, 128, 255))
        self.textbox.SetBackgroundColour(wx.Colour(128, 128, 128, 255))
        self.Refresh()
        #flash the white screen for short time
        wx.CallLater(100, self.new_stamp_pt2)
        
    def process_entries(self, today_path):
        #merge blank entries with tags with previous entry with data
        j = Journal(today_path)
        #tags_to_add = []
        also = None
        for entry in j.entries()[:]:
            if also:
                #print "Adding %s tag to %s" % (tags_to_add, entry.render())
                also.tags.remove('also')
                entry.tags.union(also.tags)
                if also.has_data():
                    entry.data += "[%s]\n" % also.created
                    entry.data += also.data
                j.remove(also)
                also = None
            if "also" in entry.tags:
                also = entry

            #other commands (watcher, etc) go here
                
            #*2011.11.21 08:01:09 
            #the following will automatically take any entries with tags
            #but no data
            #and merge the blank entry's tags with the previous entry
            #
            #don't always want to do this.
            #Instead, see "also" tags processing above
            ## #print entry.created
            ## if not entry.has_data():
            ##     if entry.tags.to_tag_string():
            ##         #print "Blank: %s" % entry.created
            ##         #print "have tags too!"
            ##         for tag in entry.tags:
            ##             tags_to_add.append(tag)
            ##         #for now just remove the ones with tags
            ##         #completely blank ones can stay in
            ##         j.remove(entry)
            ## else:
            ##     if tags_to_add:
            ##         #print "Adding %s tag to %s" % (tags_to_add, entry.render())
            ##         entry.tags.union(tags_to_add)
            ##         tags_to_add = []                    
            ##     #print "DATA: %s" % entry.render()
            ##     #j.remove

        j.save(today_path)

    def save(self):
        today_path = os.path.join('/c/outgoing', Timestamp().filename())
        if os.path.exists(today_path):
            today_file = open(today_path, 'r')
            today_buffer = today_file.read()
            today_file.close()
        else:
            today_buffer = ''

        today_file = open(today_path, 'w')

        self.check_first_line()
        current = self.textbox.GetValue()
        if not current[-2:] == '\n\n':
            if current[-1] == '\n':
                current += '\n'
            else:
                current += '\n\n'

        today_file.write(current)
        today_file.write(today_buffer)
        today_file.close()

        self.process_entries(today_path)

        #self.input.content.text = ''
        self.textbox.Clear()

        self.new_stamp()
        

    def OnChar(self, evt):
        cursor = wx.StockCursor(wx.CURSOR_BLANK)
        self.GetParent().SetCursor(cursor)

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


        if keycode == wx.WXK_ESCAPE:
            self.save()
            exit()
        elif evt.ControlDown() and keyname == "F":
            if self.GetParent().fullscreen:
                self.GetParent().fullscreen = False
                self.GetParent().ShowFullScreen(False)
            else:
                self.GetParent().fullscreen = True
                self.GetParent().ShowFullScreen(True)

        elif evt.ControlDown() and keyname == "S":
            self.save()
            
        # add a new datestamp
        elif evt.ControlDown() and keyname == "J":
            self.new_stamp()

        elif evt.ControlDown() and keyname == "E":
            #print "position: %s, line: %s" % (self.input.content.caret.position, self.input.content.caret.line)
            #print "text len: %s" % (len(self.input.content.text))
            buf = Buffer(self.textbox.GetValue())
            position = buf.end_of_line(self.textbox.GetInsertionPoint())
            #print "end of line: %s" % position
            self.textbox.SetInsertionPoint(position-1)
                
        elif evt.ControlDown() and keyname == "A":
            #print "position: %s, line: %s" % (self.input.content.caret.position, self.input.content.caret.line)
            #print "text len: %s" % (len(self.input.content.text))
            buf = Buffer(self.textbox.GetValue())
            position = buf.start_of_line(self.textbox.GetInsertionPoint())
            #print "start of line: %s" % position
            self.textbox.SetInsertionPoint(position)

        else:
            #print keyname
            evt.Skip()

    def OnMotion(self, evt):
        pass
        #cursor = wx.StockCursor(wx.CURSOR_POINT_LEFT)
        #self.GetParent().SetCursor(cursor)

#more common to subclass a wx.Frame or wx.Window
class MyFrame(wx.Frame):
    def __init__(self, parent):
        #print wx.Display().GetGeometry()
        (x, y, w, h) = wx.Display().GetGeometry()
        subh = h-82

        wx.Frame.__init__(self, parent, -1, 'edit', size=(w,subh))

        self.fullscreen = False
        self.SetBackgroundColour(wx.BLACK)
        
        #size here doesn't have an effect
        #self.main_panel = MainPanel(self, size=(400,400))
        #self.main_panel = MainPanel(self, size=(w,subh))

        self.main_panel = MainPanel(self)

        #show should come after bind:
        #self.ShowFullScreen(True)
        self.Show(True)
        
                
frame = MyFrame(None)

app.MainLoop()
