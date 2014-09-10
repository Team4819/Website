__author__ = 'christian'
import hashlib
import logging
import string
from google.appengine.ext import db
import random


class Group(db.Model):
    name = db.StringProperty()

    def get_users(self):
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


def get_group(name):
    result = db.GqlQuery('SELECT * '
                       'FROM Group '
                       'WHERE ANCESTOR IS :1 AND group = :2',
                       db_key(), name)
    if result.count() != 0:
        return result[0]
    else:
        raise NoSuchGroup


class NoSuchGroup(Exception):
    pass


def new_group(name):
    if get_group(name).count() != 0:
        newgroup = Group(parent=db_key())
        newgroup.name = name
        newgroup.put()
        logging.log("Created group with name " + name)
    else:
        logging.log("Already group with name " + name)
        return


def delete_group(name):
    group = get_group(name)
    group[0].delete()
    logging.log("Group " + name + " deleted")