from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time


class SeleniumObject(object):
    def __init__(self):
        self.timeout = 10
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1400, 700)

        self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, url):
        self.browser.get(url)
        input_tag = self.wait.until(EC.presence_of_element_located((By.ID, 'kw')))
        submit_tag = self.wait.until(EC.element_to_be_clickable((By.ID, 'su')))

        input_tag.send_keys("python")

        submit_tag.click()
        time.sleep(5)
        print(self.browser.page_source)

    def closed(self):
        self.browser.close()


if __name__ == '__main__':
    driver = SeleniumObject()
    driver.process_request("https://www.baidu.com/")

    # driver.closed()
