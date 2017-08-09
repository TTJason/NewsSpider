#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-31 15:47:46
# Project: netease_music

from pyspider.libs.base_handler import *
import json
import pymysql
import re


class Handler(BaseHandler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    }

    crawl_config = {
        'headers': headers,
        'itag': 'v5',
    }

    def __init__(self):
        self.offset = 0
        self.name_list = get_name_from_singer(self.offset)

    def on_start(self):
        for name in self.name_list:
            for i in range(3):
                print(name, i)
                self.crawl('http://music.163.com/api/search/pc/',
                           data={'s': name, 'offset': 0, 'limit': 100, 'type': 1},
                           callback=self.deal_song_list,
                           method='POST'
                           )
                print(name, i, 'end')

    def get_taskid(self, task):
        return md5string(task['url'] + json.dumps(task['fetch'].get('data', '')))

    def deal_song_list(self, response):
        data = json.loads(response.content)
        if 'result' not in data.keys():
            return
        songs = data['result']['songs']
        for song in songs:
            id = song['id']
            name = song['name'].replace('"', '')
            singer = song['artists'][0]['name'].replace('"', '')
            l = Lyric(id, name, singer=singer)
            l.insert()
            self.crawl('http://music.163.com/api/song/lyric',
                       params={'os': 'pc', 'id': id, 'lv': -1, 'kv': -1, 'tv': -1},
                       callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        data = json.loads(response.content)
        if 'lrc' not in data.keys():
            id = re.findall(r'\&id=(.*?)\&', response.url, re.S | re.M)[0]
            l = Lyric(id=id, lyric='None')
            l.add_lyric()
            return "not has lyric"
        lyric = data['lrc']['lyric'].replace('"', '')
        id = re.findall(r'\&id=(.*?)\&', response.url, re.S | re.M)[0]
        l = Lyric(id=id, lyric=lyric)
        l.add_lyric()
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "text": lyric
        }


class Lyric(object):
    def __init__(self,
                 id,
                 name='',
                 lyric='',
                 singer=''
                 ):
        self.id = id
        self.name = name
        self.lyric = lyric
        self.singer = singer

    def insert(self):
        db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
        cursor = db.cursor()
        sql = 'INSERT INTO lyric(id,name, lyric,singer)\
                 VALUES ("%s", "%s", "%s", "%s")' % (
            self.id, self.name, self.lyric, self.singer)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()

    def add_lyric(self):
        db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
        cursor = db.cursor()

        sql = 'UPDATE lyric SET lyric = "%s"\
                              WHERE id="%s"' % (self.lyric, self.id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            self.insert()
        db.close()


def get_name_from_singer(offset):
    data_array = []
    db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
    cursor = db.cursor()
    sql = "select name from singer"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for res, in results:
            data_array.append(res)
    except:
        print("Error: unable to fetch data")
    db.close()
    return data_array
