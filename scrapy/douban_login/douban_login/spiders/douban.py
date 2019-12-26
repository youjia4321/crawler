# -*- coding: utf-8 -*-
import scrapy
import json


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # start_urls = ['https://www.douban.com/']

    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    profile_url = 'https://www.douban.com/people/161614413/'
    edit_url = 'https://www.douban.com/j/people/161614413/edit_signature'

    def start_requests(self):
        yield scrapy.Request(url="https://www.douban.com/", callback=self.parse, meta={'cookiejar': 1})

    def parse(self, response):
        form_data = {
            'ck': '',
            'remember': 'false',
            'ticket': ''
        }

        name = input("豆瓣账号: ")
        password = input("豆瓣密码: ")

        form_data['name'] = name
        form_data['password'] = password

        yield scrapy.FormRequest(url=self.login_url,
                                 method='POST',
                                 formdata=form_data,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 dont_filter=True,
                                 callback=self.parse_after_login)

    def parse_after_login(self, response):
        resp = json.loads(response.text)

        if resp['description'] == "需要图形验证码":
            print("登录失败， 需要图形验证码")
            print("本项目未设置验证码破解")
            return None

        if resp['status'] == 'success':
            print("用户 %s 登录成功" % resp['payload']['account_info']['name'])
            yield scrapy.Request(url=self.profile_url,
                                 meta={'cookiejar': True},
                                 callback=self.parse_profile)

    def parse_profile(self, response):
        if response.url == self.profile_url:
            print("进入个人主页，准备修改个性签名...")
            form_data = {}
            ck = response.xpath("//input[@name='ck']/@value").get()
            print("当前个性签名：", response.xpath("//span[@id='display']/text()").get())
            signature = input("输入个性签名：")
            form_data['ck'] = ck
            form_data['signature'] = signature
            print(form_data)
            yield scrapy.FormRequest(url=self.edit_url,
                                     meta={'cookiejar': True},
                                     formdata=form_data,
                                     callback=self.after_edit)

    def after_edit(self, response):
        # print(response.url)
        if response.url == self.edit_url:
            print("修改成功")
        else:
            print("修改失败")

