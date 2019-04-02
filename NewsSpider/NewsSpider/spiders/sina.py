# -*- coding: utf-8 -*-
import scrapy


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['https://news.sina.com.cn/roll']
    start_urls = ['http://https://news.sina.com.cn/roll/']

    def parse(self, response):
        pass
