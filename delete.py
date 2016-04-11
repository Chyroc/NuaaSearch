# -*- coding:utf-8 -*-
import pymongo
import whosearch

whoosh = whosearch.Whoosh()
whoosh.delete()
conn = pymongo.MongoClient('localhost', 27017)
db = conn.nuaaspider
db['nuaa_domin'].drop()
db['undo_url'].drop()
db['hash'].drop()
