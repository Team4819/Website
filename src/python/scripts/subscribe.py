import webapp2
from .. import auth

class Subscribe(webapp2.RequestHandler):
    def get(self):
        user = auth.publicUser
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        if(user.permissions == 0):
            auth.createPublicSubscribed(self.request.get('email'))
            self.response.set_cookie("Subscribed", "True", 36000 , "/")
        else:
            emails = auth.findPublicEmail(user.email)
            if(emails.count() != 0):
                emails[0].delete()
            user.subscribed = True;
            user.put()
            
        
app = webapp2.WSGIApplication([('/python/subscribe', Subscribe)], debug=True)