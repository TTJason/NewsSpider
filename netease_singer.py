#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-08 09:28:22
# Project: netease_singer

from pyspider.libs.base_handler import *
import re
import time
import pymysql


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
        'itag': 'v5',
    }

    def __init__(self):
        self.ids = [1001, 1002, 1003]
        self.initials = [i + 65 for i in range(26)]
        self.initials.append(0)

    @every(minutes=24 * 60)
    def on_start(self):
        for id in self.ids:
            for initial in self.initials:
                self.crawl('http://music.163.com/discover/artist/cat',
                           params={'id': id,
                                   'initial': initial},
                           callback=self.index_page)

    def index_page(self, response):
        singers = []
        for each in response.doc('#m-artist-box a.nm[href*="/artist?"]').items():
            id = each.attr.href.split('?')[-1].split('=')[-1]
            name = each.text().strip()
            type = re.findall(r'\?id=(.*?)&', response.url, re.S | re.M)[0]
            singers.append(Singer(id,
                                  name,
                                  type))
            # self.crawl(each.attr.href, callback=self.detail_page)
        Singer.batch_insert(singers)
        time.sleep(3)
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }


class Singer(object):
    def __init__(self,
                 id,
                 name,
                 type,
                 ):
        self.id = id
        self.name = name
        self.type = type

    def insert(self):
        db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")

        cursor = db.cursor()

        sql = "INSERT INTO singer(id,name, type)\
                 VALUES (%s, %s, %s)" % (
            self.id, self.name, self.type)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()

    @classmethod
    def batch_insert(cls, singers):
        sql = "INSERT INTO singer(id,\
                        name, type)\
                        VALUES (%s, %s, %s)"
        params = [(singer.id, singer.name, singer.type)
                  for singer in singers]
        db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
        cursor = db.cursor()
        try:
            cursor.executemany(sql, params)
            db.commit()
        except:
            db.rollback()
