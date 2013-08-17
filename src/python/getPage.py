import webapp2
import urllib
import auth

from django import template
from django.template import loader, Context
from pages import about, PageNotFound, teamUpdates, Media

def getGenericPage(resource, user):
    resource=str(urllib.unquote(resource))
    try:
        temp = loader.get_template(resource.lower() + ".html")
        
    except template.TemplateDoesNotExist:
        return PageNotFound.getPage(resource)
        
    cont = Context({"user": user}) 
    return temp.render(cont) 

def getAdminPage(resource, user):
    if(user.permissions < 3):
        return getGenericPage('accessdenied', user)
    else:
        return getGenericPage(resource, user)
    
def getWriterPage(resource, user):
    if(user.permissions < 2):
        return getGenericPage('accessdenied', user)
    else:
        return getGenericPage(resource, user)
    
def getReaderPage(resource, user):
    if(user.permissions < 1):
        return getGenericPage('accessdenied', user)
    else:
        return getGenericPage(resource, user)
    

            
Pages = { "none": about.getPage, "updates": teamUpdates.getPage, "media": Media.getPage, "calendar": getReaderPage}

def getPage(resource, user):
    split=resource.split("/")[0]
    if(split != None): split = split.lower()
    try:
        result = Pages[split](resource, user)
    except KeyError: 
        result = getGenericPage(resource, user)
    
    return result
        
class getPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
                user = auth.authorize(self.request.cookies.get("authKey"))
            else: user = auth.publicUser
            
            if(user.permissions == 0 and self.request.cookies.get("Subscribed") == "True"):
                user.subscribed = True
            
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(resource, user))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
