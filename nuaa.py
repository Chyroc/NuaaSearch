#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spider import Spider
from lxml import etree
from queue import Queue
import threading
import whosearch


class NuaaSpider(Spider):
    def __init__(self):
        super().__init__()
        self.domin = [
            "nuaa.edu.cn"
        ]
        self.notallow_host = [
            'ftp.nuaa.edu.cn'
        ]
        self.not_allow_houzhui = [
            'txt',
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'ini',
            'pdf',
            'dbl',
            'mp4', 'mp3', 'avi', 'mov', 'mpg', 'ico',
            'dll',
            'exe', 'msg',
            'torrent',
            'bat',
            'rar', 'gz', 'zip', 'iso', 'isz',
            'jpg', 'jpeg', 'jpe', 'bmp', 'png', 'psd', 'gif'
            # 'html', 'php', 'htm', 'asp', 'aspx'
        ]
        self.srart_urls = [
            "http://www.nuaa.edu.cn/nuaanew"
        ]
        self.add_url(self.srart_urls)
        self.queue = Queue()
        self.log('__init__')

    def run_queue(self):
        urls = self.get_url_40_from_mongo()
        for url in urls:
            self.queue.put(url)
        while True:
            if self.queue.qsize() < 40:
                u = self.get_url_one_from_mongo()
                if u:
                    self.queue.put(u)
                    # self.log('add queue')

    def init(self):
        while True:
            url = self.get_url_one_from_queue()
            url = self.get_real_url(url)
            text = self.do_url(self.domin, self.notallow_host, self.not_allow_houzhui, url)
            if text:
                html = etree.HTML(text)
                self.deal(url, html, text)
                # search_add_count = search_add_count + 1
    def deal(self, url, html, text=''):
        self.deal_url(url, html)  # 处理url
        self.deal_text(url, html, text)  # 处理text

    def deal_url(self, url, html):
        """处理url
        """
        items = self.get_urls_from_html(html)
        allurl = self.join_url(url, items)
        self.add_url(allurl)
        # self.log('do deal_url')

    def deal_text(self, url, html, text=''):
        """处理text
        """
        try:
            title = self.get_title_from_html(url, html)
            body = self.get_body_from_html(text)
            self.save_data_to_whoosh_single(url, title, body)
            # self.log('do deal_text '+title)
        except Exception as e:
            print(url, end='===')
            print(e)
            raise Exception('deal_text error')

    def get_url_one_from_queue(self):
        return self.queue.get()

    def to_whoosh(self):
        whoosh_commit_count = 0
        while True:
            whoosh = whosearch.Whoosh()
            whoosh.writer()
            # data = self.get_all_data_to_whoosh_single()
            datas = self.get_all_data_to_whoosh_50()
            if datas:
                for data in datas:
                    # print(data['title'], data['url'])
                    whoosh.add(data['title'], data['url'], data['content'])
            whoosh_commit_count = whoosh_commit_count + 1
            # if whoosh_commit_count > 2:
            whoosh.commit()
            # whoosh_commit_count = 0
            whoosh.close()
            # print('whoosh', end='==')
            # print(self.get_to_whoosh_count(), end=', ' )
            # print('url', end='==')
            # print(self.get_undo_url_count(), end=', ')
            # print('hash', end='==')
            # print(self.get_hash_count(), end=', ')
            # print('cha', end='==')
            # print(self.get_hash_count()-self.get_undo_url_count())


if __name__ == '__main__':
    # start
    spider = NuaaSpider()
    # queue
    for i in range(1):
        worker = threading.Thread(target=spider.run_queue)
        worker.start()
    for i in range(1):
        worker = threading.Thread(target=spider.to_whoosh)
        worker.start()
    # init
    for i in range(1):
        worker = threading.Thread(target=spider.init)
        worker.start()
