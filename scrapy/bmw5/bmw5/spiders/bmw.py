# -*- coding: utf-8 -*-
import scrapy
from ..items import Bmw5Item


class BmwSpider(scrapy.Spider):
    name = 'bmw'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/4867.html',
                  'https://car.autohome.com.cn/pic/series-t/3423.html',
                  'https://car.autohome.com.cn/pic/series/3401.html',
                  'https://car.autohome.com.cn/pic/series/5400.html',
                  'https://car.autohome.com.cn/pic/series/3919.html',
                  'https://car.autohome.com.cn/pic/series/5157.html']

    def parse(self, response):
        car_name = response.xpath("//h2[@class='fn-left cartab-title-name']/a/text()").get()
        ui_boxes = response.xpath("//div[@class='uibox']")
        for ui_box in ui_boxes:
            category = ui_box.xpath(".//div[@class='uibox-title']/a/text()").get()
            image_urls = ui_box.xpath(".//ul/li/a/img/@src").getall()
            urls = list(map(lambda url: response.urljoin(url), image_urls))
            item = Bmw5Item(name=car_name, category=category, image_urls=urls)
            yield item
