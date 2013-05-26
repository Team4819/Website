import webapp2
import datetime
import logging
from .. import auth
from .. import media

class newFolder(webapp2.RequestHandler):
    def post(self):
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser
        if(user.permissions < 2): return
        if(self.request.get("restricted") == "true"): restricted = True
        else: restricted = False
        name = self.request.get("name")
        description = self.request.get("description")
        media.newFolder(restricted, name, description)
        
app = webapp2.WSGIApplication([('/python/newFolder', newFolder)], debug=True)
 
        