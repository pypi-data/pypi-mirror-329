import time
import sys

import get_cap_code_to_log_swjtu

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

class LogIn:
    __head_less = True

    def __init__(self, user_name, pwd):
        options = Options()
        options.add_argument("--no-sandbox")  # 避免权限问题
        options.add_argument("--disable-dev-shm-usage")
        options.use_chromium = True
        if self.__head_less:
            options.add_argument("headless")
        self.user_name = str(user_name)
        self.pwd = str(pwd)
        self.log_url = 'http://jwc.swjtu.edu.cn/service/login.html'
        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()

    def log_in(self):
        self.driver.get(self.log_url)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'JSESSIONID':
                get_cap_code_to_log_swjtu.JSESSIONID = cookie['value']
                get_cap_code_to_log_swjtu.USERNAME = str(self.user_name)
                break
        username_field = self.driver.find_element(value='username')  # 假设用户名输入框的 id 是 'username'
        password_field = self.driver.find_element(value='password')  # 假设密码输入框的 id 是 'password'
        captcha_field = self.driver.find_element(value='ranstring')
        username_field.send_keys(self.user_name)
        password_field.send_keys(self.pwd)
        while True:
            captcha_code = get_cap_code_to_log_swjtu.get_cap_code()
            captcha_field.send_keys(captcha_code)
            login_button = self.driver.find_element(value='submit2')  # 假设登录按钮的 id 是 'submit2'
            login_button.click()
            time.sleep(0.5)
            # 如果浏览器出现弹窗，则重新获取验证码，清空输入框，重新输入
            try:
                self.driver.switch_to.alert.accept()
                time.sleep(0.5)
                captcha_field.clear()
                continue
            except:
                break
        print("dlcg")
        return
        # time.sleep(1)
        # # 执行 JavaScript 在当前窗口打开新的标签页
        # self.driver.execute_script(f"window.open('{global_configs['url']['throw_lessons_sys_url']}', '_blank');")
        # time.sleep(0.5)
        # # 获取当前所有窗口的句柄
        # handles = self.driver.window_handles
        # self.driver.switch_to.window(handles[0])
        # return handles
