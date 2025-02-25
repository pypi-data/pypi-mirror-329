import openpyxl
import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl.styles import Alignment
from yyyutils.data_structure_utils import DictUtils
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip
import asyncio
import re
import subprocess
import ast
from pyppeteer import launch


class CrawlerUtils:
    """
    用于爬虫的静态工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def set_excel_wrap_text(path: str, sheet_name: str = 'Sheet1', column_width: int = 50,
                            horizontal_alignment: str = 'center', vertical_alignment: str = 'center'):
        if not os.path.exists(path):
            raise FileNotFoundError("File not found")
        if not path.endswith('.xlsx'):
            raise ValueError("File is not an Excel file")
        # 打开 Excel 文件
        workbook = openpyxl.load_workbook(path)

        # 选择要操作的表格
        sheet = workbook[sheet_name]
        for column in sheet.columns:
            sheet.column_dimensions[column[0].column_letter].width = column_width
        # 遍历每行每列，并设置单元格的格式
        for row in sheet.iter_rows():
            for cell in row:
                # 设置单元格的文本换行
                cell.alignment = Alignment(wrapText=True, horizontal=horizontal_alignment, vertical=vertical_alignment)

        # 保存更改
        workbook.save(path)

    @staticmethod
    def extract_args(url):
        res = list(map(list, re.findall(r'[?,&]?(.*?=.*?)(&|$)', url)))
        res[0][0] = res[0][0].split('?')[1]
        args = [i[0] for i in res]
        if args:
            return args
        else:
            print("No args found in URL")
            return None

    @staticmethod
    def charset_finder(soup: BeautifulSoup) -> str:
        """
        找到网页的编码格式
        :param soup:
        :return:
        """
        try:
            charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})['content'].split('=')[1]
        except:
            charset = soup.find('meta', attrs={'charset': True})['charset']
        if not charset:
            print("Charset not found, using default (UTF-8)")
            charset = 'UTF-8'
        return charset

    """
    def data_formatter(data_text: str):
        data = data_text.split('\n')
        data = [d.lstrip() for d in data if d]
        data = [d.rstrip(',') for d in data if d]
        if data[0][-1] == ':':
            for i in range(len(data)):
                if data[i] and data[i][-1] == ':' and data[i + 1][-1] == ':':
                    raise ValueError("Invalid data format")
            data = {data[i][:-1]: data[i + 1] for i in range(0, len(data), 2) if data[i]}
        else:
            for d in data:
                if d and d[-1] == ':':
                    raise ValueError("Invalid data format")
            data = [i.split(': ') for i in data]
            data = {i[0]: i[1] for i in data if len(i) == 2}
        return data
    
    
    
    def value_comparer(text1: str, text2: str) -> list:
        text1 = data_formatter(text1)
        text2 = data_formatter(text2)
        if len(text1) != len(text2):
            raise ValueError("The two texts have different lengths")
        diff = []
        for key, value in text1.items():
            if text2[key] != value:
                diff.append(key)
        return diff
    
    
    def key_comparer(text1: str, text2: str) -> bool:
        text1 = data_formatter(text1)
        text2 = data_formatter(text2)
        if len(text1) != len(text2):
            print("The two texts have different lengths")
            return False
        diff_keys = []
        for key in text1.keys():
            if key not in text2.keys():
                diff_keys.append(key)
        if diff_keys:
            print("The two texts have have same length but different keys")
            print(f"Keys {diff_keys} not found in text2")
            return False
        return True
    """

    @staticmethod
    def json_to_dataframes(json_data: dict, headers: list = None, all_floors=False):
        df_list = []
        value_lists = []
        for header in headers:
            # print(header)
            value_list = DictUtils.dict_data_extractor(json_data, header)  # 包含了所有层的数据
            # print(value_list)
            floors_set = set([i[1] for i in value_list])
            if len(floors_set) > 1:
                if all_floors:
                    value_list = [i[0] for i in value_list]
                    try:
                        df_list.append(pd.DataFrame(value_list, columns=[header]))
                    except:
                        print(
                            f"数据格式错误，即将返回 {header} 当前层的数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                        value_lists.append(value_list)
                    continue
                choose_floor = input(f"现在有多层数据含有{header}，请从以下数据选择需要的层数：{floors_set} --> ")
                if choose_floor == 'all':
                    """返回该key的所有层数的数据 -> list"""
                    value_list = [i[0] for i in value_list]
                    try:
                        df_list.append(pd.DataFrame(value_list, columns=[header]))
                    except:
                        print(
                            f"数据格式错误，即将返回 {header} 当前层的数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                        value_lists.append(value_list)
                    continue
                if int(choose_floor) not in floors_set:
                    raise ValueError("Invalid floor number")
                value_list = [i[0] for i in value_list if i[1] == int(choose_floor)]
            else:
                value_list = [i[0] for i in value_list]
            try:
                df_list.append(pd.DataFrame(value_list, columns=[header]))
            except:
                print(
                    f"数据格式错误，即将返回 {header} 当前层的错误数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                value_lists.append(value_list)
        if value_lists:
            return value_lists
        df_list = pd.concat(df_list, axis=1)
        return df_list

    @staticmethod
    def extract_non_empty_from_excel(file_path):
        # 从 Excel 文件中加载数据
        df = pd.read_excel(file_path)

        result_list = []

        # 遍历每一列，提取不为空的内容到结果列表
        for col in df.columns:
            col_data = df[col].dropna().tolist()
            result_list += col_data

        return result_list

    @staticmethod
    def get_cookies_headers_by_cURL_auto(url, databag_name, driver_path="D:/msedgedriver.exe"):
        options = Options()
        service = Service(driver_path)
        options.use_chromium = True
        driver = webdriver.Edge(service=service, options=options)

        # 访问目标网页
        driver.get(url)

        # 等待页面加载完成
        time.sleep(8)

        # 打开开发者工具（F12 或 Ctrl+Shift+I）
        # 创建ActionChains对象
        actions = ActionChains(driver)

        # 模拟按下F12键
        actions.send_keys(Keys.F12).perform()
        # 等待开发者工具加载完成
        time.sleep(8)

        # 切换到Network标签页
        webdriver.ActionChains(driver).send_keys(Keys.F1).perform()  # 打开命令菜单
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys('Network').perform()  # 输入Network并选择
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()  # 确认选择

        # 刷新页面以捕获网络请求
        driver.refresh()

        # 等待网络请求捕获完成
        time.sleep(5)

        # 执行JavaScript代码，模拟右键点击并复制为cURL
        driver.execute_script("""
            // 定位到网络面板
            var networkPanel = document.querySelector('div[aria-label="Network"]');

            // 寻找具有特定名称的请求
            var targetRequestName = arguments[0]; // 从Selenium传入的请求名称
            var requests = networkPanel.querySelectorAll('.request-list-item .request-name');
            var targetRequest = null;
            for (var i = 0; i < requests.length; i++) {
                if (requests[i].textContent.includes(targetRequestName)) {
                    targetRequest = requests[i].closest('.request-list-item');
                    break;
                }
            }

            // 如果找到了请求
            if (targetRequest) {
                // 获取请求元素的尺寸和位置
                var rect = targetRequest.getBoundingClientRect();
                var x = rect.left + rect.width / 2;
                var y = rect.top + rect.height / 2;

                // 创建并触发右键点击事件
                var event = new MouseEvent('contextmenu', {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: x,
                    clientY: y
                });
                targetRequest.dispatchEvent(event);

                // 等待并点击复制为cURL菜单项
                setTimeout(() => {
                    var copyAsCurl = document.querySelector('div[aria-label="Copy as cURL"]');
                    if (copyAsCurl) {
                        copyAsCurl.click();
                    }
                }, 1000);
            }
        """, databag_name)  #

        # 等待复制操作完成
        time.sleep(2)

        # 从剪贴板中获取cURL命令（需要使用pyperclip库）
        curl_command = pyperclip.paste()
        print(curl_command)

        # 关闭浏览器
        driver.quit()

    # @staticmethod
    # async def __main(base_url, databag_name, wait_time):
    #     """
    #
    #     :param base_url: 是哪个网址
    #     :param databag_name: 是这个网址的哪个数据包
    #     :return:
    #     """
    #     browser = await launch({
    #         'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    #         'headless': True,
    #         'dumpio': True
    #     })
    #     page = await browser.newPage()
    #     await page.goto(base_url)
    #
    #     # 监听网络请求
    #     requests = []
    #     page.on('request', lambda req: requests.append(req))
    #
    #     # 等待一些时间以便捕获请求
    #     await asyncio.sleep(wait_time)  # 根据需要调整等待时间
    #
    #     # 获取 cookies
    #     cookies = await page.cookies()
    #     cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    #
    #     # 检查请求并找到特定名称的数据包
    #     for req in requests:
    #         print(req.url)
    #         if databag_name in req.url:  # 根据你的条件过滤请求
    #             url = req.url
    #             method = req.method
    #             headers = req.headers
    #             postData = req.postData  # 直接访问属性，而不是调用方法
    #
    #             # 构造 cURL 命令
    #             curl_command = f"curl -X {method} '{url}'"
    #             for header, value in headers.items():
    #                 curl_command += f" \\\n  -H '{header}: {value}'"
    #             if cookie_str:
    #                 curl_command += f" \\\n  -H 'Cookie: {cookie_str}'"
    #             if postData:
    #                 curl_command += f" \\\n  -d '{postData}'"
    #
    #             # print(curl_command)
    #             break
    #
    #     await browser.close()
    #     return curl_command
    @staticmethod
    async def __main(base_url, databag_name, wait_time, xpath_selector=None, debug=False):
        """
        :param base_url: 是哪个网址
        :param databag_name: 是这个网址的哪个数据包
        :param wait_time: 等待捕获请求的时间
        :param xpath_selector: 需要点击的按钮的 XPath 选择器，可选参数
        :return: 生成的 cURL 命令
        """
        browser = await launch({
            'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'headless': not debug,
            'dumpio': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--start-maximized'  # 添加启动参数使窗口最大化
            ]
        })

        try:
            page = await browser.newPage()
            await page.setViewport({'width': 1920, 'height': 1080})
            await page.goto(base_url, {'waitUntil': 'networkidle0'})

            # 监听网络请求
            requests = []
            page.on('request', lambda req: requests.append(req))

            # 只有当提供了xpath_selector时才执行点击操作
            if xpath_selector:
                button_handle = await page.evaluateHandle(
                    f'document.evaluate("{xpath_selector}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue')
                if button_handle:
                    await button_handle.click()  # 点击按钮
                    print(f"已点击XPath为 {xpath_selector} 的元素")
                else:
                    print(f"未找到XPath为 {xpath_selector} 的元素")

            # 等待一些时间以便捕获请求
            await asyncio.sleep(wait_time)

            # 获取 cookies
            cookies = await page.cookies()
            cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

            # 检查请求并找到特定名称的数据包
            curl_command = None
            for req in requests:
                print(f"捕获请求: {req.url}")
                if databag_name in req.url:
                    url = req.url
                    method = req.method
                    headers = req.headers
                    postData = req.postData

                    # 构造 cURL 命令
                    curl_command = f"curl -X {method} '{url}'"
                    for header, value in headers.items():
                        curl_command += f" \\\n  -H '{header}: {value}'"
                    if cookie_str:
                        curl_command += f" \\\n  -H 'Cookie: {cookie_str}'"
                    if postData:
                        curl_command += f" \\\n  -d '{postData}'"

                    break

            return curl_command

        finally:
            await browser.close()

    @staticmethod
    def __call_node_script(curl_command):
        node_script_path = 'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\crawler_utils\curl_convert.js'  # 替换为实际路径
        # 将 curl_command 作为单个字符串参数传递
        result = subprocess.run(['node', node_script_path, curl_command],
                                capture_output=True,
                                text=True,
                                encoding='utf-8')  # 使用 utf-8 编码

        if result.returncode == 0:
            code = result.stdout
            # 使用正则表达式匹配字典
            cookies_pattern = r"cookies\s*=\s*({.*?})"
            headers_pattern = r"headers\s*=\s*({.*?})"
            params_pattern = r"params\s*=\s*({.*?})"

            # 搜索代码字符串以找到匹配的字典
            cookies_match = re.search(cookies_pattern, code, re.DOTALL)
            headers_match = re.search(headers_pattern, code, re.DOTALL)
            params_match = re.search(params_pattern, code, re.DOTALL)

            # 使用 ast.literal_eval 安全地评估字符串中的字典
            cookies_dict = ast.literal_eval(cookies_match.group(1)) if cookies_match else {}
            headers_dict = ast.literal_eval(headers_match.group(1)) if headers_match else {}
            params_dict = ast.literal_eval(params_match.group(1)) if params_match else {}

            # 打印提取出的字典
            # print("Cookies 字典:", cookies_dict)
            # print("Headers 字典:", headers_dict)
            # print("Params 字典:", params_dict)
            return code, cookies_dict, headers_dict, params_dict
        else:
            print("Error:", result.stderr)

    @staticmethod
    def _call_node_script(curl_command):
        node_script_path = 'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\crawler_utils\curl_convert.js'  # 替换为实际路径
        # 将 curl_command 作为单个字符串参数传递
        result = subprocess.run(['node', node_script_path, curl_command],
                                capture_output=True,
                                text=True,
                                encoding='utf-8')  # 使用 utf-8 编码

        if result.returncode == 0:
            code = result.stdout
            # 使用正则表达式匹配字典
            cookies_pattern = r"cookies\s*=\s*({.*?})"
            headers_pattern = r"headers\s*=\s*({.*?})"
            params_pattern = r"params\s*=\s*({.*?})"

            # 搜索代码字符串以找到匹配的字典
            cookies_match = re.search(cookies_pattern, code, re.DOTALL)
            headers_match = re.search(headers_pattern, code, re.DOTALL)
            params_match = re.search(params_pattern, code, re.DOTALL)

            # 使用 ast.literal_eval 安全地评估字符串中的字典
            cookies_dict = ast.literal_eval(cookies_match.group(1)) if cookies_match else {}
            headers_dict = ast.literal_eval(headers_match.group(1)) if headers_match else {}
            params_dict = ast.literal_eval(params_match.group(1)) if params_match else {}

            # 打印提取出的字典
            # print("Cookies 字典:", cookies_dict)
            # print("Headers 字典:", headers_dict)
            # print("Params 字典:", params_dict)
            return code, cookies_dict, headers_dict, params_dict
        else:
            print("Error:", result.stderr)

    @staticmethod
    def get_databag_code_cookies_headers_params(request_url, databag_name, wait_time=5, need_save=False, xpath=None,
                                                debug=False):
        curl_command = asyncio.run(
            CrawlerUtils.__main(request_url, databag_name, wait_time, xpath_selector=xpath, debug=debug))
        python_code, cookies_dict, headers_dict, params_dict = CrawlerUtils.__call_node_script(curl_command)
        if need_save:
            with open('dictionaries.json', 'w', encoding='utf-8') as f:
                json.dump({'cookies': cookies_dict, 'headers': headers_dict, 'params': params_dict}, f,
                          ensure_ascii=False, indent=4)
        return python_code, cookies_dict, headers_dict, params_dict

    @staticmethod
    def get_databag_code_cookies_headers_params_1(curl_command, need_save=False):
        python_code, cookies_dict, headers_dict, params_dict = CrawlerUtils.__call_node_script(curl_command)
        if need_save:
            with open('dictionaries.json', 'w', encoding='utf-8') as f:
                json.dump({'cookies': cookies_dict, 'headers': headers_dict, 'params': params_dict}, f,
                          ensure_ascii=False, indent=4)
        return python_code, cookies_dict, headers_dict, params_dict

    @staticmethod
    def read_json_file(file_path) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data


