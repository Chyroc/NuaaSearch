#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import whosearch
from spider import Spider
from lxml import etree
from queue import Queue
import threading
import time
import whosearch
"""
undo_url

"""


class NuaaSpider(Spider):
    def __init__(self):
        super().__init__()
        self.domin = [
            "nuaa.edu.cn",
            "202.119.71.179"
        ]
        self.srart_urls = [
            "http://ded.nuaa.edu.cn/HomePage/default.aspx",
            "http://e.nuaa.edu.cn/sdms/",
            "http://my.nuaa.edu.cn/forum.php",
            "http://home.nuaa.edu.cn/index.portal",
            "http://www.nuaa.edu.cn/nuaanew/"
        ]
        self.save_undo_url(self.srart_urls)
        self.queue = Queue()

        self.log('__init__')
    def run_queue(self):
        urls = self.get_url_40_from_mongo()
        for url in urls:
            self.queue.put(url)
        while True:
            if self.queue.qsize()<40:
                u = self.get_url_one_from_mongo()
                if u:
                    self.queue.put(u)
                    self.log('add queue')
        # print queue.get()
    def init(self):
        while True:
            url = self.get_url_one_from_queue()
            text = self.do_url(self.domin, url)
            if text:
                html = etree.HTML(text)
                self.log('[url]:'+str(self.get_undo_url_count()) + '  [hash]:'+str(self.get_hash_count())
                         + '  [to_whoosh]:' + str(self.get_to_whoosh_count()) )
                self.deal(url, html, text)
                #search_add_count = search_add_count + 1
    def deal(self, url, html, text=''):
        self.deal_url(url, html) #处理url
        self.deal_text(url, html, text) #处理text
    def deal_url(self, url, html):
        """处理url
        """
        items = self.get_urls_from_html(html)
        allurl = self.join_url(url, items)
        self.add_url(allurl)
        self.log('do deal_url')
    def deal_text(self, url, html, text=''):
        """处理text
        """
        try:
            title = self.get_title_from_html(html)
            body  = self.get_body_from_html(text)
            self.save_data_to_whoosh_single(url, title, body)
            self.log('do deal_text'+title)
        except Exception as e:
            print(url, end='===')
            print(e)
            raise Exception('deal_text error')
    def get_url_one_from_queue(self):
        return self.queue.get()
    def to_whoosh(self):
        whoosh = whosearch.Whoosh()
        whoosh.writer()
        whoosh_commit_count = 0
        while True:
            data = self.get_all_data_to_whoosh_single()
            if data:
                whoosh.add(data[0], data[1], data[2])
                whoosh_commit_count = whoosh_commit_count + 1
                if whoosh_commit_count > 2:
                    whoosh.commit()
                    whoosh_commit_count = 0
if __name__ == '__main__':
    # start
    spider = NuaaSpider()
    # queue
    for i in range(1):
        worker=threading.Thread(target=spider.run_queue)
        worker.start()
    for i in range(1):
        worker = threading.Thread(target=spider.to_whoosh)
        worker.start()
    # init
    for i in range(4):
        worker = threading.Thread(target=spider.init)
        worker.start()
