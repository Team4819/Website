import webapp2
import urllib

from django.template import loader, Context
from pages import about

def getGenericPage(resource):
        temp = loader.get_template(resource + ".html")
        cont = Context({})
        return temp.render(cont) 
    
Pages = {"About": about.getPage, "Album": getGenericPage, "Robots": getGenericPage, "News": getGenericPage, "Awards": getGenericPage, "Sponsors": getGenericPage}

def getPage(resource):
    resource = str(resource)
    part=resource.split("/",2)[0]
    if(part == ""): part = "About"
    result = Pages[part](resource)
    return result
        
class getPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            resource=str(urllib.unquote(resource))
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(getPage(resource))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', getPageHandler)], debug=True)
