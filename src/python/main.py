
import webapp2
import urllib
import getPage

from django.template import Context, loader




class MainHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(resource)
        content = getPage.getPage(resource)
        temp = loader.get_template("index.html")
        cont = Context({"content": content})
        result = temp.render(cont)
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(result)

app = webapp2.WSGIApplication([
    ('(.+)?', MainHandler)
], debug=True)
