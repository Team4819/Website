from django.template import Context,loader
from .. import posts
import AccessDenied, PageNotFound, logging
import urllib
from datetime import datetime,tzinfo,timedelta,time

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
        return self.name

GMT = Zone(0,False,'GMT')
EST = Zone(-5,False,'EST')

def getPage(request, resource, user):
    split = str(resource).split('/')
    resource=str(urllib.unquote(resource))
    if(len(split) == 1):
        temp = loader.get_template("updates.html")
        date = request.request.get("getBefore");
        if(date == ""):date = datetime.now();
        else: date = time.strptime(date, "%Y-%m-%d")
        updates =  posts.getPostsBefore(date.date ,(user.permissions < 1))
        if(updates.count() > 0):
#            result = []
#            for update in updates:
#                result.append({"author": update.author, "title": update.title, "content": update.content, "date": update.date.astimezone(EST), "comments": update.comments})
            cont = Context({"updates": updates, "user": user})
        else:
            cont = Context({"user": user})
        result = temp.render(cont).encode('utf-8')
        return result
    
    elif(split[1] == "New"):
        if(user.permissions >= 2):
            temp = loader.get_template("newpost.html")
            cont = Context({"user": user})
            result = temp.render(cont)
            return result
        else:
            return AccessDenied.getPage(resource, user)
    

    elif(split[1] != "New"):
        

            
        if(split[1] == "Page"):
            temp = loader.get_template("updates.html")
            try:
                page = split[2]
                print("page");
                updates = posts.getPostsOnPage(page, user.permissions < 1)
                if(updates.count() > 0):
                    cont = Context({"updates": updates, "user": user})
                else:
                    cont = Context({"user": user})
                result = temp.render(cont).encode('utf-8')
                return result
            except IndexError:
                return PageNotFound.getPage(resource)  
            
        elif(len(split) == 3):
            temp = loader.get_template("post.html");
            try:
                title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                logging.info(title)
                post = posts.getPost(title, date);
                if(user.permissions < 1 & post.restricted): return AccessDenied.getPage(resource, user)
                comments = posts.getComments(post)
                if(comments.count() == 0): comments = None
                cont = Context({"post": post, "comments": comments, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(resource)
            
        elif(split[3] == "Edit"):
            if(user.permissions < 2): return AccessDenied.getPage(resource, user)
            try:
                title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                post = posts.getPost(title, date);
                if(post.author != user.firstName+" "+user.lastName and user.permissions < 3):
                    return AccessDenied.getPage(resource, user)
                temp = loader.get_template("editpost.html")
                cont = Context({"post": post, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(resource)
            
        elif(split[3] == "Delete"):
            if(user.permissions < 2): return AccessDenied.getPage(resource, user)
            try:
                title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                post = posts.getPost(title, date);
                if(post.author != user.firstName+" "+user.lastName and user.permissions < 3):
                    return AccessDenied.getPage(resource, user)
                temp = loader.get_template("deletepost.html")
                cont = Context({"post": post, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(resource)
        

