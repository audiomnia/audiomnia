# -*- coding: utf-8 -*-

from scrapers.exporters import GeoJsonItemExporter


class GeoJSONPipeline(object):
    def open_spider(self, spider):
        file_path = '../data/{}.geojson'.format(spider.name)
        self.file = open(file_path, 'wb')
        self.exporter = GeoJsonItemExporter(self.file)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        geojson = {}
        geo = item.pop("geo")
        longitude = geo.get("longitude", None)
        latitude = geo.get("latitude", None)

        if not longitude or not latitude:
            return None

        # TODO: Validate media URLs here
        # TODO: Backup geolocation by municipality
        geojson["type"] = "Feature"
        geojson["geometry"] = {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
        geojson["properties"] = item

        self.exporter.export_item(geojson)

        return geojson

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
