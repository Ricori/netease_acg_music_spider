# -*- coding: UTF-8 -*-  

from pymongo import MongoClient
import sys
import logging

logger = logging.getLogger(__name__)

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'music',
    'username': None,
    'password': None
}

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class MongoDB(Singleton):
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.client[MONGODB_CONFIG['db']]
            if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
                self.db.authenticate(MONGODB_CONFIG['username'], MONGODB_CONFIG['password'])
        except Exception as e:
            logger.error(e)
            sys.exit(1)