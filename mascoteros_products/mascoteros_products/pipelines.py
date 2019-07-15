# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter


class MascoterosProductsPipeline(object):

    def open_spider(self, spider):
        self.file = open('product_info.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(
            dict(item),
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        ) + ",\n"
        self.file.write(line)
        return item