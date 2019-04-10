# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
from scrapy.loader import ItemLoader
from NewsSpider.items import ChinanewsItem


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/best-news/news1.html']
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'NewsSpider.middlewares.RandomUserAgentMiddleware': 1,
        },
        'ITEM_PIPELINES':{            
            # 'NewsSpider.pipelines.ChinanewsImagesPipeline':1,
            # 'NewsSpider.pipelines.JsonExporterPipleline': 2,
            'NewsSpider.pipelines.MysqlTwistedPipline':1,
        },
        # 'IMAGES_URLS_FIELD':'image_url',
        # 'IMAGES_STORE':'NewsSpider/images',
    }

    def parse(self, response):
        news_urls = response.css('.dd_bt>a::attr(href)').extract()
        for news_url in news_urls:
            if 'shipin' not in news_url:
                yield Request(url=news_url, callback=self.parse_detail)
        #yield Request(url='http://www.chinanews.com/news2.html', callback=self.parse)

    def parse_detail(self, response):
        item_loader = ItemLoader(item=ChinanewsItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_css('title', '#cont_1_1_2>h1::text')
        item_loader.add_xpath('category', '//div[@id="nav"]/a[2]/text()')
        item_loader.add_css('time_created', 'div.left-t::text')
        item_loader.add_css('source', 'div.left-t>a:nth-child(1)::text')
        item_loader.add_css('content', 'div.left_zw>p::text')
        # item_loader.add_css('image_url', '.left_zw img::attr(src),.left_ph img::attr(src)')
        item_loader.add_css('editor', '.left_name .left_name::text')
        news_item = item_loader.load_item()

        yield news_item
