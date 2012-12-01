#!/usr/bin/env python
#
"""
cd /c/moments-web 
/c/downloads/python/google_appengine/dev_appserver.py --port 8081 application/

firefox -browser
firefox http://localhost:8081/

"""
import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

import re

import os
from google.appengine.ext.webapp import template

from moments.timestamp import Timestamp

class Moment(db.Model):
  author = db.UserProperty()
  content = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  tags = db.ListProperty(db.Category)

  def render(self):
    response = '<a href="/edit/%s">*</a>' % self.key().id()
    if self.date:
      response += "%4d.%02d.%02d %02d:%02d:%02d " % (self.date.year, self.date.month, self.date.day, self.date.hour, self.date.minute, self.date.second)
    else:
      response += " "
    response += " ".join(self.tags)
    response += "<br>"
    #response += "%s<br>" % str(self.date)
    temp = cgi.escape(self.content)
    response += temp.replace('\n', '<br>\n')
    return response

class User(db.Model):
    """
    local user data
    """
    name = db.StringProperty()

    google_user = db.UserProperty(auto_current_user_add=True)

    #should be the number of hours to offset (+ or -)
    timezone = db.IntegerProperty()

    #if we should scan entries for starting *
    #indicating multiple entries
    parse_data = db.BooleanProperty(default=False)
    

def get_moment(compact):
    user = users.get_current_user()

    ts = Timestamp(compact=compact)
    ts_max = ts.future(seconds=1)
    if user:
      moments = Moment.all()
      moments.filter("author =", users.get_current_user())
      moments.filter("date >=", ts.datetime)
      moments.filter("date <=", ts_max.datetime)
      moments.order('-date')
      return moments
    else:
      return None

def make_footer(uri):
  user = users.get_current_user()

  if user:
      url = users.create_logout_url(uri)
      url_linktext = 'Logout'
  else:
      url = users.create_login_url(uri)
      url_linktext = 'Login'

  footer = '<a href="%s">%s</a>' % (url, url_linktext)
  return footer

class AboutPage(webapp.RequestHandler):
  def get(self):
    body = """<p>This site provides an easy way to keep track of thoughts and ideas.  It is based on the concept of moments. Moments are defined by three simple elements: time, tags, and a description.  Time is added automatically, and tags are optional, so all you really need is the description.  What is going on?  Write it down.  Let it go.  Find it later when you need it again.</p>

    <p>This simple format makes it easy to backup your thoughts and ideas in a plain text format.  Plain text allows working offline with moments.  There are even <a href="http://bitbucket.org/cbrandt/moments/">libraries</a> available to help you work with your moments in new and custom ways, if you desire.  This also allows a high level of <a href="/privacy">privacy</a> when needed.</p>

    <p>
    
    """

    #print footer
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

class PrivacyPage(webapp.RequestHandler):
  def get(self):
    body = """<p>

    """
    #print footer
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

def get_local_user():
  google_user = users.get_current_user()
  if google_user:
    local_user_q = db.GqlQuery("SELECT * "
                               "FROM User "
                               "WHERE google_user = :1",
                               google_user)
    if local_user_q.count():
      #self.response.out.write('Existing Local User found<br>')
      local_user = local_user_q[0]
    else:
      #self.response.out.write('Creating new Local User<br>')
      local_user = User(name=google_user.nickname())
      local_user.put()
  else:
    local_user = None

  return local_user

  

class MainPage(webapp.RequestHandler):
  def get(self):

    body = ''
    
    template_values = {'date':'',
                       'tags':'',
                       'content':'',
                       'key':'',
                       'action':'/create',
                       'delete':'',
                       'complete':'',
                       }
    path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
    body += template.render(path, template_values)

    local_user = get_local_user()

    user = users.get_current_user()

    if user:
      moments = Moment.all()
      moments.filter("author =", users.get_current_user())
      moments.order('-date')

      body += '<div class="content">'
      for moment in moments:
        body += '<p>%s</p><br>' % moment.render()

      body += '</div>'

    #print footer
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