if __name__ == '__main__':
    # # options = Options()
    # # service = Service("D:/msedgedriver.exe")
    # # options.use_chromium = True
    # # driver = webdriver.Edge(service=service, options=options)
    # # driver.get('https://s.weibo.com/weibo?q=%E6%95%8F%E6%84%9F%E8%AF%8D')
    # # time.sleep(2)
    # from yyyutils.auto_utils.auto.automation_utils import AutomationUtils
    #
    # xpath = AutomationUtils.XpathGenerator.descendant_of_all('div').attribute('class',
    #                                                                           'upload-button sigle_button').get()
    # code, cookies_dict, headers_dict, params_dict = CrawlerUtils.get_databag_code_cookies_headers_params(
    #     'https://aiart.chuangkit.com/editor/cleartool?utm_source=bing??aitpbqx&utm_medium=cpc&utm_campaign=?????&utm_content=?????&utm_term=?????&msclkid=214e2897ed5610a6b0cb4fa660c0bc02&handleLogin=1&loginToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJ7XCJzdGFtcFwiOjE3MzEzMDA3NzA2NjMsXCJ0ZXJtaW5hbFwiOjAsXCJ1c2VySWRcIjo5NTU3ODE0M30ifQ.konfi-vaS6JosnzqB4Lt3YYg5USmi89fbmfBbhkF9I4',
    #     'https://aigc-pri-prod-cdn-oss.chuangkit.com/aigc/api_image_result/', wait_time=3, debug=True,
    #     xpath=xpath)
    # print(cookies_dict)
    # print(headers_dict)
    # print(params_dict)
    print(CrawlerUtils._call_node_script("""curl -X GET 'https://aigc-pri-prod-cdn-oss.chuangkit.com/aigc/api_image_result/20241113/4784330.png?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDXEtSsCVfdVHyhFm7EKLSRGuLZZx84mHb%26q-sign-time%3D1731502679%3B1731718679%26q-key-time%3D1731502679%3B1731718679%26q-header-list%3Dhost%26q-url-param-list%3D%26q-signature%3Df63380740137160797c5838a09cdc54aa82d459d' \
  -H 'origin: https://aiart.chuangkit.com' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0' \
  -H 'sec-ch-ua: "Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: image' \
  -H 'referer: https://aiart.chuangkit.com/' \
  -H 'accept-encoding: gzip, deflate, br, zstd' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'priority: i' \
  -H 'Cookie: 8c9191eb6b6b4d07_gr_cs1=95756322; 8c9191eb6b6b4d07_gr_last_sent_cs1=95756322; 8c9191eb6b6b4d07_gr_last_sent_sid_with_cs1=409ad2b6-c935-4847-92b2-2f60804c58e8; _ga_N3TGXKV4RJ=GS1.2.1731502666.1.0.1731502666.0.0.0; ckt_login=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJ7XCJzdGFtcFwiOjE3MzE1MDI2NjU5MzgsXCJ0ZXJtaW5hbFwiOjAsXCJ1c2VySWRcIjo5NTc1NjMyMn0ifQ.xuXmkaWrUS5jMSthSB-4sbXTsorDdeZQlSP9FRy4m04; _gid=GA1.2.1810503611.1731502665; Hm_lpvt_5344b558457018b9f67f8372a8214151=1731502664; HMACCOUNT=A8F84366F47476A1; _gat_UA-122218671-1=1; Hm_lvt_5344b558457018b9f67f8372a8214151=1731502664; 8c9191eb6b6b4d07_gr_session_id_sent_vst=409ad2b6-c935-4847-92b2-2f60804c58e8; _ga=GA1.2.1124043839.1731502665; 8c9191eb6b6b4d07_gr_session_id=409ad2b6-c935-4847-92b2-2f60804c58e8; SEC_SESSION=71CBFEF670EC3926E695D135212A155A; gr_user_id=e5fe52b2-bfaa-4186-92ac-3caacd700618'"""))