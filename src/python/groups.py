__author__ = 'christian'
import hashlib
import logging
import string
from google.appengine.ext import db
import random


class Group(db.Model):
    name = db.StringProperty()


    def getUsers(self):
        if self.name == "public":
            return db.GqlQuery('SELECT email '
                               'FROM publicSubscribed '
                               'WHERE ANCESTOR IS :1 ',
                               db_key())
        else:
            return db.GqlQuery('SELECT email '
                               'FROM User '
                               'WHERE ANCESTOR IS :1 AND email != NULL AND group = :2',
                               db_key(), self.name)


def db_key():
    return db.Key.from_path('GroupTable-version', 'GroupTable-1')

def getGroup(name):
    result = db.GqlQuery('SELECT * '
                       'FROM Group '
                       'WHERE ANCESTOR IS :1 AND group = :2',
                       db_key(), name)
    if result.count() != 0:
        return result[0]
    else

class noSuchGroup(Exception):
    pass


def newGroup(name):
    if getGroup(name).count() != 0:
        newgroup = Group(parent=db_key())
        newgroup.name = name
        newgroup.put()
        logging.log("Created group with name " + name)
    else:
        logging.log("Already group with name " + name)
        return

def delGroup(name):
    group = getGroup(name)
    if group.count() != 0
        group[0].delete()
        logging.log("Group " + name + " deleted");