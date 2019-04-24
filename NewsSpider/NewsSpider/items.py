# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from NewsSpider.utils.common import get_md5

class NewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def date_convert(dt, fm):
    try:
        time_created = datetime.datetime.strptime(dt, fm)
    except Exception as e:
        time_created = datetime.datetime.now()
    return time_created


class ChinanewsItem(scrapy.Item):
    url = scrapy.Field()
    url_id = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    time_created = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    # image_url = scrapy.Field()
    # image_file_path = scrapy.Field()
    editor = scrapy.Field()       

    def get_insert_sql(self):
        url = self['url'][0]
        url_id = get_md5(url)
        title = self['title'][0].strip()
        category = self['category'][0]
        time_created = date_convert(self['time_created'][0].strip()[:17], '%Y年%m月%d日 %H:%M')
        source = self['source'][0] if 'source' in self else self['time_created'][0].strip().split(u'来源：')[1]
        content = ''.join(self['content'][1:])
        # image_file_path = self['image_file_path']
        editor = self['editor'][0].strip()[4:-1] if 'editor' in self else ''

        insert_sql = '''
            INSERT INTO chinanews(url, url_id, title, category, time_created,
                source, content, editor) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            url, url_id, title, category, time_created,
            source, content, editor
            )
        return insert_sql, params


class ZhihuHotItem(scrapy.Item):
    url = scrapy.Field()
    url_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_count = scrapy.Field()
    hot = scrapy.Field()
    
    def get_insert_sql(self):
        url = self['url']
        url_id = get_md5(url)
        title = self['title']
        content = self['content']
        answer_count = self['answer_count']
        hot = int(self['hot'].split()[0])

        insert_sql = '''
            INSERT INTO zhihu_hot(url, url_id, title, content, answer_count, hot) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE answer_count=VALUES(answer_count), hot=VALUES(hot)
        '''
        params = (url, url_id, title, content, answer_count, hot)
        return insert_sql, params