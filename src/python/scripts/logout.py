import webapp2
import datetime
import logging
from .. import auth

class Logout(webapp2.RequestHandler):
    def get(self):
        self.response.set_cookie("LoginStatus", "LoggedOut", 36000 , "/")
        self.response.set_cookie("authKey", "blank", 36000 , "/")
        
app = webapp2.WSGIApplication([('/python/logout', Logout)], debug=True)