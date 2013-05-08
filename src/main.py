#!/usr/bin/env python

import webapp2
import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class Page(db.Model):
    html = db.TextProperty()
    path = db.StringProperty()
    
class Post(db.Model):
    content = db.TextProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        posts = db.GqlQuery("SELECT * "
                            "FROM Page "
                            "WHERE ANCESTOR IS :1 AND path = :2"
                            "ORDER BY Date DESC LIMIT 10",
                            
                            )
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(file(path,'rb').read())

app = webapp2.WSGIApplication([
    ('/(.+)?', MainHandler)
], debug=True)
