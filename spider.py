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

    def do_url(self, domins, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        }
        timeout = 10
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            if r.status_code == requests.codes.ok:
                self.save_nuaa_domin(domins, url)
                r.encoding = self.get_encoding_from_reponse(r)
                return r.text
        except requests.exceptions.ConnectTimeout:
            self.log('ConnectTimeout   ' + url + '=========================================================')
        except requests.exceptions.Timeout:
            self.log('Timeout   ' + url + '=========================================================')
        except requests.exceptions.ConnectionError:
            self.log('ConnectionError   ' + url + '=========================================================')
        except requests.exceptions.RequestException as e:
            if 'javascript' in url:
                self.log('javascript   ' + url + '=========================================================')
            elif 'mailto:' in url:
                self.log('mailto   ' + url + '=========================================================')
            else:
                print(e)
                raise Exception('requests.exceptions.RequestException')
                exit()
        return False

    def join_url_single(self, base, url):
        return urlparse.urljoin(base, url)

    def join_url(self, base, urls):
        return [self.join_url_single(base, url) for url in urls]

    def get_urls_from_html(self, html):
        return html.xpath('//a/@href')

    def add_url(self, urls):
        self.save_undo_url(urls)

    def get_title_from_html(self, html):
        tit = html.xpath('//title/text()')
        if tit:
            return tit[0].strip()
        else:
            return 'unknow title'

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
