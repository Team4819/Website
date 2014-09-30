from django.template import Context,loader
from .. import posts, config, email, users
import urllib
from datetime import datetime,tzinfo,timedelta,time
from page_base import PageBase
from pagehub_base import PagehubBase
import ErrorPages


class Zone(tzinfo):
    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name

GMT = Zone(0, False, 'GMT')
EST = Zone(-5, False, 'EST')


class UpdatesPage(PagehubBase):
    def __init__(self):
        PagehubBase.__init__(self)
        self.spokes["none"] = MainUpdatesPage()
        self.spokes["new"] = NewUpdatePage()
        self.defaultPage = PostPageHub()


class MainUpdatesPage(PageBase):
    def get_page(self, request, resource, parent):
        r, w = self.check_permissions()
        if not r:
            return ErrorPages.AccessDenied(request, resource)

        temp = loader.get_template("updates.html")
        before = request.request.get("getBefore")
        after = request.request.get("getAfter")

        if before != "":
            updates = posts.getPostsBefore(datetime.strptime(before, "%Y-%m-%d-%H"), (users.currentUser.permissions < 1))
        elif after != "":
            updates = posts.getPostsAfter(datetime.strptime(after, "%Y-%m-%d-%H"), (users.currentUser.permissions < 1))
        else:
            updates = posts.getPostsBefore(datetime.now(), (users.currentUser.permissions < 1))

        if(len(updates) > 0):
            nextPage = None
            prevPage = None

            if(after != ""):
                nextPage = updates[len(updates) - 1].date.strftime("%Y-%m-%d-%H")
                if(len(updates) == config.PostsPerPage + 1):
                    prevPage = updates[1].date.strftime("%Y-%m-%d-%H")
                    updates.pop(0)

            if(before != ""):
                prevPage = updates[0].date.strftime("%Y-%m-%d-%H")
                if(len(updates) == config.PostsPerPage + 1):
                    nextPage = updates[config.PostsPerPage - 1].date.strftime("%Y-%m-%d-%H")
                    updates.pop()

            else:
                if(len(updates) == config.PostsPerPage + 1):
                    nextPage = updates[config.PostsPerPage - 1].date.strftime("%Y-%m-%d-%H")
                    updates.pop()

            cont = Context({"updates": updates, "user": users.currentUser, "nextPage": nextPage, "prevPage": prevPage})
        else:
            cont = Context({"user": users.currentUser})
        result = temp.render(cont).encode('utf-8')
        return result


class NewUpdatePage(PageBase):

    def __init__(self):
        PageBase.__init__(self, group="poster")

    def get_page(self, request, resource, parent):
        r, w = parent.check_permissions()
        if not w:
            return ErrorPages.AccessDenied(request, resource)

        temp = loader.get_template("newpost.html")
        cont = Context({"user": users.currentUser})
        result = temp.render(cont)
        return result


class PostPageHub(PagehubBase):
    def __init__(self):
        PagehubBase.__init__(self)
        self.spokes["edit"] = PostEditPage()
        self.spokes["delete"] = PostDeletePage()
        self.spokes["remail"] = PostRemailPage()
        self.spokes["none"] = PostPage()


    def get_page(self, request, resource):
        split = str(resource).split("/")
        title = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
        date = urllib.unquote(split[0].encode('ascii')).decode('utf-8')
        try:
            post = posts.getPost(title, date)
        except IndexError:
            return ErrorPages.PageNotFound(request, resource)

        try:
            spoke = self.spokes[split[2].lower]
            result = spoke.get_page(request, split[2], post)
        except KeyError:
            result = self.defaultPage.get_page(request, split[2], post)
        return result


class PostPage(PageBase):
    def get_page(self, request, resource, post):
        temp = loader.get_template("post.html");
        if users.currentUser.permissions < 1 & post.restricted:
            return ErrorPages.AccessDenied(request, resource, users.currentUser)
        comments = posts.getComments(post)
        if comments.count() is 0:
            comments = None
        cont = Context({"post": post, "comments": comments, "user": users.currentUser})
        return temp.render(cont)


class PostEditPage(PageBase):
    def get_page(self, request, resource, post):
        if users.currentUser.isGroup("poster") == False: return ErrorPages.AccessDenied(request, resource)
        try:
            if(post.author != users.currentUser.firstName+" "+users.currentUser.lastName and users.currentUser.permissions < 3):
                return ErrorPages.AccessDenied(request, resource, users.currentUser)
            temp = loader.get_template("editpost.html")
            cont = Context({"post": post, "user": users.currentUser})
            return temp.render(cont)
        except IndexError:
            return ErrorPages.PageNotFound(request, resource)


class PostDeletePage(PageBase):
    def get_page(self, request, resource, post):
        if post.author != users.currentUser.firstName+" "+users.currentUser.lastName and users.currentUser.permissions < 3:
            return ErrorPages.AccessDenied(request, resource)
        temp = loader.get_template("deletepost.html")
        cont = Context({"post": post, "user": users.currentUser})
        return temp.render(cont)


class PostRemailPage(PageBase):
    def get_page(self, request, resource, post):
        if(users.currentUser.permissions < 2):
            return ErrorPages.AccessDenied(request, resource, users.currentUser)
        email.mailToSubscribed(post)
        return "Re-emailed Everyone."


        

