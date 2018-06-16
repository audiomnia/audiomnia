# -*- coding: utf-8 -*-

import json
from lxml import etree
import sys

from bs4 import BeautifulSoup
import scrapy

def HTTPS(string):
    return string.replace("http://", "https://")

class MacauleySpider(scrapy.Spider):
    name = 'macauley'
    allowed_domains = ['macaulaylibrary.org']
    start_urls = ['http://macauleylibrary.org/sitemap.xml']

    URLTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
    LOCTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}log"

    # Step 1:
    # Get urls from http://macauleylibrary.org/sitemap.xml
    def parse(self, response):
        # generate etree from response string: 
        # http://www.fis.unipr.it/doc/python-lxml-2.2.3/doc/html/tutorial.html
        root = etree.fromstring(response.body)

        # Navigate XML subtree and fetch URL strings
        children = [sitemap.getchildren()[0] for sitemap in root]
        url_tags = filter(lambda child: child.tag == self.URLTAG, children)
        urls = [url.getchildren()[0].text for url in url_tags]
        xml_urls = filter(lambda url: ".xml" in url, urls)

        # Queue requests and call parse_audio_sitemap against responses
        for url in xml_urls:
            yield scrapy.Request(HTTPS(url), callback=self.parse_audio_sitemap)

    # Step 2:
    # Get individual media sitemaps
    def parse_audio_sitemap(self, response):
        root = etree.fromstring(response.body)
        children = [sitemap.getchildren()[0] for sitemap in root]
        urls = [child.text for child in children]
        
        for url in urls:
            yield scrapy.Request(HTTPS(url), callback=self.parse_media_page)

    # Step 3
    # Get JSON-LD schema.org metadata from each individual page (187,000+ pages)
    def parse_media_page(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        json_ld = soup.find('script', {'type':'application/ld+json'})

        if json_ld:
            yield json.loads(json_ld.text)