# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from NewsSpider.settings import BASE_DIR
from scrapy.loader import ItemLoader

class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['https://news.sina.com.cn/roll/']

    rules = (
        Rule(LinkExtractor(allow=r's/'), follow=False),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'NewsSpider.middlewares.JSPageMiddleware':1,
        }
    }

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=BASE_DIR+r'\tools\chromedriver.exe')
        super().__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def spider_closed(self, spider):
        print('Spider closed')
        self.browser.quit()

    def parse_item(self, response):
        item_loader = ItemLoader()

        return item_loader