def process_tags(tag_string):
  tags = []
  if tag_string:
    tag_strings = tag_string.split()
    for t in tag_strings:
      tags.append(db.Category(t))
  return tags

def process_date(date_string):
  date = None
  if date_string:
    if date_string == "now":
      #default is now
      pass
    else:
      #doesn't look like dateutil is available here:
      #from dateutil.parser import parse
      #date = parse(date_string)
      
      timestamp = Timestamp(date_string)
      date = timestamp.datetime
      #date = from_text(date_string)
  return date
    
class CreateMoment(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      moment = Moment()

      moment.author = users.get_current_user()

      tag_response = self.request.get('tags')
      moment.tags = process_tags(tag_response)

      date_response = self.request.get('date')
      date = process_date(date_response)
      if date:
        moment.date = date
      
      moment.content = self.request.get('content')
      moment.put()
      self.redirect('/')

class UpdateMoment(webapp.RequestHandler):
  def post(self, item_id):
    #id_response = self.request.get('id')
    moment = Moment.get_by_id(int(item_id))
    if moment.author == users.get_current_user():
      #body = moments.render()
      #commit the changes:
      #for date, could check if anything has changed
      #by comparing year, month, day, hour, minutes, seconds
      tag_response = self.request.get('tags')
      moment.tags = process_tags(tag_response)

      date_response = self.request.get('date')
      date = process_date(date_response)
      if date:
        moment.date = date

      moment.content = self.request.get('content')
      moment.put()
      body = "Changes added.<br>"
      body += moment.render()
      body += "<a href='/'>Home</a><br>"

    else:
      body = "You do not have permissions to access that entry"
      body += "<a href='/'>Home</a><br>"
      
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))
    
class EditMoment(webapp.RequestHandler):
  def get(self, item_id):
    body = ''

    #this will search based on the timestamp provided
    #could return more than one result though
    #id is a better choice for edit
    #def get(self, compact):
    #lookup moment:
    #compact,
    #ts = Timestamp(compact=compact)
    #moment_q = get_moment(compact)
    #if moment_q.count():
    #  current = moment_q[0]
    #else:
    #  body += "No Moment found with time: %s<br>" % (ts.datetime)
    #  #body += str(ts.datetime) + '<br>'

    current = Moment.get_by_id(int(item_id))

    if current.author == users.get_current_user():
      #debug options
      #body += current.render()
      #body += '<br>'
      #body += str(moment_q[0].key()) + '<br>'
      #body += str(moment_q[0].key().id()) + '<br>'
      #body += str(moment_q[0].key().name()) + '<br>'
      ts = Timestamp(current.date)
      template_values = {'date':str(ts),
                         'tags':' '.join(current.tags),
                         'content':current.content, 
                         'action':'/update/%s' % current.key().id(),
                         'complete':'<a href="/complete/%s">complete</a> |' % current.key().id(),
                         'delete':'<a href="/delete/%s">delete</a>' % current.key().id(),
                         }
      path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
      body += template.render(path, template_values)

    else:
      body += "You do not have permissions to access that entry"
        

    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

class CompleteMoment(webapp.RequestHandler):
  def get(self, item_id):
    body = ''
    current = Moment.get_by_id(int(item_id))
    if current.author != users.get_current_user():
      body += "You do not have permissions to access that entry"
    else:
      body += "Marking entry complete:<br>"
      ts = Timestamp(current.date)
      content = "created [%s]\n%s" % (ts, current.content)
      current.content = content
      # add complete to tags
      current.tags.append(db.Category("complete"))
      # update time to now
      now = Timestamp()
      current.date = now.datetime
      current.put()
      body += current.render()

    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

class DeleteMoment(webapp.RequestHandler):
  def get(self, item_id):
    body = ''
    body += "<a href='/'>Home</a><br>"
    current = Moment.get_by_id(int(item_id))
    if current.author != users.get_current_user():
      body += "You do not have permissions to access that entry"
    else:
      body += "Deleted entry:<br>"
      body += current.render()
      current.delete()
      
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

