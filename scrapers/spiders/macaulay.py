# -*- coding: utf-8 -*-

import json
from lxml import etree, html
import os
import sys

from geojson import Point, Feature
import scrapy

from elasticsearch import Elasticsearch

ES_USER = os.environ.get("ES_USER")
ES_PASS = os.environ.get("ES_PASS")
es = Elasticsearch(['https://{}:{}@es.mrh.io:443'.format(ES_USER, ES_PASS)])
if es.ping() is not True: sys.exit()


class MacaulayLibrarySpider(scrapy.Spider):
    name = 'macaulaylibrary'
    allowed_domains = ['macaulaylibrary.org']
    start_urls = ['http://macaulaylibrary.org/sitemap.xml']

    URLTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
    LOCTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}log"


    # Step 1:
    # Get urls from http://macaulaylibrary.org/sitemap.xml
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
            yield scrapy.Request(url, callback=self.parse_audio_sitemap)

    # Step 2:
    # Get individual media sitemaps
    def parse_audio_sitemap(self, response):
        root = etree.fromstring(response.body)
        children = [sitemap.getchildren()[0] for sitemap in root]
        urls = [child.text for child in children]
        
        for url in urls:

            yield scrapy.Request(url, callback=self.parse_media_page)

    # Step 3:
    # Get JSON-LD schema.org metadata from each individual page (187,000+ pages)
    #
    # TODO: Write response.
    #
    def parse_media_page(self, response):
        h = html.fromstring(response.body)
        json_ld_element = h.cssselect("script[type='application/ld+json']")[0]
        json_ld = json.loads(json_ld_element.text)

        # Only capture resources that have valid geo-coordinates
        json_ld["commonName"] = h.cssselect(".SpecimenHeader-commonName span")[0].text
        json_ld["sciName"] = h.cssselect(".SpecimenHeader-sciName")[0].text
        
        # Tidy up schema.org stuff
        json_ld['geo'].pop("@type")
        json_ld.pop("@type")
        json_ld.pop("@context")

        try:
            es.index(index="audiomnia-dev", doc_type='media', body=json_ld)

            geo = json_ld.pop("geo")
            longitude = geo["longitude"]
            latitude = geo["latitude"]
            if(longitude == "" or latitude == ""): pass

            yield Feature(
                geometry=Point([float(geo["longitude"]), float(geo["latitude"])]),
                properties=json_ld
            )
        except ValueError as e:
            assert False, geo
