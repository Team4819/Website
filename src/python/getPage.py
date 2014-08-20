import webapp2
import urllib
import users
import groups

from django import template
from django.template import loader, Context
from pages import about, PageNotFound, UpdatesPage, MediaPage, PageBase
from scripts import subscribe

def getGenericPage(request, resource, user):
    resource=str(urllib.unquote(resource))
    try:
        temp = loader.get_template(resource.lower() + ".html")
        
    except template.TemplateDoesNotExist:
        return PageNotFound.getPage(request, resource)
        
    cont = Context({"user": user}) 
    return temp.render(cont) 

def getAdminPage(request, resource, user):
    if(user.permissions < 3):
        return getGenericPage(request, 'accessdenied', user)
    else:
        return getGenericPage(request, resource, user)
    
def getWriterPage(request, resource, user):
    if(user.permissions < 2):
        return getGenericPage(request, 'accessdenied', user)
    else:
        return getGenericPage(request, resource, user)
    
def getReaderPage(request, resource, user):
    if(user.permissions < 1):
        return getGenericPage(request, 'accessdenied', user)
    else:
        return getGenericPage(request, resource, user)
    
Pages = dict()
Pages["none"] = PageBase.PageBase(file="about.html")
Pages["updates"] =

Pages = {"none": about.getPage, "updates": UpdatesPage.getPage, "media": MediaPage.getPage, "calendar": getReaderPage}

def getPage(request, resource, user):
    split = resource.split("/")[0]
    if(split != None): split = split.lower()
    try:
        result = Pages[split](request, resource, user)
    except KeyError: 
        result = getGenericPage(request, resource, user)
    
    return result
        
class getPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            if(self.request.cookies.get("LoginStatus") == "LoggedIn"):
                user = users.authorize(self.request.cookies.get("authKey"))
            else:
                user = users.publicUser
            
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(self, resource, user))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
