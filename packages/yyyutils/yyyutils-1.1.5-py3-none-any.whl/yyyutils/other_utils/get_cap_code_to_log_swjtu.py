"""
获取验证码图片
"""
import requests
import cv2
import numpy as np
import time
import pytesseract
from PIL import Image

JSESSIONID = ''
USERNAME = ''


def get_cap_img():
    cookies = {
        'username': USERNAME,
        'JSESSIONID': JSESSIONID,
        'Hm_lvt_87cf2c3472ff749fe7d2282b7106e8f1': '1719645339',
        'Hm_lpvt_87cf2c3472ff749fe7d2282b7106e8f1': '1719645339',
    }

    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'username=2022110080; JSESSIONID=2FF5DD248083489C415AA861F651BF76; Hm_lvt_87cf2c3472ff749fe7d2282b7106e8f1=1719462160,1719474159,1719545608,1719639500; Hm_lpvt_87cf2c3472ff749fe7d2282b7106e8f1=1719640056',
        'Pragma': 'no-cache',
        'Referer': 'http://jwc.swjtu.edu.cn/service/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

    params = {
        'test': str(int(time.time() * 1000))
    }
    # print(params)
    response = requests.get(
        'http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    with open('cap.jpg', 'wb') as f:
        f.write(response.content)


def get_cap_code():
    while True:
        time.sleep(1)
        get_cap_img()
        res = True

        # 读取验证码图片
        image = cv2.imread('cap.jpg')
        # 裁剪左边的边缘和上边的边缘
        image = image[2:100, 1:100]
        import copy
        image = copy.deepcopy(image)

        # 转换为灰度图像
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 自适应阈值二值化处理
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        # 进一步去除小的白点噪声
        image = cv2.medianBlur(image, 1)
        # 去除噪点，通过形态学操作
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        # 锐化处理
        kernel = np.array([[-1, -1, -1], [-1, 11, -1], [-1, -1, -1]])
        image = cv2.filter2D(image, -1, kernel)

        # 将处理后的图像保存为 'processed_image.png'
        cv2.imwrite('processed_image.png', image)
        print("处理后的图片已保存为 processed_image.png", flush=True)

        # 使用 pytesseract 进行 OCR 识别
        pil_image = Image.fromarray(image)

        # Tesseract OCR 配置只提取字母
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # 获取详细数据
        text_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT, config=custom_config)
        text = text_data['text']
        confidences = text_data['conf']
        print("识别结果:", text, flush=True)
        print("置信度:", confidences, flush=True)

        recognized_text = ''
        text_confidence_dict = {}

        # 填入文本
        for i in range(len(text)):
            if text[i] and len(text[i]) != 4:
                res = False
                break
            if text[i]:
                text_confidence_dict[text[i]] = confidences[i]

        if not res or not text_confidence_dict:
            print('验证码识别缺失', flush=True)
            continue

        for k, v in text_confidence_dict.items():
            print(k, v, flush=True)
            if v > 60:
                recognized_text += k
            else:
                res = False
                break

        if res and len(recognized_text) == 4:
            return recognized_text
        else:
            print('未能识别完整的四个字母验证码，继续尝试', flush=True)


