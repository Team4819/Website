import logging
import webapp2
import getPage
import auth

from django.template import Context, loader




class MainHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(resource)
        
        temp = loader.get_template("index.html")
        
        logging.info(self.request.cookies.get("LoginStatus"))
        
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            
            logging.info(self.request.cookies.get("authKey"))
            
            user = auth.authorize(self.request.cookies.get("authKey"))
            content = getPage.getPage(resource, user)
            if (user): 
                cont = Context({"content": content, "Username": user.firstName})
            else:
                cont = Context({"content": content})
        else:
            user = auth.publicUser
            content = getPage.getPage(resource, user)
            cont = Context({"content": content})
            
            
        result = temp.render(cont)
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(result)

app = webapp2.WSGIApplication([
    ('/(.+)?', MainHandler)
], debug=True) 
