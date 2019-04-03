# -*- coding: utf-8 -*-
import scrapy


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/news1.html']

    def parse(self, response):
        title = response.css('.dd_bt>a::text').extract()
        title_href = response.css('.dd_bt>a::attr(href)').extract()
        time_created = response.css('.dd_time::text').extract()
        #title_href = response.xpath('//div[@class="dd_bt"]//@href').extract()
        #time_created = response.xpath('//div[@class="dd_time"]/text()').extract()

