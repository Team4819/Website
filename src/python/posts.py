import cgi
import datetime, time
import urllib
import webapp2
import logging
import config

from google.appengine.ext import db

class Post(db.Model):
    author = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    restricted = db.BooleanProperty()
    comments = db.IntegerProperty()

class Comment(db.Model):
    author = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def Posts_key():
    return db.Key.from_path('posts-version', 'posts-2')



def getPostsAfter(date, restricted=True, tag="all"):
    print(date.isoformat() );
    date += datetime.timedelta(hours=1);
    print(date.isoformat() );
    if (restricted):
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND restricted = False AND tags = :2 AND date > :3 "
                        "ORDER BY date ASC LIMIT " + str(config.PostsPerPage + 1),
                        Posts_key(), tag, date)
    else:
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND tags = :2 AND date > :3 "
                        "ORDER BY date ASC LIMIT " + str(config.PostsPerPage +1),
                        Posts_key(), tag, date)
    result = []
    #print(posts.count());
    for post in posts:
        result.insert(0,post);
    logging.info(str(len(result)) + " posts returned")
    return result;

def getPostsBefore(date, restricted=True, tag="all"):
    print(date.isoformat() );
    if (restricted):
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND restricted = False AND tags = :2 AND date < :3 "
                        "ORDER BY date DESC LIMIT " + str(config.PostsPerPage + 1),
                        Posts_key(), tag, date)
    else:
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND tags = :2 AND date < :3 "
                        "ORDER BY date DESC LIMIT " + str(config.PostsPerPage + 1),
                        Posts_key(), tag, date)
    result = []
    for post in posts:
        result.append(post);
        
    logging.info(str(len(result)) + " posts returned")
    return result
    
    
def getRecentPosts(restricted=True, tag="all" ):
    if (restricted):
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND restricted = False AND tags = :2 "
                        "ORDER BY date DESC LIMIT :3",
                        Posts_key(), tag, str(config.PostsPerPage))
    else:
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND tags = :2 "
                        "ORDER BY date DESC LIMIT :3",
                        Posts_key(), tag, str(config.PostsPerPage))
    logging.info(str(posts.count()) + " posts returned")
    return posts

def getPost(title, date):
    results = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 AND title = :2 ",
                        Posts_key(), title)
    print(date);
    for result in results:
        compdate = result.date.strftime("%Y-%m-%d");
        print(compdate);
        if(compdate == date):
            return result;
    raise(IndexError);
    
def getComments(post):
    return db.GqlQuery("SELECT * "
                       "FROM Comment "
                       "WHERE ANCESTOR IS :1 "
                       "ORDER BY date DESC LIMIT 20",
                       post)
    
