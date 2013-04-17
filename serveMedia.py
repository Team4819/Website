import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class Image(db.Model):
    Description = db.StringProperty(multiline=True)
    Key = db.StringProperty()
    Date = db.StringProperty()
    Filename = db.StringProperty()
    
def album_key(album_name=None):
    return db.Key.from_path('album', album_name or 'default_album')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
       resource=str(urllib.unquote(resource))
       resourcelist=resource.split("/",2)
       
       images = db.GqlQuery("SELECT * "
                "FROM Image "
                "WHERE ANCESTOR IS :1 AND Date = :2 AND Filename = :3 "
                "ORDER BY Date DESC LIMIT 10",
                album_key("Images"),resourcelist[0],resourcelist[1])
       blob_info = blobstore.BlobInfo.get(images[0].Key)
       self.send_blob(blob_info)


app = webapp2.WSGIApplication([('/media/(.+)?', ServeHandler)], debug=True)

