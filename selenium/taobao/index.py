from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class SeleniumObject(object):
    def __init__(self):
        self.timeout = 10
        # 创建浏览器对象
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # 设置开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 不加载图片,加快访问速度
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()

        self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, url):
        self.browser.get(url)
        # input_tag = self.wait.until(EC.presence_of_element_located((By.ID, 'q')))
        # submit_tag = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                                          '#J_TSearchForm > div.search-button > button')))
        #
        # input_tag.send_keys("美食")
        #
        # submit_tag.click()

        # 密码登录
        self.wait.until(EC.element_to_be_clickable((By.ID, 'J_Quick2Static'))).click()

        username_input = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_username_1')))

        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_password_1')))

        user = input("用户名：")
        password = input("密码：")

        username_input.send_keys(user)
        password_input.send_keys(password)

        time.sleep(5)

        dragger = self.browser.find_element_by_id('nc_1_n1z')  # 滑块定位

        action = ActionChains(self.browser)
        for index in range(500):
            try:
                action.drag_and_drop_by_offset(dragger, 500, 0).perform()
                # 平行移动鼠标，此处直接设一个超出范围的值，这样拉到头后会报错从而结束这个动作

            except Exception:
                break

        # 点击登录
        print('*点击登录')
        self.browser.find_element_by_id('J_SubmitStatic').click()
        print('@')

    def closed(self):
        self.browser.close()


if __name__ == '__main__':
    driver = SeleniumObject()
    driver.process_request("https://login.taobao.com/member/login.jhtml")

    # driver.closed()
