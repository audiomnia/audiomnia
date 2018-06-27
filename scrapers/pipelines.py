# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class MacaulaylibraryPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        bulk_command = json.dumps({ "index" : {
            "_index" : "audiomnia-dev",
            "_type" : "media",
            "_id" : item["url"] }
        }) + "\n"
        line = json.dumps(dict(item)) + "\n"

        self.file.write(bulk_command)
        self.file.write(line)
        return item