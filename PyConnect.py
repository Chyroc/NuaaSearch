#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo


class PyConnect(object):
    def __init__(self, host, port):
        try:
            self.conn = pymongo.MongoClient(host, port)
        except  Error:
            print('connect to %s:%s fail' % (host, port))
            exit(0)

    def __del__(self):
        self.conn.close()

    def use(self, dbname):
        self.db = self.conn[dbname]

    def setCollection(self, collection):
        if not self.db:
            print('don\'t assign database')
            exit(0)
        else:
            self.coll = self.db[collection]

    def find(self, query={}):
        if type(query) is not dict:
            print('the type of query isn\'t dict')
            exit(0)
        try:
            if not self.coll:
                print('don\'t assign collection')
            else:
                result = self.coll.find(query)
        except NameError:
            print('some fields name are wrong in ', query)
            exit(0)
        return result

    def insert(self, data):
        if type(data) is not dict:
            print('the type of insert data isn\'t dict')
            exit(0)
        self.coll.insert(data)

    def remove(self, data):
        if type(data) is not dict:
            print('the type of remove data isn\'t dict')
            exit(0)
        a = self.coll.remove(data)
        print(a)
    def update(self, data, setdata):
        if type(data) is not dict or type(setdata) is not dict:
            print('the type of update and data isn\'t dict')
            exit(0)
        self.coll.update(data, {'$set': setdata})

    def dropDatabase(self):
        pass

# if __name__ == '__main__':
#     connect = PyConnect('localhost', 27017)
#     connect.use('test_for_new')
#     connect.setCollection('collection1')
#     connect.insert({'a': 10, 'b': 19})
#     connect.insert({'a': 'url', 'b': 19})
#     result = connect.find({'a':'url'})
#     # connect.update({'a':10, 'b':1}, {'b':10})
#     # x也是dict类型，非常好
#     #connect.remove({'a': 10})
#     for x in result:
#         print(x)
#         #connect.remove({'a': x['a'], 'b':x['b']})
