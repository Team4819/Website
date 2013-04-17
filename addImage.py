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
    Filename = db.StringProperty();

def album_key(album_name=None):
    return db.Key.from_path('album', album_name or 'default_album')

class addImage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload.py')
        self.response.out.write('<html><body>')
        images = db.GqlQuery("SELECT * "
                        "FROM Image "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY Date DESC LIMIT 10",
                        album_key("Images"))
        for image in images:
            self.response.out.write('<img src="/media/%s"/>' % (image.Date + "/" + image.Filename))
        
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br>
                                <p>Date</p><textarea name="Date" rows="1" cols="10">""" + datetime.date.isoformat() + """</textarea><div><p>Filename</p><textarea name="Filename" rows="1" cols="20"></textarea><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        image = Image(parent=album_key("Images"))
        image.Key = "%s" % blob_info.key()
        image.Date = self.request.get('Date')
        image.Filename = self.request.get('Filename')
        image.put()
        self.redirect('/addImage.py')


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource=str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        
app = webapp2.WSGIApplication([('/addImage.py', addImage), ('/upload.py', UploadHandler), ('/serve/a', ServeHandler)], debug=True)
    
