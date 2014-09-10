import webapp2
import datetime
import logging
from .. import users

class Login(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        password = self.request.get('Password')
        #logging.info(firstName + " " + lastName + " " + password)
        try:
            authKey = users.log_in(firstName, lastName, password)
            user = users.authorize(authKey)
            self.response.set_cookie("authKey", authKey, 360000 , "/")
            self.response.set_cookie("LoginStatus", "LoggedIn", 360000 , "/")
            self.response.set_cookie("Subscribed", str(user.subscribed), 360000 , "/")
            self.response.out.write(user.firstName)
        except users.invalidLogon:
            self.response.set_cookie("loginStatus", "InvalidLogin", 360000 , "/")
            self.response.out.write('InvalidLogin')
        
app = webapp2.WSGIApplication([('/python/login', Login)], debug=True)