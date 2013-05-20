import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db

class Post(db.Model):
    author = db.StringProperty()
    title = db.StringProperty(multiline=True)
    content = db.TextProperty()
    date = db.DateTimeProperty()
    pic = db.StringProperty()
    restricted = db.BooleanProperty()

def Posts_key():
    return db.Key.from_path('posts-version', 'posts-2')

def getRecentPosts():
    posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC LIMIT 10",
                        Posts_key("Posts"))
    return posts

             
    
