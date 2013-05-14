from google.appengine.ext import db

class Page(db.Model):
    template = db.TextProperty()
    path = db.StringProperty()
    query = db.StringProperty()