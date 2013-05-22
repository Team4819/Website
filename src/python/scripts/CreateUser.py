import webapp2
from .. import auth

class CreateUser(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        password = self.request.get('Password')
        permissions = self.request.get('Permissions')
        auth.createUser(firstName, lastName, password, permissions)
        
app = webapp2.WSGIApplication([('/python/CreateUser', CreateUser)], debug=True)