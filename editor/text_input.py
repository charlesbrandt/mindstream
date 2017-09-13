#! /usr/bin/env python
"""
example to illustrate the use of a text_input area

for stray keys on thinkpad/ubuntu, edit:
/c/downloads/python/pyglet/pyglet/window/xlib/__init__.py

around line 951:
            # Issue 353: Symbol is uppercase when shift key held down.
            try:
                symbol = ord(unichr(symbol).lower())
            except:
                # on a thinkpad running Ubuntu can get:
                #ValueError: unichr() arg not in range(0x110000) (wide Python build)
                # when a "Fn" + key is pressed
                # this ignores those presses.
                symbol = None

*2011.11.17 21:41:14 
This pyglet based version of a simple moments editor is not as reliable, not as efficient, and not as complete as the wx based version: edit.py
The approach is very similar in both of them.
"""
from __future__ import print_function
from builtins import str
from builtins import range
from builtins import object

import os
import pyglet
# disable error checking for increased performance
pyglet.options['debug_gl'] = False

#from areaui import *
from areaui.area import Area, RootArea
from areaui.widgets import TextInput, TextArea

from moments import Timestamp

class Buffer(object):
    """
    provide common tasks for navigating a text buffer
    similar in concept to a moment.log item (once saving happens here)
    """
    def __init__(self, text):
        self.text = text

    def make_words(self):
        temps = self.text.split()
        print(temps)

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
        
    def start_of_line(self, line_number):
        """
        find the position of the start of the requested line
        (in total characters from buffer start)
        lines are indexed from 0
        """
        self.make_lines()
        position = 0
        for i in range(line_number):
            position += len(self.lines[i])
        return position

    def end_of_line(self, line_number):
        """
        find the position of the end of the requested line
        (in total characters from buffer start)
        lines are indexed from 0
        """
        self.make_lines()
        position = 0
        for i in range(line_number+1):
            position += len(self.lines[i])
        return position

