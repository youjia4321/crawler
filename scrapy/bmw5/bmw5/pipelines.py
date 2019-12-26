# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request


class Bmw5Pipeline(object):

    def process_item(self, item, spider):
        base_dir = "images\\" + item['name']
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), base_dir)
        if not os.path.exists(path):
            os.mkdir(path)

        category = item['category']
        urls = item['image_urls']
        category_path = os.path.join(path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name = url.split("_")[-1]
            request.urlretrieve(url, os.path.join(category_path, image_name))

        return item
