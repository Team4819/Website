import webapp2
import datetime
import logging
from .. import auth

class Login(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('Username')
        password = self.request.get('Password')
        logging.info(username + " " + password)
        try:
            authKey = auth.logIn(username, password)
            self.response.set_cookie("authKey", authKey, 36000 , "/")
            self.response.set_cookie("LoginStatus", "LoggedIn", 36000 , "/")
            self.response.out.write('LoginSuccessfull')
        except auth.invalidLogon:
            self.response.set_cookie("loginStatus", "InvalidLogin", 36000 , "/")
            self.response.out.write('InvalidLogin')
        
app = webapp2.WSGIApplication([('/python/login', Login)], debug=True)