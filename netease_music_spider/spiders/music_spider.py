# -*- coding:utf8 -*-
import scrapy
import re
import json
import logging
from scrapy.http import Request, FormRequest
from netease_music_spider import MongoUtils
from netease_music_spider import config

logger = logging.getLogger(__name__)

class MusicSpider(scrapy.Spider):
    name = "music_spider"
    allowed_domains = ["music.163.com"]
    start_urls = ['']
    post_data = config.post_data
    page_num = config.page_num
    page_history = config.history_num

    # 歌单id缓存，防止重复插入。除此还可以使用playlist_buffer、comment_buffer做缓存，然后insert_many
    playlist_id_buffer = []
    db = MongoUtils.MongoDB().db

    def start_requests(self):
        for offset in range(self.page_history * 35, self.page_num * 35, 35):
            full_url = 'http://music.163.com/discover/playlist/?cat=ACG&order=hot&limit=35&offset=' + str(offset)
            logger.info('Getting playlist url:' + full_url)
            yield Request(full_url, callback=self.in_get_playlist)

    def in_get_playlist(self, response):
        playlist_url = 'http://music.163.com/api/playlist/detail?id='
        playlist_ids = response.xpath('//ul/li/div/div/a/@data-res-id').extract()
        for id in playlist_ids:
            if re.match('^\d{4,}\d$', id) and id not in self.playlist_id_buffer:
                self.playlist_id_buffer.append(id)
                yield Request(playlist_url + str(id), callback=self.post_get_playlist)

    def post_get_playlist(self, response):
        collection = self.db.playlist
        result = json.loads(response.body, encoding='utf-8')['result']

        # inserted = collection.update({'id': result['id']}, result, upsert=True)
        # logger.info('Update or Insert to playlist database[%s]' % (str(inserted),))
        if result['id'] not in self.playlist_id_buffer:
            collection.update({'id': result['id']}, result, upsert=True)

        for song in result['tracks']:
            artists = []
            for detail in song['artists']:
                artists.append(detail['name'])
            comment_url = 'http://music.163.com/weapi/v1/resource/comments/%s/?csrf_token=' % (song['commentThreadId'],)
            # 使用FormRequest来进行POST登陆，或者使用下面的方式
            # Request(url, method='POST', body=json.dumps(data))
            yield FormRequest(comment_url, formdata=self.post_data, callback=self.parse,
                              meta={'m_id': song['id'], 'm_name': song['name'], 'artists': artists})

    def parse(self, response):
        collection = self.db.comment
        comment_body = json.loads(response.body, encoding='utf-8')
        music_id = response.meta['m_id']
        comment = {
            'm_id' : music_id,
            'm_name' : response.meta['m_name'],
            'artists' : response.meta['artists'],
            'hotComments' : comment_body.get('hotComments'),
            'total' : comment_body.get('total')
        }

        collection.update({'m_id': music_id}, comment, upsert=True)
        # logger.info('Update or Insert to Mongodb[%s]' % (str(inserted),))
        yield