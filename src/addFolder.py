import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class Folder(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline=True);
    date = db.DateProperty();
    thumbnail = db.StringProperty();
    
def Folder_key(folder_name=None):
    return db.Key.from_path('Folder', folder_name or 'default_folder')


class MainPage(webapp2.RequestHandler):
    def get(self, resource):
        self.response.out.write('<html><body>')
        resource=str(urllib.unquote(resource))
        path = resource.split("/")
        ancestry = ""
        for part in path:
            ancestry += "Folder:" + part + " "
        parent_key = Folder_key(ancestry)
        folder_name=resource
        
        folder = db.GqlQuery("SELECT * "
                        "FROM Folder "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC LIMIT 10",
                        parent_key)
        self.response.out.write('<div class="folder"><a href="../">Parent Folder</a></div>')
        for folder in folders:
            self.response.out.write('<div class="Folder"><a href="/%s">' % folder.name )
            self.response.out.write('<img src="%s"/>' % folder.thumbnail )
            self.response.out.write('<h3>%s</h3>' % folder.name)
            self.response.out.write('</div>\n')
            
        self.response.out.write("""
          <form action="/addPost?%s" method="post">
            <div><p>name</p><textarea name="name"></textarea></div>
            <div><p>description</p><textarea name="description" rows="3" cols="60"></textarea></div>
            <div><p>date</p><textarea name="date" rows="3" cols="60">%s</textarea></div>
            <div><input type="submit" value="Submit Post"></div>
          </form>
        </body>
      </html>"""  % (urllib.urlencode({'folder_name': folder_name}),datetime.date.isoformat(datetime.date.today())))
                
        

class createFolder(webapp2.RequestHandler):
    def post(self, resource):
        resource=str(urllib.unquote(resource))
        path = resource.split("/")
        ancestry = ""
        for part in path:
            ancestry += "Folder:" + part + " "
        parent_key = Folder_key(ancestry)
        folder_name = self.request.get('name')
        folder = Folder(parent=parent_key)
        folder.date = self.request.get("date")
        folder.name = self.request.get("name")
        folder.description = self.request.get("description")
        folder.put()
        self.redirect('/Album/' + urllib.urlencode({'folder_name' : archive_name}))
    


app = webapp2.WSGIApplication([('/Album/(.+)/addFolder?', MainPage), ('/Album/(.+)/createFolder', createFolder)], debug=True)    
