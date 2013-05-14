from google.appengine.ext import db

class Post(db.Model):
    author = db.StringProperty()
    title = db.StringProperty(multiline=True)
    content = db.TextProperty()
    date = db.DateTimeProperty()
    pic = db.StringProperty()