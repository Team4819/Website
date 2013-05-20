import webapp2
from .. import auth

class CreateUser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('Username')
        password = self.request.get('Password')
        permissions = self.request.get('Permissions')
        auth.createUser(username, password, permissions)
        
app = webapp2.WSGIApplication([('/python/CreateUser', CreateUser)], debug=True)