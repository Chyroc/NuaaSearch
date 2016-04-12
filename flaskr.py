# -*- coding: utf-8 -*-
import whosearch
from nuaamongodb import NuaaMongodb
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def index():
    # html = """
    # <title>南航搜索</title>
    # <form action="/search" method="get">
    # <input type="text" name=value />
    # <input type="hidden" name="page" value="1" />
    # <input type="submit" value="提交" />
    # """
    # return html
    nuaamon = NuaaMongodb()
    urlcount = nuaamon.get_hash_count()-nuaamon.get_undo_url_count()
    return render_template('index.html', urlcount=urlcount)#, entries=entries


@app.route('/search/')
def search():
    value = request.args.get('value')
    page = request.args.get('page')
    if page:
        if type(page) == str:
            page = int(page)
    else:
        page = 1
    s = '<title>南航搜索</title>'
    s = s + '<a href="../">返回主页</a><br><br>'
    whoosh = whosearch.Whoosh()
    seadata = whoosh.search(value, page)
    posts = []
    pagecount = 1
    if seadata:
        pagecount = seadata.pagecount
        for data in seadata:
            posts.append({'url':data['url'], 'title':data['title']})
            #s = s + '<a href="' + data['url'] + '" target="_blank">' + data['title'] + '</a><br><br>'
        s = s + '[<a href="/search/?value=' + value + '&page=1">首页</a>]'
        if page < pagecount:
            s = s + ' [<a href="/search/?value=' + value + '&page=' + str(page + 1) + '">下页</a>]'
        s = s + ' [<a href="/search/?value=' + value + '&page=' + str(pagecount) + '">尾页</a>]'
    else:
        s = s + '空！'
    return render_template('search.html', value=value, posts=posts, page=page, pagecount=pagecount)
    #return s


if __name__ == '__main__':
    app.run()
