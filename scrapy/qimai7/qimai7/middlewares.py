# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from scrapy.http import HtmlResponse


# 随机User-Agent
class RandomUserAgent(object):
    """
    随机获取settings.py中配置的USER_AGENTS设置'User-Agent'
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class SeleniumMiddleware(object):
    def __init__(self):
        self.timeout = 50
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 打开浏览器
        self.browser = webdriver.Chrome(options=options)
        # 指定浏览器窗口大小
        self.browser.set_window_size(1400, 700)
        # 设置页面加载超时时间
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, request, spider):
        # 当请求的页面不是当前页面时

        if self.browser.current_url != request.url:
            # 获取页面
            self.browser.get(request.url)
            time.sleep(5)
            # 请求的url开始为https://www.qimai.cn/rank/时，调用滑动界面，每页20个，滑动4次
            if request.url.startswith("https://www.qimai.cn/rank"):
                try:
                    for _ in (0, 1, 2, 3):
                        self.browser.execute_script(
                            "document.getElementsByClassName('cm-explain-bottom')[0].scrollIntoView(true)")
                        time.sleep(5)
                except Exception as e:
                    pass
        else:
            pass
        # 返回页面的response
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source,
                            encoding="utf-8", request=request)

    def spider_closed(self):
        # 爬虫结束 关闭窗口
        time.sleep(10)
        self.browser.close()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # 设置爬虫结束的回调监听
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