class Editor(pyglet.window.Window):
    def __init__(self, source=None, **kwargs):
        pyglet.window.Window.__init__(self, **kwargs)
        fullscreen = kwargs.get("fullscreen", False)
        if fullscreen:
            self.set_fullscreen(fullscreen)

        self.border = 5

        #self.layer = RootArea(self, color=(1.0, 1.0, 1.0, 1.0))
        self.layer = RootArea(self, color=(0, 0, 0, 1.0))
        self.input = TextInput('', self.width-self.border*2, self.height-self.border*2, x=self.border, y=self.border, color=(255, 255, 255, 255))
        self.layer.add(self.input)

        self.layer.update_layout()
        self.push_handlers(self.layer)
        self.input.set_focus()

        self.input.content.caret.visible = True
        self.new_stamp()

    def on_draw(self):
        self.clear()
        self.layer.draw()

    def new_stamp(self):
        self.input.content.text = "*%s \n\n%s" % (str(Timestamp()), self.input.content.text)
        self.input.content.caret.position = 21

    def resize_input(self):
        pos = self.input.content.caret.position
        print("Pos pre: %s" % pos)
        self.pop_handlers()
        buf = Buffer(self.input.content.text)
        self.input.unset_focus()
        self.layer.remove(self.input)
        self.layer.rearrange()
        del self.input
        self.input = TextInput('in', self.width-self.border*2, self.height-self.border*2, x=self.border, y=self.border, color=(255, 255, 255, 255))
        #self.input = TextInput('in', self.width, self.height)
        self.input.content.text = buf.text
        self.layer.add(self.input)
        #need to call rearrange so that layer is using the right input
        #before setting various caret options
        #self.layer.rearrange()
        self.layer.update_layout()

        self.push_handlers(self.layer)
        self.input.set_focus()
        self.input.content.caret.visible = True
        self.input.content.caret.position = pos
        print("Pos post: %s" % self.input.content.caret.position)

    def on_key_press(self, symbol, modifiers):
        #for debugging:
        #print pyglet.window.key.symbol_string(symbol)

        #quit!
        #if key.symbol_string(symbol) == "ESCAPE":
        if symbol == pyglet.window.key.ESCAPE:
            if modifiers & pyglet.window.key.MOD_CTRL:
                exit()

        #save
        if symbol == pyglet.window.key.S:
            if modifiers & pyglet.window.key.MOD_CTRL:
                today_path = os.path.join('/c/outgoing', Timestamp().filename())
                if os.path.exists(today_path):
                    today_file = open(today_path, 'r')
                    today_buffer = today_file.read()
                    today_file.close()
                else:
                    today_buffer = ''
                    
                today_file = open(today_path, 'w')
                today_file.write(self.input.content.text)
                today_file.write(today_buffer)
                today_file.close()
                self.input.content.text = ''
                
                self.new_stamp()

        # add a new datestamp
        if symbol == pyglet.window.key.J:
            if modifiers & pyglet.window.key.MOD_CTRL:
                self.new_stamp()
                
        if (pyglet.window.key.symbol_string(symbol) == "F") and modifiers and (pyglet.window.key.MOD_CTRL == modifiers):
            if not self.fullscreen:
                self.set_fullscreen()
                self.resize_input()
                #print "window: %sx%s, layer: %sx%s, input: %sx%s" % (self.width, self.height, self.layer.w, self.layer.h, self.input.w, self.input.h)
                self.on_draw()
            else:
                self.set_fullscreen(fullscreen=False)
                self.resize_input()
                #print "window: %sx%s, layer: %sx%s, input: %sx%s" % (self.width, self.height, self.layer.w, self.layer.h, self.input.w, self.input.h)
                self.on_draw()

        #pyglet provides this already:
        ## if (pyglet.window.key.symbol_string(symbol) == "LEFT"):
        ##     if modifiers & pyglet.window.key.MOD_CTRL:
        ##         buf = Buffer(self.input.content.text)
        ##         position = buf.previous_word(self.input.content.caret.position)
                

        ## if (pyglet.window.key.symbol_string(symbol) == "RIGHT"):
        ##     if modifiers & pyglet.window.key.MOD_CTRL:
        ##         buf = Buffer(self.input.content.text)
        ##         position = buf.next_word(self.input.content.caret.position)

        if (pyglet.window.key.symbol_string(symbol) == "E"):
            if modifiers & pyglet.window.key.MOD_CTRL:
                #print "position: %s, line: %s" % (self.input.content.caret.position, self.input.content.caret.line)
                #print "text len: %s" % (len(self.input.content.text))
                buf = Buffer(self.input.content.text)
                position = buf.end_of_line(self.input.content.caret.line)
                #print "end of line: %s" % position
                self.input.content.caret.position = position-1
                
        if (pyglet.window.key.symbol_string(symbol) == "A"):
            if modifiers & pyglet.window.key.MOD_CTRL:
                #print "position: %s, line: %s" % (self.input.content.caret.position, self.input.content.caret.line)
                #print "text len: %s" % (len(self.input.content.text))
                buf = Buffer(self.input.content.text)
                position = buf.start_of_line(self.input.content.caret.line)
                #print "start of line: %s" % position
                self.input.content.caret.position = position
                
if __name__ == '__main__':
    editor = Editor(width=900, height=500, caption='text edit', vsync=True)

    #pyglet.clock.schedule_interval(check_dropped, 2)

    # finally, run the application...
    pyglet.app.run()

# this illustrates creating a main window
# and then passing that window into the main object for use by the application

## if __name__ == '__main__':
##     # create a basic pyglet window
##     window = pyglet.window.Window(900, 500, caption='text edit', vsync=True)
##     #window.set_fullscreen()

##     def on_key_press(symbol, modifiers):
##         if symbol == pyglet.window.key.ESCAPE:
##             if modifiers & pyglet.window.key.MOD_CTRL:
##                 exit()

##     #want to override the default so that ESCAPE is not available
##     window.on_key_press = on_key_press

##     @window.event
##     def on_draw():
##         window.clear()
##         experiment.draw()

##     #this must be after the on_draw decorator has been applied to window
##     experiment = Experiment(window)

##     #pyglet.clock.schedule_interval(check_dropped, 2)

##     # finally, run the application...
##     pyglet.app.run()

# another common approach is to subclass window itself
# and put all main application logic there
# examples of this are fwt.py
# and player/thumbnails.Window

# finally, can make a separate object
# then have window as a property of it.
