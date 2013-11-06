import webapp2
import datetime
import logging
from .. import auth

class Login(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        password = self.request.get('Password')
        #logging.info(firstName + " " + lastName + " " + password)
        try:
            authKey = auth.logIn(firstName, lastName, password)
            user = auth.authorize(authKey)
            self.response.set_cookie("authKey", authKey, 360000 , "/")
            self.response.set_cookie("LoginStatus", "LoggedIn", 360000 , "/")
            self.response.set_cookie("Subscribed", str(user.subscribed), 360000 , "/")
            self.response.out.write(user.firstName)
        except auth.invalidLogon:
            self.response.set_cookie("loginStatus", "InvalidLogin", 360000 , "/")
            self.response.out.write('InvalidLogin')
        
app = webapp2.WSGIApplication([('/python/login', Login)], debug=True)