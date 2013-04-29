import webapp2

from google.appengine.api import urlfetch

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = urlfetch.fetch('http://firstteam4819.appspot.com' +'/Content/Sidebar.html')
        self.response.write('''fillSidebar(' ''' + content.content + ''' ')''')

app = webapp2.WSGIApplication([
    ('/Content/getSidebar.py', MainHandler)
], debug=True)
