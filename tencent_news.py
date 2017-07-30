#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-27 17:45:37
# Project: tencent_news

from pyspider.libs.base_handler import *
import pymysql
import re
import json


class Handler(BaseHandler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    }

    crawl_config = {
        'headers': headers,
        'itag': 'v3',
    }

    def __init__(self):
        self.paths = ['http://news.qq.com/',
                      ]

    @every(minutes=24 * 60)
    def on_start(self):
        for path in self.paths:
            self.crawl(path, callback=self.get_list_paths)

    def get_list_paths(self, response):
        for each in response.doc('#channelNavPart a').items():
            self.crawl(each.attr.href, callback=self.index_page, fetch_type='js')

    def index_page(self, response):
        for each in response.doc('a[href*="/a/"]').items():
            if "ly.qq.com" in each.attr.href:
                continue
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    def detail_page(self, response):
        url_split = response.url.split('/')
        script_info = get_object_from_js(response.content)
        dict = {
            "date": url_split[4],
            "id": script_info['id'],
            "content": response.doc('#Cnt-Main-Article-QQ p').text(),
            "url": response.url,
            "title": response.doc('.qq_article h1').text(),
            "encoding": response.encoding,
            "cname": script_info['subName']['cname'],
            "is_photo": len(response.doc('#P-QQ')) > 0
        }
        tencent_new = TencentNew(id=dict['id'],
                                 title=dict['title'],
                                 content=dict['content'],
                                 url=dict['url'],
                                 date=dict['date'],
                                 cname=dict['cname'])
        if not dict['is_photo']:
            tencent_new.insert()
        for each in response.doc('a[href*="/a/"]').items():
            if "ly.qq.com" in each.attr.href:
                continue
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')
        return dict


class TencentNew(object):
    def __init__(self,
                 id,
                 title,
                 content,
                 url,
                 date,
                 cname):
        if len(content) > 3000:
            content = content[:3000]

        self.id = id
        self.title = title
        self.content = content
        self.url = url
        self.date = date
        self.cname = cname

    def insert(self):
        db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")

        cursor = db.cursor()

        sql = "INSERT INTO tencent(id,title, content,url, date, cname)\
                 VALUES ('%s', '%s', '%s','%s', '%s','%s')" % (
            self.id, self.title, self.content, self.url, self.date, self.cname)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()

    @classmethod
    def batch_insert(newses):
        sql = "INSERT INTO tencent(id,\
                        title, content,url, date,cname)\
                        VALUES ('%s', '%s', '%s','%s', '%s','%s')"
        params = [(news.id, news.title, news.content, news.url, news.date, news.cname)
                  for news in newses]
        db = pymysql.connect("localhost", "root", "!@#$%^", "news_dataset", charset="utf8")
        cursor = db.cursor()
        try:
            cursor.executemany(sql, params)
            db.commit()
        except:
            db.rollback()


def my_split(text, sep):
    array = []
    flag = True
    pos = 0
    for i in range(len(text)):
        if text[i] == sep:
            if flag:
                seg = text[pos:i]
                if seg[0] == ',' or seg[0] == '}':
                    seg = '""' + seg
                array.append(seg)
                pos = i + 1
        elif text[i] == "\"":
            flag = not flag
    seg = text[pos:]
    if seg[0] == ',' or seg[0] == '}':
        seg = '""' + seg
    array.append(seg)
    return array


def to_json_with_quates(text):
    new_text = []
    ms = my_split(text, ":")
    for i in ms:
        length = len(i)
        pos = length - 1
        new_split = ""
        for j in range(length):
            if i[length - j - 1] is ',' or i[length - j - 1] is '{':
                pos = length - j - 1
                break
        new_split += i[:pos + 1]
        new_split += "\""
        new_split += i[pos + 1:]
        new_split += "\""
        new_text.append(new_split)
    return ":".join(new_text)[:-2]


def get_object_from_js(text):
    p = r'window.ARTICLE_INFO.*?\|\|(.*?)</script>'
    js_info = re.findall(p, text, re.S | re.M)[0].replace("'", '"')
    js_info = js_info.replace(" ", "")
    js_info = js_info.replace("\n", "")
    js_info = to_json_with_quates(js_info)
    print(js_info)
    json_obj = json.loads(js_info)
    return json_obj