# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['https://news.sina.com.cn/roll/']

    def start_requests(self):
        browser = webdriver.Chrome(executable_path=r'C:\GitHub\spiders\NewsSpider\tools\chromedriver.exe')
        browser.get(self.start_urls[0])
        time.sleep(10)
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True)]
    
    def parse(self, response):
        time_created = response.xpath('//span[@class="c_time"]/text()')
        print(time_created)
        pass
