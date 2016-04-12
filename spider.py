#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lxml.html
from urllib import parse as urlparse
import requests.exceptions
import requests
from nuaamongodb import NuaaMongodb


class Spider(NuaaMongodb):
    def __init__(self):
        super().__init__()

    def fail_save_url(self, url):
        pass
        # mymon.insert({'url': url})

    def get_encoding_from_reponse(self, reponse):
        encoding = requests.utils.get_encodings_from_content(reponse.text)
        if encoding:
            return encoding[0]
        else:
            return requests.utils.get_encoding_from_headers(reponse.headers)
    def check_domin(self, domins, url):
        for domin in domins:
            if domin in url:
                return True
        return False
    def check_not_allow_houzhui(self, not_allow_houzhui, url):
        for al in not_allow_houzhui:
            if '.' + al in url:
                return False
        return True
    def check_notallow_host(self, notallow_host, url):
        for al in notallow_host:
            if al in url:
                return False
        return True
    def do_url(self, domins, notallow_host, not_allow_houzhui, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        }
        timeout = 10
        try:
            if self.check_domin(domins, url):
                if self.check_not_allow_houzhui(not_allow_houzhui, url):
                    if self.check_notallow_host(notallow_host, url):
                        r = requests.get(url, headers=headers, timeout=timeout)
                        if r.status_code == requests.codes.ok:
                            # self.save_nuaa_domin(domins, url)
                            # self.save_nuaa_source(sources, url)
                            r.encoding = self.get_encoding_from_reponse(r)
                            return r.text
        except requests.exceptions.ConnectTimeout:
            pass
            #self.log('ConnectTimeout   ' + url + '=========================================================')
        except requests.exceptions.Timeout:
            pass
            #self.log('Timeout   ' + url + '=========================================================')
        except requests.exceptions.ConnectionError:
            self.log('ConnectionError   ' + url + '=========================================================')

        except requests.exceptions.RequestException as e:
            if 'javascript' in url:
                pass
                #self.log('javascript   ' + url + '=========================================================')
            elif 'mailto:' in url:
                pass
                #self.log('mailto   ' + url + '=========================================================')
            else:
                print(e)
                exit()
                raise Exception('requests.exceptions.RequestException')
        return False
    def join_url_single(self, base, url):
        return urlparse.urljoin(base, url)

    def join_url(self, base, urls):
        return [self.join_url_single(base, url) for url in urls]

    def get_urls_from_html(self, html):
        return html.xpath('//a/@href')

    def add_url(self, urls):
        self.save_undo_url(urls)

    def get_title_from_html(self, url, html):
        tit = html.xpath('//title/text()')
        if tit:
            return tit[0].strip()
        else:
            return url

    def get_body_from_html(self, text):
        # text = rehtml.strip_tags(text)
        # dr = re.compile(r'<[^>]+>', re.S)
        # text = dr.sub('', html)
        # text = re.sub('<[^>]+>', '', text)
        document = lxml.html.document_fromstring(text)
        body = document.text_content()
        return body

    def do_ziyuan(self):
        """doc,pdf,rar,
        """
        pass
