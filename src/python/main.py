import webapp2
import getPage
import auth

from django.template import Context, loader




class MainHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(resource)
        
        temp = loader.get_template("index.html")
        user = auth.publicUser
        
        if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
            user = auth.authorize(self.request.cookies.get("authKey"))
        if( user.permissions == 0 and self.request.cookies.get("Subscribed") == "True"):
            user.subscribed = True
        content = getPage.getPage(self, resource, user)
        cont = Context({"content": content, "user": user})            
        result = temp.render(cont)
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(result)

app = webapp2.WSGIApplication([
    ('/(.+)?', MainHandler)
], debug=True) 
