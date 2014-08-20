from django.template import Context,loader
from google.appengine.ext import blobstore
from .. import media
import AccessDenied, PageNotFound
import logging, urllib


def getPage(request, resource, user):
    split = str(resource).split("/")
    if(len(split) == 1):
        folders = media.getFolders(user.permissions == 0)
        logging.info(str(folders.count()))
        result = []
        for folder in folders:
            thumbnail = media.getFolderThumbnail(folder)
            result.append({"name": folder.Name, "description": folder.Description, "thumbnail": thumbnail, "date": folder.Date})
        temp = loader.get_template("Media.html")
        cont = Context({"folders": result, "user": user})
        return temp.render(cont)
    elif(len(split) == 2):
        folder = media.getFolder(urllib.unquote(split[1]))[0]
        if(folder.Restricted and user.permissions == 0): return AccessDenied.getPage(resource, user)
        files = media.getFiles(user.permissions == 0, folder)
        temp = loader.get_template("Folder.html")
        url = blobstore.create_upload_url(urllib.quote("/upload/media/" + split[1]))
        cont = Context({"files": files, "folder": folder, "user": user, "url": url})
        return temp.render(cont)
        
    elif(len(split) == 3):
        if(split[2] == "upload"):
            if(user.permissions < 2):  return AccessDenied.getPage(resource, user)
            temp = loader.get_template("upload.html")
            url = blobstore.create_upload_url(urllib.quote("/upload/media/" + urllib.unquote(split[1])))
            cont = Context({"url": url, "user": user, "folder": urllib.unquote(split[1])})
            return temp.render(cont)
        else:
            try:
                folder = media.getFolder(urllib.unquote(split[1]))[0]
                if(folder.Restricted and user.permissions == 0): return AccessDenied.getPage(resource, user)
                f = media.getFile(urllib.unquote(split[2]), folder)
                if(f.Restricted and user.permissions == 0): return AccessDenied.getPage(resource, user)
                temp = loader.get_template("file.html")
                cont = Context({"file": f, "folder": folder, "user": user})
                return temp.render(cont)
            except IndexError: return PageNotFound.getPage(resource)
