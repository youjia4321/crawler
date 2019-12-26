# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from .items import Qimai7Item


class Qimai7Pipeline(object):
    def __init__(self):
        self.app_info = open("apps.json", "wb")
        self.app_info_exporter = JsonLinesItemExporter(self.app_info, encoding="utf-8", ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, Qimai7Item):
            self.app_info_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.app_info.close()
