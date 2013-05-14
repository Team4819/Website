import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users



def archive_key(archive_name=None):
    return db.Key.from_path('Archive', archive_name or 'default_archive')

class getPosts(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC LIMIT 10",
                        archive_key("Posts"))
        first = True;
        for post in posts:
            if(first==False): self.response.out.write("<hr/>")
            first=False
            self.response.out.write("<div class=\"post\">")
            self.response.out.write('<h3>%s</h3>' % post.title)
            self.response.out.write("<div class=\"Content\">%s</div>" % post.content)
            if post.author != '':
                self.response.out.write("<div class=\"Author\"><b>posted by %s</b></div>" % post.author)
            else:
                self.response.out.write("<p class=\"Author\"><b>posted by Anonymous</b></p>")
            self.response.out.write("<p class=\"Date\">%s</p>" % post.date)
            self.response.out.write("</div>")
            
class getMiniPosts(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/javascript"
        self.response.out.write("$('#Updates').append(\" ")
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC LIMIT 10",
                        archive_key("Posts"))
        for post in posts:
            self.response.out.write("<div class='post'>")
            self.response.out.write("<h3>%s</h3>" % post.title)
            self.response.out.write("<img src='%s'/>" % post.pic)
            self.response.out.write("<div class='shortContent'>%s</div>" % post.shortContent)
            if post.author != '':
                self.response.out.write("<div class='Author'><b>posted by %s</b></div>" % post.author)
            else:
                self.response.out.write("<p class='Author'><b>posted by Anonymous</b></p>")
            self.response.out.write("<p class='Date'>%s</p>" % post.date)
            self.response.out.write("</div>")
             
app = webapp2.WSGIApplication([('/getPosts.py', getPosts),('/getMiniPosts.js', getMiniPosts)], debug=True)
    
