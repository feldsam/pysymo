from pymongo import MongoClient

__author__ = 'icoz'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


def get_hosts():
    return db.messages.distinct('h')


def get_applications():
    return db.messages.distinct('a')


def get_facility():
    return  db.messages.distinct('f')