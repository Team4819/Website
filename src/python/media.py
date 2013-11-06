import datetime
import urllib
import webapp2
import auth
import logging

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.api import files
from google.appengine.ext.webapp import blobstore_handlers



class File(db.Model):
    Description = db.StringProperty(multiline=True)
    Key = db.StringProperty()
    Html = db.TextProperty()
    Date = db.DateTimeProperty(auto_now_add=True)
    Name = db.StringProperty()
    Type = db.StringProperty()
    Restricted = db.BooleanProperty()
    
class Folder(db.Model):
    Description = db.StringProperty(multiline=True)
    Date = db.DateTimeProperty(auto_now_add=True)
    Name = db.StringProperty()
    Restricted = db.BooleanProperty()
    
def Media_key():
    return db.Key.from_path('media-version', 'media-2')

def getFolderKey(name):
    folderKey = db.GqlQuery("SELECT _key_ "
                            "FROM Folder "
                            "WHERE ANCESTOR IS :1 AND Name = :2 "
                            "LIMIT 1",
                            Media_key(),name)
    return folderKey[0]

def getFolder(name):
    return db.GqlQuery("SELECT * "
                       "FROM Folder "
                       "WHERE ANCESTOR IS :1 AND Name = :2 "
                       "LIMIT 1",
                       Media_key(),name)
    
def getFile(name, folder):
    return db.GqlQuery("SELECT * "
                       "FROM File "
                       "WHERE ANCESTOR IS :1 AND Name = :2 "
                       "LIMIT 1",
                       folder,name)[0]

def getFolderThumbnail(folder):
    files = db.GqlQuery("SELECT * "
                        "FROM File "
                        "WHERE ANCESTOR IS :1 AND Type = 'image' "
                        "LIMIT 1", folder)
    if(files.count(1) == 0):
        return "/static/Images/UI/folder-folder.png"
    return "/static/media/" + folder.Name + "/" + files[0].Name + "?resize=true&width=200&height=150"



def getFiles(restricted, folder):
    if(restricted):
        files = db.GqlQuery("SELECT * "
                            "FROM File "
                            "WHERE ANCESTOR IS :1 AND Restricted = False "
                            "ORDER BY Name DESC LIMIT 30",
                            folder)
    else:
        files = db.GqlQuery("SELECT * "
                            "FROM File "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY Name DESC LIMIT 30",
                            folder)
    return files

def getFolders(restricted):
    if(restricted):
        folders = db.GqlQuery("SELECT * "
                            "FROM Folder "
                            "WHERE ANCESTOR IS :1 AND Restricted = False "
                            "ORDER BY Date DESC LIMIT 10",
                            Media_key())
    else:
        folders = db.GqlQuery("SELECT * "
                            "FROM Folder "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY Date DESC LIMIT 10",
                            Media_key())
    return folders

def newFolder(restricted, name, description, date):
    folder = Folder(parent=Media_key())
    folder.Restricted = restricted
    folder.Name = name
    folder.Description = description
    folder.Date = date
    folder.put()
    
class uploadHtml(webapp2.RequestHandler):
    def post(self, resource):
        resource = str(urllib.unquote(resource))
        logging.info('resource is ' + resource)
        nfile = File(parent=getFolder(resource)[0])
        nfile.Name = self.request.get('title')
        nfile.Html = self.request.get('html')
        nfile.Type = 'html'
        if(self.request.get("restricted")== "on"): nfile.Restricted = True
        else: nfile.Restricted = False
        nfile.put()
        
class StaticHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        logging.info("static " + resource)
        resource=str(urllib.unquote(resource))
        resourcelist=resource.split("/")
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser
        try:
            fileResult = db.GqlQuery("SELECT * "
                "FROM File "
                "WHERE ANCESTOR IS :1 AND Name = :2 "
                "ORDER BY Date DESC LIMIT 10",
                getFolder(resourcelist[0])[0],resourcelist[1])[0]
            if(fileResult.Restricted and user.permissions == 0):
                logging.info("not allowed, " + str(user.permissions))
                return
            if(fileResult.Type == "image"):
                if(self.request.get("resize")=="true"):
                    img = images.Image(blob_key=fileResult.Key)
                    img.resize( width=int(self.request.get("width")), height=int(self.request.get("height")))
                    image = img.execute_transforms(output_encoding=images.PNG)
                    self.response.headers['Content-Type'] = "image/png"
                    self.response.out.write(image)
                else: self.send_blob(blobstore.BlobInfo.get(fileResult.Key))
                logging.info("done")
                return
            else:
                blob_info = blobstore.BlobInfo.get(fileResult.Key)
                self.send_blob(blob_info)
                
        except IndexError:
            return

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self, resource):
        resource=str(urllib.unquote(resource))
        logging.info(resource)
        upload_files = self.get_uploads()
        for f in upload_files:
            blob_info = f
            nfile = File(parent=getFolder(resource)[0])
            nfile.Key = "%s" % blob_info.key()
            nfile.Name = blob_info.filename
            nfile.Type = str(blob_info.content_type).split("/")[0]
            if(self.request.get("restricted")== "on"): nfile.Restricted = True
            else: nfile.Restricted = False
            nfile.Description = self.request.get("description")
            nfile.put()
        self.redirect("/Media/" + resource)
        

app = webapp2.WSGIApplication([('/static/media/(.+)?', StaticHandler),('/upload/media/(.+)?', UploadHandler), ('/upload/html/(.+)?', uploadHtml)], debug=True)