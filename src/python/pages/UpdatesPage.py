from django.template import Context,loader
from .. import posts, config, email
import AccessDenied, PageNotFound, logging
import urllib
from datetime import datetime,tzinfo,timedelta,time
from PageBase import PageBase
from PageHubBase import PageHubBase

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

class UpdatesPage(PageHubBase):
    def __init__(self):
        self.spokes["none"] = MainUpdatesPage()
        self.spokes["new"] = NewUpdatePage()
        self.defaultPage = PostPage()
        super(self).__init__()


class MainUpdatesPage(PageBase):
    def getPage(request, resource, user):
        temp = loader.get_template("updates.html")

        before = request.request.get("getBefore");
        after = request.request.get("getAfter");

        if(before != ""):
            updates = posts.getPostsBefore(datetime.strptime(before, "%Y-%m-%d-%H") ,(user.permissions < 1))
        elif(after != ""):
            updates = posts.getPostsAfter(datetime.strptime(after, "%Y-%m-%d-%H") ,(user.permissions < 1))
        else:
            updates = posts.getPostsBefore(datetime.now() ,(user.permissions < 1))

        if(len(updates) > 0):
            nextPage = None
            prevPage = None

            if(after != ""):
                nextPage = updates[len(updates) - 1].date.strftime("%Y-%m-%d-%H");
                if(len(updates) == config.PostsPerPage + 1):
                    prevPage = updates[1].date.strftime("%Y-%m-%d-%H");
                    updates.pop(0)

            if(before != ""):
                prevPage = updates[0].date.strftime("%Y-%m-%d-%H");
                if(len(updates) == config.PostsPerPage + 1):
                    nextPage = updates[config.PostsPerPage - 1].date.strftime("%Y-%m-%d-%H");
                    updates.pop()

            else:
                if(len(updates) == config.PostsPerPage + 1):
                    nextPage = updates[config.PostsPerPage - 1].date.strftime("%Y-%m-%d-%H");
                    updates.pop()

            cont = Context({"updates": updates, "user": user, "nextPage": nextPage, "prevPage": prevPage})
        else:
            cont = Context({"user": user})
        result = temp.render(cont).encode('utf-8')
        return result

class NewUpdatePage(PageBase):

    def __init__(self):
        super.__init__()

    def getPage(self, request, resource, user):
        if user.isGroup("poster"):
            temp = loader.get_template("newpost.html")
            cont = Context({"user": user})
            result = temp.render(cont)
            return result
        else:
            return AccessDenied.getPage(resource, user)


class PostPagesHub(PageHubBase):
    def __init__(self):
        self.spokes["edit"] = PostEditPage()
        super(self).__init__()

    def getPage(self, request, resource, user):
        split = str(resource).split("/")

        title = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
        date = urllib.unquote(split[0].encode('ascii')).decode('utf-8')
        post = posts.getPost(title, date)

        try:
            spoke = self.spokes[split[2].lower]
            result = spoke.getPage(request, split[2], user, post)

        except KeyError:
            result = self.defaultPage.getPage(request, split[2], user, post)

        return result

class PostPage(PageBase):


class PostEditPage(PageBase):
    def getPage(self, request, resource, user, post):
        if user.isGroup("poster") == False: return AccessDenied.getPage(request, resource, user)
        try:

            if(post.author != user.firstName+" "+user.lastName and user.permissions < 3):
                return AccessDenied.getPage(request, resource, user)
            temp = loader.get_template("editpost.html")
            cont = Context({"post": post, "user": user})
            return temp.render(cont)
        except IndexError:
            return PageNotFound.getPage(request, resource)

def getPage(request, resource, user):
    split = str(resource).split('/')
    resource=str(urllib.unquote(resource))

    if(len(split) == 1):

    
    elif(split[1] == "New"):

    elif(split[1] != "New"):

        if(len(split) == 3):
            temp = loader.get_template("post.html");
            try:
                title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                logging.info(title)
                post = posts.getPost(title, date);
                if(user.permissions < 1 & post.restricted): return AccessDenied.getPage(request, resource, user)
                comments = posts.getComments(post)
                if(comments.count() == 0): comments = None
                cont = Context({"post": post, "comments": comments, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(request, resource)
            
        elif(split[3] == "Edit"):

            
        elif(split[3] == "Delete"):
            if(user.permissions < 2): return AccessDenied.getPage(request, resource, user)
            try:
                title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                post = posts.getPost(title, date);
                if(post.author != user.firstName+" "+user.lastName and user.permissions < 3):
                    return AccessDenied.getPage(request, resource, user)
                temp = loader.get_template("deletepost.html")
                cont = Context({"post": post, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(request, resource)
        elif(split[3] == "remail"):
		if(user.permissions < 2): return AccessDenied.getPage(request, resource, user)
		try:
                    title = urllib.unquote(split[2].encode('ascii')).decode('utf-8')
                    date = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                    post = posts.getPost(title, date);
                    email.mailToSubscribed(post);
                    return "Re-emailed Everyone."
		except IndexError:
		    return PageNotFound.getPage(request, resource)
        

