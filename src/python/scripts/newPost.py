import webapp2
import logging
from .. import auth, posts, email

class newPost(webapp2.RequestHandler):
    def post(self):
        logging.info("newPost")
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser
        if(user.permissions < 2):
            return
        newpost = posts.Post(parent =posts.Posts_key())
        newpost.title = self.request.get('title')
        newpost.content = self.request.get('content')
        newpost.author = user.firstName + " " + user.lastName
        if( self.request.get('restricted') == 'true' ): newpost.restricted = True
        else: newpost.restricted = False
        newpost.tags = ["all"]
        newpost.comments = 0
        newpost.put()
        email.mailToSubscribed(newpost)
        self.response.out.write('Posted Successfully')
            
        
app = webapp2.WSGIApplication([('/python/newPost', newPost)], debug=True)