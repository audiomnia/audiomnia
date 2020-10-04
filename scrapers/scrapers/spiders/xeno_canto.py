# -*- coding: utf-8 -*-
import scrapy


class XenoCantoSpider(scrapy.Spider):
    name = 'xeno-canto'
    allowed_domains = ['xeno-canto.org']

    URL_TEMPLATE = 'https://xeno-canto.org/{}'

    def start_requests(self):
        for asset_id in range(1, int(self.MAX) +1):
            url = self.URL_TEMPLATE.format(asset_id)
            yield scrapy.Request(url, callback = self.parse_media_page)

    def parse_media_page(self, response):
        try:
            item = {}
            item['url'] = response.url
            item['latitude'] = response.css('table.key-value:nth-child(2) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)::text').get()
            item['longitude'] = response.css('table.key-value:nth-child(2) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)::text').get()
            item['scientific_name'] = response.css('html body#recording-details div#content-area div header h1 span.sci-name::text').get()
            item['common_name'] = response.css('html body#recording-details div#content-area div header h1 a::text').get()
            item['audio_src'] = response.css("meta[itemprop='contentURL']::attr(content)").get()
            item['citation'] = response.css("#player > p:nth-child(14)::text").get()
            item['license'] = response.css('#player > p:nth-child(16) > a:nth-child(1)::text').get()
            # TODO: Add country
            item['location'] = response.css('table.key-value:nth-child(2) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > a:nth-child(1)::text').get()
            item['datetime'] = response.css('table.key-value:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').get()

            yield item
        except Exception as err:
            print(self, response, type(err), err)
