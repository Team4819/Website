import webapp2
from .. import users

class CreateUser(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        password = self.request.get('Password')
        email = self.request.get('Email')
        number = self.request.get('Number')
        users.create_user(firstName, lastName, email, number, password)
        authKey = users.log_in(firstName, lastName, password)
        user = users.authorize(authKey)
        self.response.set_cookie("authKey", authKey, 36000 , "/")
        self.response.set_cookie("LoginStatus", "LoggedIn", 36000 , "/")
        self.response.set_cookie("Subscribed", str(user.subscribed), 36000 , "/")
        self.response.out.write(user.firstName)
        
app = webapp2.WSGIApplication([('/python/CreateUser', CreateUser)], debug=True)