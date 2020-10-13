# -*- coding: utf-8 -*-

# Based on Scrapy's JsonItemExporter
# See: https://github.com/scrapy/scrapy/blob/master/scrapy/exporters.py
from scrapy.exporters import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.utils.python import to_bytes


class GeoJsonItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
        kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.first_item = True

    def start_exporting(self):
        self.file.write(b'{ "type": "FeatureCollection","features":[\n')

    def finish_exporting(self):
        self.file.write(b"\n]}")

    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(b',\n')
        data = self.encoder.encode(item)
        self.file.write(to_bytes(data, self.encoding))
