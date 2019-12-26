# -*- coding: utf-8 -*-
import scrapy
from ..items import Qimai7Item


class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    allowed_domains = ['qimai.cn']
    start_urls = ['https://www.qimai.cn/rank']

    def parse(self, response):
        base = response.xpath(
            "//div[@class='ivu-row rank-all-item']/div[@class='ivu-col ivu-col-span-8']"
            "[2]//ul/li[@class='child-item']/div[@class='ivu-row']")
        for box in base:
            item = Qimai7Item()
            item['index'] = box.xpath(".//div[@class='ivu-col ivu-col-span-3 left-item']/span/text()").get()
            item['src'] = box.xpath(".//img/@src").get()
            item['title'] = box.xpath(".//p[@class='medium-txt']/a/text()").get().strip().replace("\n", "")
            item['type'] = box.xpath(".//p[@class='small-txt']/text()").get().strip().replace("\n", "").split(":")[0]
            item['type_rank'] = box.xpath(".//p[@class='small-txt']//span[@class='rank-item']/text()").get()
            item['company'] = box.xpath(".//p[@class='small-txt']//span[@class='company-item']/text()").get()
            item['info'] = "https://www.qimai.cn" + box.xpath(".//div[@class='info-content']//a/@href").get()

            yield item
