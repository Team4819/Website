import webapp2
import urllib

from django import template
from django.template import loader, Context
from pages import about, PageNotFound

def getGenericPage(resource):
    try:
        temp = loader.get_template(resource + ".html")
        
    except template.TemplateDoesNotExist:
        return PageNotFound.getPage(resource)
        
    cont = Context({})
    return temp.render(cont) 

        
    
Pages = { "None": about.getPage, "About": getGenericPage, "Album": getGenericPage, "Robots": getGenericPage, "News": getGenericPage, "Awards": getGenericPage, "Sponsors": getGenericPage}

def getPage(resource):
    resource=str(urllib.unquote(resource))
    split=resource.split("/")[0]
    try:
        result = Pages[split](resource)
    except KeyError: 
        result = PageNotFound.getPage(resource)
    
    return result
        
class getPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            resource=str(urllib.unquote(resource))
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(resource))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
