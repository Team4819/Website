import webapp2
from .. import auth

class Subscribe(webapp2.RequestHandler):
    def get(self):
        user = auth.publicUser
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        if(user.permissions == 0):
            auth.createPublicSubscribed(self.request.get('email'))
        else:
            emails = auth.findPublicEmail(user.email)
            if(emails.count() != 0):
                emails[0].delete()
            user.subscribed = True;
            user.put()

class Unsubscribe(webapp2.RequestHandler):
    def get(self):
        user = auth.publicUser
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))

	email = self.request.get("email");
	if(email != ""):
	    emails = auth.findPublicEmail(email)
            if(emails.count() != 0):
                emails[0].delete()
	    else:
                emails = auth.lookupEmail(email)
                if(emails.count() != 0):
                    user = emails[0];
                    user.subscribed = False;
                    user.put();
        elif(user.permissions != 0):
            user.subscribed = False;
            user.put();

	self.response.out.write('You have been unsubscribed.');
        
app = webapp2.WSGIApplication([('/python/subscribe', Subscribe),('/python/unsubscribe', Unsubscribe)], debug=True)
