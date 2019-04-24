# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class NewsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ChinanewsImagesPipeline(ImagesPipeline):
    # 获取image保存路径
    def item_completed(self, results, item, info):
        image_file_path = ''    # 设置默认值.有的文章,不包含图片
        for ok, value in results:
            image_file_path = value['path']
        item['image_file_path'] = image_file_path
        return item


class JsonExporterPipleline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('testExport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MySQLPipeline(object):
    # 同步
    def __init__(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'qixt',
            db = 'news_spider',
            charset="utf8",
            use_unicode=True
        )
        self.cur = self.conn.cursor()
    
    def process_item(self, item, spider):
        insert_sql = '''
            INSERT INTO chinanews(url, url_id, title, category, time_created,
                source, content, image_file_path, editor) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            item['url'], item['url_id'], item['title'], item['category'],
            item['time_created'], item['source'], item['content'],
            item['image_file_path'], item['editor']
            )
        self.cur.execute(insert_sql, params)
        self.conn.commit()


class MysqlTwistedPipline(object):
    # 异步
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            port = settings['MYSQL_PORT'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,)
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)
    
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
    
    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)
