#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

class NuaaMongodb(object):
    def __init__(self):
        conn = pymongo.MongoClient('localhost', 27017)
        self.db = conn.nuaaspider
    def log(self, str):
        print('[*] ' + str)
    def md5(self, ddd):
        #isinstance
        import hashlib
        m2 = hashlib.md5()
        # if isinstance(ddd, str):
        #     m2.update(str)
        # else:
        #     m2.update(str.encode('utf-8'))
        m2.update(repr(ddd).encode('utf-8'))
        return m2.hexdigest()
    def save_undo_url_single(self, url):
        hashs = self.save_hash(url)
        if hashs:
            self.save_url(url)
    def save_undo_url(self, url):
        if type(url) == list:
            for u in url:
                self.save_undo_url_single(u)
        else:
            self.save_undo_url_single(url)
    def save_url(self, url):
        coll = self.db['undo_url']
        if not coll.find_one({'hash':self.md5(url)}):
            coll.insert({'hash': self.md5(url), 'url': url})
    def save_hash(self, url):
        coll = self.db['hash']
        if not coll.find_one({'hash':self.md5(url)}):
            coll.insert({'hash':self.md5(url)})
            return True
        else:
            return False
    def save_nuaa_domin(self, domins, url):
        for domin in domins:
            if domin not in url:
                return 1
        nuaa_domin = self.db['nuaa_domin']
        nuaa_domin.insert({'url': url})
    def save_data_to_whoosh_single(self, url, title, content):
        to_whoosh = self.db['to_whoosh']
        to_whoosh.insert({'url':url, 'title':title, 'content':content})
    def get_url_one_from_mongo(self):
        coll_undo = self.db['undo_url']
        data = coll_undo.find_one()
        if data:
            coll_undo.remove(data['_id'])
            return data['url']
    def get_url_40_from_mongo(self):
        coll_undo = self.db['undo_url']
        uiiii = []
        for i in range(40):
            data = coll_undo.find_one()
            if data:
                coll_undo.remove(data['_id'])
                uiiii.append(data['url'])
            else:
                return uiiii
        return uiiii
    def get_undo_url_count(self):
        coll_undo = self.db['undo_url']
        return coll_undo.count()
    def get_hash_count(self):
        coll_undo = self.db['hash']
        return coll_undo.count()
    def get_all_data_to_whoosh_single(self):
        to_whoosh = self.db['to_whoosh']
        data = to_whoosh.find_one()
        if data:
            to_whoosh.remove(data['_id'])
            return (data['url'], data['title'], data['content'])
        else:
            return False
    def get_to_whoosh_count(self):
        to_whoosh = self.db['to_whoosh']
        return to_whoosh.count()