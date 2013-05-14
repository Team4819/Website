from google.appengine.ext import db

def site_key():
    return db.Key.from_path('Site',"Team4819")