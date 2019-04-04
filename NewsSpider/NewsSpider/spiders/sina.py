# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['https://news.sina.com.cn/roll/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'NewsSpider.middlewares.JSPageMiddleware':1,
        }
    }
    
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=r'C:\GitHub\spiders\NewsSpider\tools\chromedriver.exe')
        super().__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def spider_closed(self, spider):
        print('Spider closed')
        self.browser.quit()
    
    def parse(self, response):
        time_created = response.xpath('//span[@class="c_time"]/text()').extract()
        print(time_created)
