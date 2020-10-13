# -*- coding: utf-8 -*-

import json

import scrapy


class MacaulayLibrarySpider(scrapy.Spider):
    name = 'macaulaylibrary'
    allowed_domains = ['macaulaylibrary.org']

    URL_TEMPLATE = 'https://macaulaylibrary.org/asset/{}'
    start_asset_id = 1

    URLTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
    LOCTAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}log"

    # Step 1:
    # Start the scraper by making a big array of all the urls from
    # start asset_id to max_asset_id, then concurrently requesting them

    # TODO: Caching
    # TODO: Error caching
    #           - Bad description split
    #           - 40X errors
    #           - Unidentified
    #           - No lat lon
    def start_requests(self):
        for asset_id in range(1, int(self.MAX) + 1):
            url = self.URL_TEMPLATE.format(asset_id)
            yield scrapy.Request(url, callback=self.parse_media_page)

    # Step 2:
    # Get JSON-LD schema.org metadata from each individual page, as well as an
    # untested derivation of the media URL.
    def parse_media_page(self, response):
        try:
            selector = "script[type='application/ld+json']::text"
            json_ld = response.css(selector).get()
            if json_ld is None:
                yield None
            else:
                item = json.loads(json_ld)
                oldurl = "macaulaylibrary.org/asset"
                newurl = "cdn.download.ams.birds.cornell.edu/api/v1/asset"
                item["audio"] = item["url"].replace(oldurl, newurl)

                yield item
        except Exception as err:
            print(self, response, type(err), err)
