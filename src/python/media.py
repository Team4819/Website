import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class File(db.Model):
    Description = db.StringProperty(multiline=True)
    Key = db.StringProperty()
    Date = db.DateTimeProperty()
    Name = db.StringProperty()
    
class Folder(db.Model):
    Description = db.StringProperty(multiline=True)
    Date = db.DateTimeProperty()
    Name = db.StringProperty()
    
def Media_key():
    return db.Key.from_path('media-version', 'media-0.2')

def getFolderKey(name):
    folderKey = db.GqlQuery("SELECT _key_"
                            "FROM Folder"
                            "WHERE ANCESTOR IS :1  Name = :2"
                            "LIMIT 10",
                            Media_key(),name)
    return folderKey[0]

class StaticHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource=str(urllib.unquote(resource))
        resourcelist=resource.split("/",2)
        images = db.GqlQuery("SELECT * "
                "FROM Image "
                "WHERE ANCESTOR IS :1 AND Name = :2 "
                "ORDER BY Date DESC LIMIT 10",
                getFolderKey(resourcelist[0]),resourcelist[1])
        blob_info = blobstore.BlobInfo.get(images[0].Key)
        self.send_blob(blob_info)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self, resource):
        resource=str(urllib.unquote(resource))
        resourceList=resource.split("/",2)
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        nfile = File(parent=getFolderKey(resourceList[0]))
        nfile.Key = "%s" % blob_info.key()
        nfile.Date = datetime.datetime.strptime(self.request.get('Date'), "%m-%d-%y")
        nfile.Name = resourceList[1]
        nfile.put()

app = webapp2.WSGIApplication([('/static/media/(.+)?', StaticHandler),('/upload/media/(.+)?', UploadHandler)], debug=True)