class ClearMindAsk(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      moments = Moment.all()
      moments.filter("author =", users.get_current_user())
      moments.order('-date')
      count = moments.count()

      
      body = ''
      if count > 1:
        body += "<h4>Are you *sure* you want to remove all %s entries?</h4>\n" % moments.count()
      elif count == 1:
        body += "<h4>Are you *sure* you want to remove your entry?</h4>\n"
        
      body += "<h5>This action cannot be undone!</h5>\n"
      body += """<div><span><a href="/"><h2>No!</h2></a></span><br><br><br><br><br><span><a href="/clear/mind">Yes, I'm sure.</a></span></div>"""
      #print body

      if count < 1:
        body = "<h4>You don't have any entries.  <br>Your mind is clear.  <br>Be calm.  <br>Smile.  <br>Breathe deeply.</h4>"
        body += '<p>&nbsp;</p>'
        body += """<div><span><a href="/">Home</a></span></div>"""

    else:
      body = "You must be logged in"
      
    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

class ClearMind(webapp.RequestHandler):
  def get(self):
    count = 0
    deleted = ""
    
    user = users.get_current_user()
    if user:
      moments = Moment.all()
      moments.filter("author =", users.get_current_user())
      moments.order('-date')

      for moment in moments:
        deleted += '<p>%s</p><br>' % moment.render()
        moment.delete()
        count += 1

    body = ''
    body += "<h1>Clear Mind</h1>"
    body += "<p>clear as a mountain stream</p>"
    body += '<p><a href="/">Home</a></p>'
    body += '<p>&nbsp;</p>'
    body += '<p>&nbsp;</p>'
    body += '<p>&nbsp;</p>'
    body += '<p>&nbsp;</p>'
    body += '<h3>Deleted %s moments:</h3>' % count
    body += "<p>(copy them now to keep them. this is the last time you'll see them here.)</p>"
    body += '<p>&nbsp;</p>'
    body += deleted

    template_values = {
        'body': body,
        'footer': make_footer(self.request.uri),
        'title': "now",
        }

    path = os.path.join(os.path.dirname(__file__), 'templates/site.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/about', AboutPage),
  ('/create', CreateMoment),
  ('/update/(.*)', UpdateMoment),
  ('/edit/(.*)', EditMoment),
  ('/complete/(.*)', CompleteMoment),
  ('/delete/(.*)', DeleteMoment),
  ('/clear', ClearMindAsk),
  ('/clear/mind', ClearMind),
  ]  
, debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

## def from_text(text_time):
##     """
##     take a string of the format:
##     YYYY.MM.DD HH:MM
##     return a python datetime object
##     """
##     #removed leading char if needed
##     if re.match("[-\*]", text_time):
##         text_time = text_time[1:]

##     if re.search("-", text_time):
##         format = "%Y-%m-%d %H:%M:%S"
##     elif re.search("/", text_time):
##         format = "%Y/%m/%d %H:%M:%S"
##     else:
##         format = "%Y.%m.%d %H:%M:%S"

##     if len(text_time) > 19:
##         #2007-05-03T15:56:05-04:00
##         #
##         #but what about 2009-07-17 07:14:17.003537?
##         #truncating for now
##         #TODO: accept micro seconds
##         text_time = text_time[:19]
##         time = datetime(*(strptime(text_time, "%Y-%m-%dT%H:%M:%S")[0:6]))

##     elif len(text_time) == 19:
##         # this only works with python 2.5
##         # (current default is 2.4.4 for zope)
##         #return datetime.strptime(text_time, self.text_time_format)
##         # e.g. "%Y.%m.%d %H:%M:%S"
##         time = datetime(*(strptime(text_time, format)[0:6]))
##     elif len(text_time) == 16:
##         # e.g. "%Y.%m.%d %H:%M"
##         time = datetime(*(strptime(text_time, format[:14])[0:6]))
##     elif len(text_time) == 10:
##         # e.g. "%Y.%m.%d"
##         time = datetime(*(strptime(text_time, format[:8])[0:6]))
##     else:
##         #some other format
##         time = None

##     return time
