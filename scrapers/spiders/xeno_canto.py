# -*- coding: utf-8 -*-
import scrapy


class XenoCantoSpider(scrapy.Spider):
    name = 'xeno-canto'
    allowed_domains = ['xeno-canto.org']
    start_urls = ['http://xeno-canto.org/']

    def parse(self, response):
        pass
