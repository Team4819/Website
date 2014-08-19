import hashlib
import logging
import string
from google.appengine.ext import db
import random






def getSubscribed():
    return db.GqlQuery('SELECT email '
                       'FROM User '
                       'WHERE ANCESTOR IS :1 AND subscribed = true ',
                       UserTable_key())




    


    

