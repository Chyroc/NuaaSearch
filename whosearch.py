#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' my whoosh '

__author__ = 'Chyroc'
import sys
# sys.path.append('C:\Python27\Lib\site-packages')

#一个完整的演示
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import shelve
import os
import jieba
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
from whoosh.analysis import Tokenizer, Token

class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode,
            **kwargs)
        seglist=jieba.cut(value,cut_all=False)                       #使用结巴分词库进行分词
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos=start_pos+value.find(w)
            if chars:
                t.startchar=start_char+value.find(w)
                t.endchar=start_char+value.find(w)+len(w)
            yield t                                               #通过生成器返回每个分词的结果token

def ChineseAnalyzer():
    return ChineseTokenizer()

class Whoosh:
    def __init__(self):
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True, analyzer=analyzer), url=STORED,
                        content=TEXT(stored=True, analyzer=analyzer))
        if not os.path.exists("whoosh"):
            os.mkdir("whoosh")
            ix = create_in("whoosh", schema)
        else:
            ix = open_dir("whoosh")
        self.ix = ix
    def writer(self):
        self.writer = self.ix.writer()
    def add(self, title='', url='', content=''):
        try:
            self.writer.add_document(title=title, url=url,content=content)
        except:
            pass
    def commit(self):
        try:
            self.writer.commit()
        except:
            pass
    def search(self, keyword, page, kind='content'):
        try:
            searcher = self.ix.searcher()
            from whoosh.qparser import QueryParser
            qp = QueryParser(kind, schema=self.ix.schema)
            q = qp.parse(keyword)
            data = searcher.search_page(q, page)
            return data
            #pagecount = data.pagecount
            #return {'pagecount':pagecount, 'data':data}
            #return searcher.find(kind, keyword, limit=10)
        except:
            pass
    def close(self):
        self.ix.close()
    def delete(self):
        import shutil
        shutil.rmtree("whoosh")
    def searchq(self, word, key='content'):
        try:
            from whoosh.qparser import QueryParser
            qp = QueryParser("content", schema=self.ix.schema)
            q = qp.parse(u"南")
            s = self.ix.searcher()
            results = s.search(q, limit=20)
            return results
        except:
            pass
# from whoosh.qparser import QueryParser
# with ix.searcher() as searcher:
#     query = QueryParser("content", ix.schema).parse("学生")
#     results = searcher.search(query)
#     for ii in results:
#         print ii
