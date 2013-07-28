import webapp2
import datetime
import logging
from .. import auth
from .. import posts

class editPost(webapp2.RequestHandler):
    def post(self):
        logging.info("editPost")
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser
        if(user.permissions < 2):
            return
        post = posts.getPost(self.request.get('oldTitle'))
        post.title = self.request.get('title')
        post.content = self.request.get('content')
        post.author = user.firstName + " " + user.lastName
        if( self.request.get('restricted') == 'true' ): post.restricted = True
        else: post.restricted = False
        post.tags = ["all"]
        post.put()
        self.response.out.write('Edited Successfully')
        
class deletePost(webapp2.RequestHandler):
    def post(self):
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser
        post = posts.getPost(self.request.get('title'))
        if( post.author != user.firstName + " " + user.lastName and user.permissions < 3): return
        post.delete()
        self.response.out.write("Deleted Successfully")
        
            
        
app = webapp2.WSGIApplication([('/python/editPost', editPost),('/python/deletePost', deletePost)], debug=True)