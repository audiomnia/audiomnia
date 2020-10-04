# -*- coding: utf-8 -*-

from scrapers.exporters import GeoJsonItemExporter
from scrapy.exceptions import DropItem
from scrapy.item import Item, Field
from scrapy.http import Request

# const datetime = desc[5]

# TODO: Error caching
#           - Bad description split
#           - 40X errors
#           - Unidentified
#           - No lat lon
# TODO: Error logging
class GeoJSONPipeline(object):
    def open_spider(self, spider):
        file_path = '../data/{}.geojson'.format(spider.name)
        self.file = open(file_path, 'wb')
        self.exporter = GeoJsonItemExporter(self.file)
        self.exporter.start_exporting()

    def item_is_valid(self, item):
        if not item.get('latitude', False) or not item.get('longitude', False):
            raise DropItem("Missing `latitude` and/or `latitude` in %s" % item)

        if not item.get('scientific_name'):
            raise DropItem("Missing `scientific_name` in %s" % item)

        if not item.get('common_name'):
            raise DropItem("Missing `common_name` in %s" % item)

        if not item.get('audio_src'):
            raise DropItem("Missing `audio_src` in %s" % item)

        if not item.get('citation'):
            raise DropItem("Missing `citation` in %s" % item)

        if not item.get('license'):
            raise DropItem("Missing `license` in %s" % item)

        # TODO: Split into administrative hierarchy
        if not item.get('location'):
            raise DropItem("Missing `location` in %s" % item)

        # TODO: ISO Timestamp
        if not item.get('datetime'):
            raise DropItem("Missing `datetime` in %s" % item)

    def process_item(self, item, spider):
        self.item_is_valid(item)

        self.exporter.export_item(item)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
