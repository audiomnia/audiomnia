# -*- coding: utf-8 -*-

import json
from lxml import etree, html
import os
import sys

import scrapy


class MacaulayLibrarySpider(scrapy.Spider):
    name = 'macaulaylibrary'
    allowed_domains = ['macaulaylibrary.org']

    URL_TEMPLATE = 'https://macaulaylibrary.org/asset/{}'
    start_asset_id = 1
    max_asset_id = 10

    URLTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
    LOCTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}log"

    # Step 1:
    # Start the scraper by making a big array of all the urls from
    # start asset_id to max_asset_id, then concurrently requesting them
    def start_requests(self):
        for asset_id in range(self.start_asset_id, self.max_asset_id):
            url = self.URL_TEMPLATE.format(asset_id)
            yield scrapy.Request(url, callback=self.parse_media_page)


    # Step 2:
    # Get JSON-LD schema.org metadata from each individual page, as well as an
    # untested derivation of the media URL.
    def parse_media_page(self, response):
        h = html.fromstring(response.body)
        json_ld_element = h.cssselect("script[type='application/ld+json']")[0]
        json_ld = json.loads(json_ld_element.text)

        # Only capture resources that have valid geo-coordinates
        # json_ld["commonName"] = h.cssselect(".SpecimenHeader-commonName span")[0].text
        # json_ld["sciName"] = h.cssselect(".SpecimenHeader-sciName")[0].text

        # Handle geospatial stuff
        geo = json_ld.pop("geo")
        json_ld["geo"] = {
            "lat": geo.get("latitude", ""),
            "lon": geo.get("longitude", "")
        }

        # Remove any schema.org stuff that's left
        json_ld.pop("@type")
        json_ld.pop("@context")

        json_ld["likely_media_url"] = json_ld["url"].replace("https://macaulaylibrary.org/asset/", "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/")

        yield json_ld