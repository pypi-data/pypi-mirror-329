from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from seleniumwire import webdriver as seleniumwire_webdriver
from selenium.webdriver import Edge
import time


class AutomationUtils:
    """
    用于自动化测试的工具类
    """
    def __init__(self, driver_path=r'D:\msedgedriver.exe', headless=False, debug=False):
        """
        初始化方法
        :param driver_path: 浏览器驱动路径
        """
        edge_options = EdgeOptions()
        # 配置下载参数（核心设置）
        prefs = {
            # "download.default_directory": download_path,
            "download.prompt_for_download": False,  # 禁用下载弹窗
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
        if not debug:
            edge_options.add_argument("--headless")
        edge_options.add_experimental_option("prefs", prefs)
        edge_options.add_argument("--no-sandbox")  # 避免权限问题
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

        service = Service(executable_path=driver_path)
        self._driver = Edge(options=edge_options, service=service)
        self.get_driver()

    def get_driver(self):
        """
        获取驱动
        :return:
        """
        return self._driver

    def get(self, url):
        """
        打开指定url
        :param url:
        :return:
        """
        self._driver.get(url)
        self._driver.maximize_window()

    def find_element_by_xpath(self, xpath):
        """
        根据xpath查找元素，如果有多个元素，只返回第一个
        :param xpath:
        :return:
        """
        return self._driver.find_element(By.XPATH, xpath)

    @staticmethod
    def find_element_by_xpath_static(driver, xpath):
        """
        根据xpath查找元素，如果有多个元素，只返回第一个
        :param xpath:
        :return:
        """
        return driver.find_element(By.XPATH, xpath)

    @staticmethod
    def find_elements_by_xpath_static(driver, xpath):
        """
        根据xpath查找元素，返回所有元素
        :param driver:
        :param xpath:
        :return:
        """
        return driver.find_elements(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath):
        """
        根据xpath查找元素，返回所有元素
        :param xpath:
        :return:
        """
        return self._driver.find_elements(By.XPATH, xpath)

    def find_element(self, id):
        """
        根据id查找元素，如果有多个元素，只返回第一个
        :param id:
        :return:
        """
        return self._driver.find_element(value=id)

    class XpathGenerator:
        """
        XPath生成器
        """

        __xpath = ""

        @staticmethod
        def reset():
            """重置 XPath"""
            AutomationUtils.XpathGenerator.__xpath = ""
            return AutomationUtils.XpathGenerator

        @staticmethod
        def add(path: str):
            """添加路径"""
            AutomationUtils.XpathGenerator.__xpath += path
            return AutomationUtils.XpathGenerator

        @staticmethod
        def descendant_of_all(tag: str = "*"):
            """选择后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"//{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def this_descendant(tag: str = "*"):
            """选择当前元素的后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"./{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def descendant_from_parent(tag: str = "*"):
            """选择根元素的后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"/{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def attribute(name: str, value: str, contains: bool = False):
            """根据属性选择"""
            if contains:
                AutomationUtils.XpathGenerator.__xpath += f"[contains(@{name}, '{value}')]"
            else:
                AutomationUtils.XpathGenerator.__xpath += f"[@{name}='{value}']"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def text(value: str, contains: bool = False):
            """选择包含特定文本的元素"""
            if contains:
                AutomationUtils.XpathGenerator.__xpath += f"[contains(text(), '{value}')]"
            else:
                AutomationUtils.XpathGenerator.__xpath += f"[text()='{value}']"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def index(n: int):
            """选择第n个元素"""
            AutomationUtils.XpathGenerator.__xpath += f"[{n}]"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def parent():
            """选择父元素"""
            AutomationUtils.XpathGenerator.__xpath += "/.."
            return AutomationUtils.XpathGenerator

        @staticmethod
        def or_condition(condition: str):
            """添加 OR 条件"""
            AutomationUtils.XpathGenerator.__xpath += f" | {condition}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def get() -> str:
            """获取生成的 XPath"""
            xpath = AutomationUtils.XpathGenerator.__xpath
            AutomationUtils.XpathGenerator.reset()  # 自动重置
            return xpath

    # class WebAutomation:
    #     def __init__(self):
    #         self.browser = None
    #         self.page = None
    #         self.requests = []
    #
    #     def setup(self, base_url, debug=False):
    #         loop = asyncio.get_event_loop()
    #         if loop.is_closed():
    #             loop = asyncio.new_event_loop()
    #             asyncio.set_event_loop(loop)
    #         self.browser = loop.run_until_complete(self._launch(base_url, debug))
    #         self.page = loop.run_until_complete(self.browser.newPage())
    #         loop.run_until_complete(self.page.setViewport({'width': 1920, 'height': 1080}))
    #         loop.run_until_complete(self.page.goto(base_url, {'waitUntil': 'networkidle0'}))
    #         return self.page
    #
    #     async def _launch(self, base_url, debug):
    #         return await launch({
    #             'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    #             'headless': not debug,
    #             'dumpio': True,
    #             'args': [
    #                 '--no-sandbox',
    #                 '--disable-setuid-sandbox',
    #                 '--start-maximized'
    #             ]
    #         })
    #
    #     def start_capture(self, debug=False, timeout=3):
    #         # 开启请求捕获
    #         if debug:
    #             # 打印捕获的请求并添加到列表中
    #             def request_interceptor(req):
    #                 self.requests.append(req)
    #                 print(req.url)
    #                 return req
    #
    #             self.page.on('request', request_interceptor)
    #         else:
    #             # 仅添加到列表中
    #             def request_interceptor(req):
    #                 self.requests.append(req)
    #                 return req
    #
    #             self.page.on('request', request_interceptor)
    #
    #         time.sleep(timeout)
    #
    #     def generate_curl(self, databag_name):
    #         cookies = self.page.cookies()
    #         cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    #
    #         curl_command = None
    #         for req in self.requests:
    #             if databag_name in req.url:
    #                 url = req.url
    #                 method = req.method
    #                 headers = req.headers
    #                 postData = req.postData
    #                 curl_command = f"curl -X {method} '{url}'"
    #                 for header, value in headers.items():
    #                     curl_command += f" \\\n  -H '{header}: {value}'"
    #                 if cookie_str:
    #                     curl_command += f" \\\n  -H 'Cookie: {cookie_str}'"
    #                 if postData:
    #                     curl_command += f" \\\n  -d '{postData}'"
    #                 break
    #         return curl_command
    #
    #     def cleanup(self):
    #         if self.browser:
    #             self.browser.close()

    class WebAutomation:
        def __init__(self):
            self.driver = None

        def setup(self, base_url, debug=False):
            edge_options = EdgeOptions()
            if not debug:
                edge_options.add_argument("--headless")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

            service = Service(executable_path=r'D:\msedgedriver.exe')
            self.driver = seleniumwire_webdriver.Edge(options=edge_options, service=service)
            self.driver.get(base_url)
            return self.driver

        def wait_to_capture(self, debug=False, timeout=3):
            # 等待一段时间以捕获请求
            time.sleep(timeout)
            # 打印捕获到的请求 URL
            if debug:
                for request in self.driver.requests:
                    print(request.url)

        def generate_curl(self, databag_name, timeout=60):
            # 获取cookies
            cookies = self.driver.get_cookies()
            cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            # 构建curl命令
            curl_command = None
            begin_time = time.time()
            while not curl_command and time.time() - begin_time < timeout:
                for entry in self.driver.requests:
                    if databag_name in entry.url:
                        print(f"Find databag {databag_name} in {entry.url}")
                        url = entry.url
                        method = entry.method
                        headers = entry.headers
                        postData = entry.body

                        curl_command = f"curl -X {method} '{url}'"
                        for header, value in headers.items():
                            curl_command += f" \\\n  -H '{header}: {value}'"
                        if cookie_str:
                            curl_command += f" \\\n  -H 'Cookie: {cookie_str}'"
                        if postData:
                            curl_command += f" \\\n  -d '{postData}'"
                        break
            return curl_command

        def get_all_requests(self):
            return self.driver.requests

        def get_all_databags_urls(self):
            urls = []
            for request in self.driver.requests:
                urls.append(request.url)
            return urls

        def cleanup(self):
            if self.driver:
                self.driver.quit()


# 示例使用
if __name__ == '__main__':
    # xpath = AutomationUtils.XpathGenerator.descendant_of_all('div').attribute('class',
    #                                                                           'upload-button sigle_button').get()
    # web_automation = AutomationUtils.WebAutomation()
    # driver = web_automation.setup('https://aiart.chuangkit.com/editor/cleartool')
    # driver.find_element(By.XPATH, xpath).click()
    # driver.find_element(By.XPATH, '//div[@class="toggle-button"]').click()
    # driver.find_element(By.XPATH, AutomationUtils.XpathGenerator.descendant_of_all('input').attribute('data-type',
    #                                                                                                   'account').get()).send_keys(
    #     '13541923084')
    # driver.find_element(By.XPATH, AutomationUtils.XpathGenerator.descendant_of_all('input').attribute('data-type',
    #                                                                                                   'password').get()).send_keys(
    #     '13541Wky@')
    # driver.find_element(By.XPATH, AutomationUtils.XpathGenerator.descendant_of_all('button').text('登录').get()).click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, xpath).click()
    # time.sleep(2)
    # file_path = r'D:\QQDownloads\Data\Tencent Files\1992541488\nt_qq\nt_data\Pic\2024-11\Ori\03fe0390ef1647de044dea5a0f8bbcd5.jpg'
    # # 写入edge浏览器弹出的资源上传对话框
    # driver.find_element(By.XPATH, AutomationUtils.XpathGenerator.descendant_of_all('input').attribute('type',
    #                                                                                                   'file').get()).send_keys(
    #     file_path)
    #
    # web_automation.wait_to_capture(timeout=10)
    # curl_command = web_automation.generate_curl("result")
    # print(curl_command)
    # web_automation.cleanup()
    # from yyyutils.crawler_utils.crawler_utils import CrawlerUtils
    #
    # print(CrawlerUtils.get_databag_code_cookies_headers_params_1(curl_command)[0])

    # # 示例使用
    # if __name__ == '__main__':
    #     # driver = AutomationUtils('D:/msedgedriver.exe')
    #     # driver.get('https://www.baidu.com')
    #     web_automation = AutomationUtils.WebAutomation()
    #     web_automation.setup(
    #         'https://aiart.chuangkit.com/editor/cleartool?utm_source=bing??aitpbqx&utm_medium=cpc&utm_campaign=?????&utm_content=?????&utm_term=?????&msclkid=214e2897ed5610a6b0cb4fa660c0bc02&handleLogin=1&loginToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJ7XCJzdGFtcFwiOjE3MzEzMDA3NzA2NjMsXCJ0ZXJtaW5hbFwiOjAsXCJ1c2VySWRcIjo5NTU3ODE0M30ifQ.konfi-vaS6JosnzqB4Lt3YYg5USmi89fbmfBbhkF9I4',
    #         debug=True)
    #     web_automation.start_capture(debug=True, timeout=5)

    # web_obj = AutomationUtils.WebAutomation()
    # driver = web_obj.setup(base_url='http://jwc.swjtu.edu.cn/vatuu/CourseAction?setAction=classroomQuery', debug=True)
    # print(web_obj.get_all_requests())
    # print(web_obj.get_all_databags_urls())
    # web_obj.wait_to_capture(debug=True, timeout=5)
    # web_obj.generate_curl('http://jwc.swjtu.edu.cn/vatuu/CourseAction')
    # web_obj.
    pass