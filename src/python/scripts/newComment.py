import webapp2
import datetime
import logging
from .. import auth, email, posts

class newComment(webapp2.RequestHandler):
    def post(self):
        logging.info("newComment")
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        else: user = auth.publicUser

        post = posts.getPost(self.request.get('title'), self.request.get('date'))
        comment = posts.Comment(parent=post)
        comment.content = self.request.get('content')
        comment.author = user.firstName + " " + user.lastName
        comment.put()
        post.comments += 1
        post.put();
        email.mailToSubscribed(post)
        self.response.out.write('Commented Successfully')
            
        
app = webapp2.WSGIApplication([('/python/newComment', newComment)], debug=True)
