import webapp2

from google.appengine.api import urlfetch

class MainHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        content = urlfetch.fetch('http://' + self.request.host + '/Content' + url)
        self.response.out.write('$(fillContent(' + content + '))')

app = webapp2.WSGIApplication([
    ('/Content/getContent.py', MainHandler)
], debug=True)

