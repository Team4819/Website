import webapp2
import urllib
import auth

from django import template
from django.template import loader, Context
from pages import about, PageNotFound, teamUpdates

def getGenericPage(resource, user):
    try:
        temp = loader.get_template(resource + ".html")
        
    except template.TemplateDoesNotExist:
        return PageNotFound.getPage(resource)
        
    cont = Context({"user": user}) 
    return temp.render(cont) 

def getAdminPage(resource, user):
    if(user.permissions < 3):
        return getGenericPage('accessDenied', user)
    else:
        return getGenericPage(resource, user)
    
def getWriterPage(resource, user):
    if(user.permissions < 2):
        return getGenericPage('accessDenied', user)
    else:
        return getGenericPage(resource, user)
    
def getReaderPage(resource, user):
    if(user.permissions < 1):
        return getGenericPage('accessDenied', user)
    else:
        return getGenericPage(resource, user)
    

            
Pages = { "None": about.getPage, "Updates": teamUpdates.getPage}

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
            else: user = auth.publicUser
            
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(resource, user))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
