# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Qimai7Item(scrapy.Item):
    # 下标
    index = scrapy.Field()
    # 图标地址
    src = scrapy.Field()
    # app标题信息
    title = scrapy.Field()
    # app类型
    type = scrapy.Field()
    # 分类中的排行
    type_rank = scrapy.Field()
    # 开发者
    company = scrapy.Field()
    # 详情信息
    info = scrapy.Field()
