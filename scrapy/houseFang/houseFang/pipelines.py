# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from .items import EsfHouseItem, NewHouseItem


class HousefangPipeline(object):
    def __init__(self):
        self.new_house_fp = open('new_house.json', 'wb')
        self.esf_house_fp = open('esf_house.json', 'wb')
        self.new_house_exporter = JsonLinesItemExporter(self.new_house_fp, encoding="utf-8", ensure_ascii=False)
        self.esf_house_exporter = JsonLinesItemExporter(self.esf_house_fp, encoding="utf-8", ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.new_house_exporter.export_item(item)
        else:
            self.esf_house_exporter.export_item(item)

        return item

    def close_spider(self, spider):
        self.new_house_fp.close()
        self.esf_house_fp.close()

