import webapp2
import urllib
import auth

from django import template
from django.template import loader, Context
from pages import about, PageNotFound

def getGenericPage(resource, user):
    try:
        temp = loader.get_template(resource + ".html")
        
    except template.TemplateDoesNotExist:
        return PageNotFound.getPage(resource)
        
    cont = Context({"user": user})
    return temp.render(cont) 

        
    
Pages = { "None": about.getPage}

def getPage(resource, user):
    resource=str(urllib.unquote(resource))
    split=resource.split("/")[0]
    try:
        result = Pages[split](resource, user)
    except KeyError: 
        result = getGenericPage(resource, user)
    
    return result
        
class getPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            resource=str(urllib.unquote(resource))
            if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
                user = auth.authorize(self.request.cookies.get("authKey"))
            else: user = None
            
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(resource, user))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
