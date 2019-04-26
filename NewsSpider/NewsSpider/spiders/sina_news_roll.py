# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from NewsSpider.items import SinaNewsRollItem


class SinaNewsRollSpider(scrapy.Spider):
    name = 'sina_news_roll'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'NewsSpider.middlewares.RandomUserAgentMiddleware': 1,
        },
        'ITEM_PIPELINES':{
            'NewsSpider.pipelines.MysqlTwistedPipline':1,
        },
    }

    def parse(self, response):
        news_json = json.loads(response.text)
        for news in news_json['result']['data']:
            news_url = news['url']
            intro = news['intro']
            yield scrapy.Request(news_url, meta={'intro':intro}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item_loader = ItemLoader(item=SinaNewsRollItem(), response=response)
        item_loader.add_value('intro', response.meta.get('intro'))
        item_loader.add_value('url', response.url)
        item_loader.add_css('title', '.main-title::text')
        item_loader.add_css('category', '.channel-path>a::text')
        if not item_loader.add_css('source', '.date-source>a::text'):
            item_loader.add_xpath('source', '//*[@class="source ent-source"]/text()')
            item_loader.add_xpath('date', '//*[@class="date"]/text()')
        else:    
            item_loader.add_css('source', '.date-source>a::text')
            item_loader.add_css('date', '.date-source>span::text')
        item_loader.add_css('content', '.article>p::text')
        item_loader.add_css('keywords', '#keywords>a::text')
        news_item = item_loader.load_item()
        yield news_item