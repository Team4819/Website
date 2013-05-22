import cgi
import datetime
import urllib
import webapp2
import logging

from google.appengine.ext import db

class Post(db.Model):
    author = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    restricted = db.BooleanProperty()

class Comment(db.Model):
    author = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def Posts_key():
    return db.Key.from_path('posts-version', 'posts-2')

def getPostsAfter(date, restricted=True, tag="all"):
    posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND date > :2 AND restricted = :3 AND tags = :4 "
                        "ORDER BY date DESC LIMIT 10",
                        Posts_key(), date, restricted, tag)
    return posts

def getRecentPosts(restricted=True, tag="all" ):
    if (restricted):
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND restricted = False AND tags = :2 "
                        "ORDER BY date DESC LIMIT 10",
                        Posts_key(), tag)
    else:
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND tags = :2 "
                        "ORDER BY date DESC LIMIT 10",
                        Posts_key(), tag)
    logging.info(str(posts.count()) + " posts returned")
    return posts

def getPost(title):
    return db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND title = :2 "
                        "LIMIT 1",
                        Posts_key(), title)[0]
    
def getComments(post):
    return db.GqlQuery("SELECT * "
                       "FROM Comment "
                       "WHERE ANCESTOR IS :1 "
                       "ORDER BY date DESC LIMIT 20",
                       post)
    
