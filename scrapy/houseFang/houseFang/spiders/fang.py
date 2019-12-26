# -*- coding: utf-8 -*-
import scrapy
from ..items import NewHouseItem, EsfHouseItem
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//table[@id='senfe']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text
            # 不抓取海外的城市的房源
            if province == "其它":
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # 构建新房链接 new_house_url
                url_module = city_url.split("//")
                scheme = url_module[0]
                _name = url_module[1].split(".")[0]
                new_house_url = scheme + "//" + _name + ".newhouse.fang.com/house/s/"

                # 构建二手房链接 esf_url
                esf_url = scheme + "//" + _name + ".esf.fang.com/"
                yield scrapy.Request(url=new_house_url, callback=self.parse_newhouse, meta={"info": (province, city)})

                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={"info": (province, city)})

    def parse_newhouse(self, response):
        province, city = response.meta.get("info")
        lis = response.xpath("//div[contains(@class, 'nl_con')]/ul/li")
        for li in lis:
            try:
                name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()

                origin_url = 'https:' + li.xpath(".//div[@class='nlcd_name']/a/@href").get()

                house_type_list = li.xpath(".//div[@class='house_type clearfix']/a/text()").getall()
                house_type_list = list(filter(lambda x: x.endswith("居"), house_type_list))
                rooms = "/".join(house_type_list)

                district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
                district = re.search(r".*\[(.+)\].*", district_text).group(1)

                price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r"\s|广告", "", price)
                address = li.xpath(".//div[@class='address']/a/@title").get()

                sale = li.xpath(".//div[@class='fangyuan']/span/text()").get()

                area = "".join(li.xpath(".//div[@class='house_type clearfix']/text()").getall())
                area = re.sub(r"\s|－|/", "", area)

                item = NewHouseItem(name=name,
                                    city=city,
                                    province=province,
                                    address=address,
                                    area=area,
                                    district=district,
                                    price=price,
                                    sale=sale,
                                    rooms=rooms,
                                    origin_url=origin_url)
                yield item
            except:
                continue

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()

        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_newhouse,
                                 # dont_filter=True,
                                 meta={"info": (province, city)})

    def parse_esf(self, response):
        province, city = response.meta.get("info")
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            try:
                name = dl.xpath(".//p[@class='add_shop']/a/@title").get()
                if name.strip() == "":
                    continue
                rooms_info = "".join(dl.xpath(".//p[@class='tel_shop']//text()").getall())
                rooms_info = re.sub(r"\s", "", rooms_info).split("|")
                room_details = "|".join(rooms_info[:-1])
                owner = rooms_info[-1]

                address = dl.xpath(".//p[@class='add_shop']/span/text()").get()

                price = "".join(dl.xpath(".//dd[@class='price_right']//text()").getall())
                price = re.sub(r"\s", "", price)
                origin_url = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
                item = EsfHouseItem(province=province,
                                    city=city,
                                    info=room_details,
                                    name=name,
                                    owner=owner,
                                    address=address,
                                    price=price,
                                    origin_url=origin_url)
                yield item
            except:
                continue

        next_url = response.xpath("//div[@class='page_al']/p[1]/a/@href").get()

        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_esf,
                                 meta={"info": (province, city)})

