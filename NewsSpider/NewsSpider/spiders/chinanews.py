# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/best-news/news1.html']
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'NewsSpider.middlewares.RandomUserAgentMiddleware': 1,
        }
    }

    def parse(self, response):
        news_urls = response.css('.dd_bt>a::attr(href)').extract()
        for news_url in news_urls:
            if 'shipin' not in news_url:
                yield Request(url=news_url, callback=self.parse_detail)
        # yield Request(url='http://www.chinanews.com/news2.html', callback=self.parse)

    def parse_detail(self, response):
        title = response.css('#cont_1_1_2>h1::text').extract()[0].strip()
        category = response.xpath('//div[@id="nav"]/a[2]/text()').extract()
        time_created = response.css('div.left-t::text').extract()[0].strip()[:-4]
        source = response.css('div.left-t>a:nth-child(1)::text').extract()
        content = response.css('div.left_zw>p::text').extract()
        content = '\n'.join([i.strip() for i in content[1:]])
        editor = response.css('.left_name .left_name::text').extract()
        if editor:
            editor = editor[0].strip()[4:-1] 
        else:    
            editor = 'None'
        
        print('xx')


