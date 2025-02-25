# import pdfplumber
# from yyyutils.math_utils.math_utils import MathUtils
# from reportlab.pdfgen import canvas
# import fitz
#
#
# class PDF工具箱:
#     def __init__(self, 要打开用于读取的PDF路径=None, 要打开用于写入的PDF路径=None):
#         self.要打开的PDF路径 = 要打开用于读取的PDF路径
#         if 要打开用于读取的PDF路径 is not None:
#             self.用于读取的PDF_plb = pdfplumber.open(要打开用于读取的PDF路径)
#             self.用于读取的PDF_fitz = fitz.open(要打开用于读取的PDF路径)
#         if 要打开用于写入的PDF路径 is not None:
#             self.用于写入的PDF = fitz.open(要打开用于写入的PDF路径)
#
#     def 创建新的PDF(self, 要创建的PDF路径):
#         c = canvas.Canvas(要创建的PDF路径)
#         c.save()
#         return c
#
#     def 获取页面迭代器(self) -> pdfplumber.page.Page:
#         return self.用于读取的PDF.pages
#
#     def 获取第n页(self, n: int) -> pdfplumber.page.Page:
#         return self.用于读取的PDF.pages[n - 1]
#
#     def 获取当前页面的所有下划线对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有下划线对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.lines
#
#     def 获取当前页面的所有行对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有行对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.extract_text_lines()
#
#     def 获取当前页面的以空格分割的所有单词对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有单词对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.extract_words()
#
#     def 获取当前页面的所有文字内容(self, page: pdfplumber.page.Page) -> str:
#         """
#         获取当前页面中的所有文字内容
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.extract_text()
#
#     def 无格式获取当前页面的所有文字内容(self, page: pdfplumber.page.Page) -> str:
#         """
#         获取当前页面中的所有文字内容，无格式
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.extract_text_simple()
#
#     def 获取当前页面的所有字符对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有字符对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.chars
#
#     def 获取当前页面的所有矩形对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有矩形对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.rects
#
#     def 获取当前页面的所有图像对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有图像对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.images
#
#     def 获取当前页面的所有曲线对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有曲线对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.curves
#
#     def 获取当前页面的所有注释对象(self, page: pdfplumber.page.Page) -> list:
#         """
#         获取当前页面中的所有注释对象
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.annots
#
#     def 获取当前页面的宽度(self, page: pdfplumber.page.Page) -> float:
#         """
#         获取当前页面的宽度
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.width
#
#     def 获取当前页面的高度(self, page: pdfplumber.page.Page) -> float:
#         """
#         获取当前页面的高度
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.height
#
#     def 获取当前页面的尺寸(self, page: pdfplumber.page.Page) -> tuple:
#         """
#         获取当前页面的尺寸
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.width, page.height
#
#     def 获取当前页面的页码(self, page: pdfplumber.page.Page) -> int:
#         """
#         获取当前页面的页码
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#         return page.page_number
#
#     def 获取当前页面的PDF对象(self) -> pdfplumber.pdf.PDF:
#         """
#         获取当前PDF对象
#         :return:
#         """
#         return self.用于读取的PDF
#
#     def 提取对象的xy坐标(self, obj_dict) -> tuple:
#         """
#         提取对象的xy坐标，以(x0,x1,y0,y1)的形式返回
#         其中x0是对象左边界到页面左边界的距离，x1是对象右边界到页面左边界的距离，y0是对象下边界到页面下边界的距离，y1是对象上边界到页面下边界的距离
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             x0, y0, x1, y1 = obj_dict['x0'], obj_dict['x1'], obj_dict['y0'], obj_dict['y1']
#             return x0, y0, x1, y1
#         except:
#             print("提取对象的xy坐标失败")
#             return None
#
#     def 提取对象的高度和宽度(self, obj_dict) -> tuple:
#         """
#         提取对象的高度和宽度，以(height,width)的形式返回
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             height, width = obj_dict['height'], obj_dict['width']
#             return height, width
#         except:
#             print("提取对象的高度和宽度失败")
#             return None
#
#     def 计算对象中心点坐标(self, obj_dict) -> tuple:
#         """
#         计算对象中心点坐标，以(x,y)的形式返回
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             x0, y0, x1, y1 = self.提取对象的xy坐标(obj_dict)
#             x = (x0 + x1) / 2
#             y = (y0 + y1) / 2
#             return x, y
#         except:
#             print("计算对象中心点坐标失败")
#             return None
#
#     def 提取对象的颜色(self, obj_dict) -> tuple:
#         """
#         提取对象的颜色，以(r,g,b)的形式返回
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             r, g, b = obj_dict['color']
#             return r, g, b
#         except:
#             print("提取对象的颜色失败")
#             return None
#
#     def 提取对象的文本内容(self, obj_dict) -> str:
#         """
#         提取对象的文本内容
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             return obj_dict['text']
#         except:
#             print("提取对象的文本内容失败")
#             return None
#
#     def 提取对象的字体和字体大小(self, obj_dict) -> tuple:
#         """
#         提取对象的字体和字体大小，以(font,size)的形式返回
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             font, size = obj_dict['fontname'], obj_dict['size']
#             return font, size
#         except:
#             print("提取对象的字体和字体大小失败")
#             return None
#
#     def 提取对象所在页面的页码(self, obj_dict) -> int:
#         """
#         提取对象所在页面的页码
#         :param obj_dict: pdfplumber.utils.obj_dictect对象
#         :return:
#         """
#         try:
#             return obj_dict['chars'][0]['page_number']
#         except:
#             print("提取对象所在页面的页码失败")
#             return None
#
#     def 提取某一行中下划线上方的文本内容(self, text_line_dict):
#         """
#         提取下划线上方的文本内容
#         :param line: pdfplumber.utils.Line对象
#         :return:
#         """
#         x0, y0, x1, y1, page_number = text_line_dict['x0'], text_line_dict['top'], text_line_dict['x1'], text_line_dict[
#             'bottom'], text_line_dict['chars'][0]['page_number']
#         text = text_line_dict['text']
#         all_lines = self.用于读取的PDF.pages[page_number - 1].lines
#         for line in all_lines:
#             if MathUtils.a近似大于等于b减去容忍度(line['x0'], x0, 1) and MathUtils.a近似小于等于b加上容忍度(
#                     line['x1'], x1, 1) and MathUtils.两个数近似相等(line['top'], y1, 5):
#                 lx0, lx1 = line['x0'], line['x1']
#                 len_text = len(text)
#                 len_word = (x1 - x0) / len_text
#                 每个字的起始位置 = []
#                 每个字的终止位置 = []
#                 for i, W in enumerate(text):
#                     start = MathUtils.linear_interpolate(0, len_text - 1, x0, x1 - len_word, i)
#                     end = start + len_word
#                     每个字的起始位置.append(start)
#                     每个字的终止位置.append(end)
#                 起始差值 = [abs(start - lx0) for start in 每个字的起始位置]
#                 终止差值 = [abs(end - lx1) for end in 每个字的终止位置]
#                 # 找到最小值的索引
#                 起始字符索引 = 起始差值.index(min(起始差值))
#                 终止字符索引 = 终止差值.index(min(终止差值))
#                 # 提取答案
#                 答案 = text[起始字符索引:终止字符索引 + 1]
#                 return 答案
#         return None
#
#     def 提取高亮文本(self, page: int):
#         """
#         提取高亮文本
#         :param page: pdfplumber.page.Page对象
#         :return:
#         """
#
#         def __提取高亮文本(page, points):
#             rect = fitz.Rect(points[0], points[-1])  # 创建矩形区域
#             highlight_text = page.get_text("text", clip=rect)
#             if highlight_text.strip():  # 确保文本不为空
#                 return highlight_text
#             else:
#                 print("高亮区域内无文本")
#                 return None
#
#         def __调整结果的顺序(result_with_leftoppoints):
#             if not result_with_leftoppoints:
#                 print("未找到高亮文本")
#                 return []
#             result = []
#             # 根据左上角坐标排序，先比较上坐标，上坐标越小，说明越靠上，靠上的排在前面，如果上坐标相同，则比较左坐标，左坐标越小，说明越靠左
#             result_with_leftoppoints.sort(key=lambda x: (x[1][1], x[1][0]))
#             # 直接提取出文本
#             for text, leftup in result_with_leftoppoints:
#                 result.append(text)
#             return result
#
#         result_with_leftoppoints = []
#         page = self.用于读取的PDF_fitz[page - 1]
#         annots = page.annots()
#         if annots:
#             for annot in annots:
#                 if annot.type[0] == 8:
#                     positions = annot.vertices
#                     # 将positions按四个元组的形式划分为列表，每个列表代表一个矩形区域
#                     positions = [positions[i:i + 4] for i in range(0, len(positions), 4)]
#                     highlight_text = ''
#                     for i, position in enumerate(positions):
#                         highlight_text += __提取高亮文本(page, position).strip()
#                         if highlight_text and i == len(positions) - 1:
#                             result_with_leftoppoints.append((highlight_text, position[0]))
#         result = __调整结果的顺序(result_with_leftoppoints)
#         return result
#
#     def 在PDF的指定位置写入文本(self, 文本内容, 位置, 字体大小=12, 字体='宋体', 颜色=(0, 0, 0)):
#         page_number, x0, x1, y0, y1 = 位置
#         rect = fitz.Rect(x0, y0, x1, y1)
#         self.用于写入的PDF[page_number].insertText(rect, 文本内容, fontname=字体, fontsize=字体大小, color=颜色)
#         self.用于写入的PDF.save()
#
#
# if __name__ == '__main__':
#     PDF工具箱 = PDF工具箱(要打开用于读取的PDF路径=r'D:\Python\Python38\Lib\site-packages\mytools\习概总结提纲.pdf')
#     # PDF工具箱.在PDF的指定位置写入文本('你好，世界！', (1, 100, 130, 100, 150))
#     print(PDF工具箱.提取高亮文本(1))
"""
TODO:
1.
"""

import pdfplumber
from yyyutils.math_utils.math_utils import MathUtils
from reportlab.pdfgen import canvas
import fitz
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.pagesizes import A4
import os


class PDF工具箱:
    def __init__(self, 用于读取的PDF路径=None, 用于写入的PDF路径=None):
        self.用于读取的PDF路径 = 用于读取的PDF路径
        self.用于写入的PDF路径 = 用于写入的PDF路径
        if 用于读取的PDF路径 is not None:
            self.用于读取的PDF_plb = pdfplumber.open(用于读取的PDF路径)
            self.用于读取的PDF_fitz = fitz.open(用于读取的PDF路径)
        if 用于写入的PDF路径 is not None:
            self.用于写入的PDF = fitz.open(用于写入的PDF路径)

    def 创建新的PDF(self, 要创建的PDF路径, page_size: tuple = None, 初始化操作=None):
        """
        创建一个新的空白PDF文件，并在创建后执行初始化操作
        :param 要创建的PDF路径: 新PDF文件的路径
        :param page_size: 页面大小，默认为A4
        :param 初始化操作: 创建canvas对象后要执行的操作，可以是函数或lambda表达式
        """
        if page_size is None:
            page_size = A4
        c = canvas.Canvas(要创建的PDF路径, pagesize=page_size)
        if 初始化操作:
            初始化操作(c)
        c.save()
        return c

    def 获取页面迭代器(self):
        """
        获取页面迭代器，每次迭代返回一个整数页数，不是pdfplumber.page.Page对象
        :return:
        """
        return range(1, len(self.用于读取的PDF_plb.pages) + 1)

    def 获取读取PDF的第n页(self, n: int) -> pdfplumber.page.Page:
        return self.用于读取的PDF_plb.pages[n - 1]

    def 获取写入PDF的第n页(self, n: int) -> fitz.Page:
        return self.用于写入的PDF[n - 1]

    def 获取当前页面的所有下划线对象(self, n: int) -> list:
        """
        获取当前页面中的所有下划线对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.lines

    def 获取当前页面的所有行对象(self, n: int) -> list:
        """
        获取当前页面中的所有行对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.extract_text_lines()

    def 获取当前页面的以空格分割的所有单词对象(self, n: int) -> list:
        """
        获取当前页面中的所有单词对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.extract_words()

    def 获取当前页面的所有文字内容(self, n: int) -> str:
        """
        获取当前页面中的所有文字内容
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.extract_text()

    def 无格式获取当前页面的所有文字内容(self, n: int) -> str:
        """
        获取当前页面中的所有文字内容，无格式
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.extract_text_simple()

    def 获取当前页面的所有字符对象(self, n: int) -> list:
        """
        获取当前页面中的所有字符对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.chars

    def 获取当前页面的所有矩形对象(self, n: int) -> list:
        """
        获取当前页面中的所有矩形对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.rects

    def 获取当前页面的所有图像对象(self, n: int) -> list:
        """
        获取当前页面中的所有图像对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.images

    def 获取当前页面的所有曲线对象(self, n: int) -> list:
        """
        获取当前页面中的所有曲线对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.curves

    def 获取当前页面的所有注释对象(self, n: int) -> list:
        """
        获取当前页面中的所有注释对象
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.annots

    def 获取当前页面的宽度(self, n: int) -> float:
        """
        获取当前页面的宽度
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.width

    def 获取当前页面的高度(self, n: int) -> float:
        """
        获取当前页面的高度
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.height

    def 获取当前页面的尺寸(self, n: int) -> tuple:
        """
        获取当前页面的尺寸
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.width, page.height

    def 获取当前页面的页码(self, n: int) -> int:
        """
        获取当前页面的页码
        :param n: 页码
        """
        page = self.获取读取PDF的第n页(n)
        return page.page_number

    def 获取当前页面的PDF对象(self) -> pdfplumber.pdf.PDF:
        """
        获取当前PDF对象
        """
        return self.用于读取的PDF_plb

    def 提取对象的xy坐标(self, obj_dict) -> tuple:
        """
        提取对象的xy坐标，以(x0,x1,y0,y1)的形式返回
        其中x0是对象左边界到页面左边界的距离，x1是对象右边界到页面左边界的距离，y0是对象下边界到页面下边界的距离，y1是对象上边界到页面下边界的距离
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            x0, y0, x1, y1 = obj_dict['x0'], obj_dict['x1'], obj_dict['y0'], obj_dict['y1']
            return x0, y0, x1, y1
        except:
            print("提取对象的xy坐标失败")
            return None

    def 提取对象的高度和宽度(self, obj_dict) -> tuple:
        """
        提取对象的高度和宽度，以(height,width)的形式返回
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            height, width = obj_dict['height'], obj_dict['width']
            return height, width
        except:
            print("提取对象的高度和宽度失败")
            return None

    def 计算对象中心点坐标(self, obj_dict) -> tuple:
        """
        计算对象中心点坐标，以(x,y)的形式返回
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            x0, y0, x1, y1 = self.提取对象的xy坐标(obj_dict)
            x = (x0 + x1) / 2
            y = (y0 + y1) / 2
            return x, y
        except:
            print("计算对象中心点坐标失败")
            return None

    def 提取对象的颜色(self, obj_dict) -> tuple:
        """
        提取对象的颜色，以(r,g,b)的形式返回
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            r, g, b = obj_dict['color']
            return r, g, b
        except:
            print("提取对象的颜色失败")
            return None

    def 提取对象的文本内容(self, obj_dict) -> str:
        """
        提取对象的文本内容
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            return obj_dict['text']
        except:
            print("提取对象的文本内容失败")
            return None

    def 提取对象的字体和字体大小(self, obj_dict) -> tuple:
        """
        提取对象的字体和字体大小，以(font,size)的形式返回
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            font, size = obj_dict['fontname'], obj_dict['size']
            return font, size
        except:
            print("提取对象的字体和字体大小失败")
            return None

    def 提取对象所在页面的页码(self, obj_dict) -> int:
        """
        提取对象所在页面的页码
        :param obj_dict: pdfplumber.utils.obj_dictect对象
        :return:
        """
        try:
            return obj_dict['chars'][0]['page_number']
        except:
            print("提取对象所在页面的页码失败")
            return None

    def 提取某一行中下划线上方的文本内容(self, text_line_dict, n: int):
        """
        提取下划线上方的文本内容
        :param text_line_dict: pdfplumber.utils.Line对象
        :param n: 页码
        :return:
        """
        x0, y0, x1, y1, page_number = text_line_dict['x0'], text_line_dict['top'], text_line_dict['x1'], text_line_dict[
            'bottom'], text_line_dict['chars'][0]['page_number']
        text = text_line_dict['text']
        all_lines = self.获取读取PDF的第n页(page_number).lines
        for line in all_lines:
            if MathUtils.a近似大于等于b减去容忍度(line['x0'], x0, 1) and MathUtils.a近似小于等于b加上容忍度(
                    line['x1'], x1, 1) and MathUtils.两个数近似相等(line['top'], y1, 5):
                lx0, lx1 = line['x0'], line['x1']
                len_text = len(text)
                len_word = (x1 - x0) / len_text
                每个字的起始位置 = []
                每个字的终止位置 = []
                for i, W in enumerate(text):
                    start = MathUtils.linear_interpolate(0, len_text - 1, x0, x1 - len_word, i)
                    end = start + len_word
                    每个字的起始位置.append(start)
                    每个字的终止位置.append(end)
                起始差值 = [abs(start - lx0) for start in 每个字的起始位置]
                终止差值 = [abs(end - lx1) for end in 每个字的终止位置]
                # 找到最小值的索引
                起始字符索引 = 起始差值.index(min(起始差值))
                终止字符索引 = 终止差值.index(min(终止差值))
                # 提取答案
                答案 = text[起始字符索引:终止字符索引 + 1]
                return 答案
        return None

    def 提取高亮文本(self, page: int):
        """
        提取高亮文本
        :param page: 页码
        :return:
        """

        def __提取高亮文本(page, points):
            rect = fitz.Rect(points[0], points[-1])  # 创建矩形区域
            highlight_text = page.get_text("text", clip=rect)
            if highlight_text.strip():  # 确保文本不为空
                return highlight_text
            else:
                print("高亮区域内无文本")
                return None

        def __调整结果的顺序(result_with_leftoppoints):
            if not result_with_leftoppoints:
                print("未找到高亮文本")
                return []
            result = []
            # 根据左上角坐标排序，先比较上坐标，上坐标越小，说明越靠上，靠上的排在前面，如果上坐标相同，则比较左坐标，左坐标越小，说明越靠左
            result_with_leftoppoints.sort(key=lambda x: (x[1][1], x[1][0]))
            # 直接提取出文本
            for text, leftup in result_with_leftoppoints:
                result.append(text)
            return result

        result_with_leftoppoints = []
        page = self.用于读取的PDF_fitz[page - 1]
        annots = page.annots()
        if annots:
            for annot in annots:
                if annot.type[0] == 8:
                    positions = annot.vertices
                    # 将positions按四个元组的形式划分为列表，每个列表代表一个矩形区域
                    positions = [positions[i:i + 4] for i in range(0, len(positions), 4)]
                    highlight_text = ''
                    for i, position in enumerate(positions):
                        highlight_text += __提取高亮文本(page, position).strip()
                        if highlight_text and i == len(positions) - 1:
                            # highlight_text = highlight_text.strip()
                            result_with_leftoppoints.append((highlight_text, position[0]))
        result = __调整结果的顺序(result_with_leftoppoints)
        return result

    def _是否是英文字母(self, char):
        return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

    def _是否是英文字母字符串(self, text):
        return all(self._是否是英文字母(char) for char in text)

    def 提取判断答案(self, page: int, symbol_list: list = None):
        """
        提取判断答案
        :param page:
        :param symbol_list:
        :return:
        """
        if not symbol_list:
            # '是', '否', '对', '错', '真', '假', '正确', '错误', 'F', 'T', 'Y', 'N',, 'X', 'x'
            symbol_list = ['√', '×', '✔', '✗']
        page = self.获取读取PDF的第n页(page)
        text = page.extract_text_simple().strip()
        result = []
        for i, char in enumerate(text):
            if char in symbol_list:
                result.append(char)
        return result

    def 提取括号内的文本(self, page: int,
                         bracket_style: list = None,
                         clear_text=True, letter_only=False, number_only=False, true_false_only=False) -> list:
        """
        提取指定页面中所有括号内的文本
        :param page: 页码
        :param bracket_style: 包含括号样式的列表，每个元素是一个元组，表示一对括号
        :param clear_text: 是否清除文本中的空格和换行符
        :return: 包含所有括号内文本的列表
        """
        if not bracket_style:
            all_left_brackets = ['（', '(', '【', '[', '{']
            all_right_brackets = ['）', ')', '】', ']', '}']
            bracket_style = [(left, right) for left in all_left_brackets for right in all_right_brackets]
        page = self.获取读取PDF的第n页(page)
        text = page.extract_text_simple().strip()
        stack = []
        result = []

        for i, char in enumerate(text):
            for left, right in bracket_style:
                if char == left:
                    stack.append((i, left, right))
                elif char == right:
                    if stack:
                        last = stack.pop()
                        if last[2] == char:
                            start_index = last[0] + 1
                            end_index = i
                            if end_index > start_index:
                                if clear_text:
                                    res = text[start_index:end_index].strip().replace('\n', '').replace(' ', '')
                                else:
                                    res = text[start_index:end_index]
                                result.append(res)
        if letter_only:
            result = [text for text in result if self._是否是英文字母字符串(text)]
        elif number_only:
            result = [text for text in result if text.isdigit()]
        elif true_false_only:
            # '是', '否', '对', '错', '真', '假', '正确', '错误', 'F', 'T', 'Y', 'N','X', 'x'
            symbols = ['√', '×', '✔', '✗']
            result = [text for text in result if text in symbols]
        return result

    def 删除括号内的文本(self, page: int, bracket_style: list = None, letter_only=False, number_only=False,
                         True_false_only=False, output_pdf_path=None) -> None:
        """
        删除指定页面中所有括号内的文本，保留括号
        :param page: 页码
        :param bracket_style: 包含括号样式的列表，每个元素是一个元组，表示一对括号
        :param letter_only: 是否只删除字母
        :param number_only: 是否只删除数字
        :return: None
        """
        if not bracket_style:
            all_left_brackets = ['（', '(', '【', '[', '{']
            all_right_brackets = ['）', ')', '】', ']', '}']
            bracket_style = [(left, right) for left in all_left_brackets for right in all_right_brackets]

        page_obj = self.获取写入PDF的第n页(page)
        page_rect = page_obj.rect
        width, height = page_rect.width, page_rect.height
        text_blocks = page_obj.get_text("blocks")

        def 删除文本中的括号内容(text):
            modified_text = text
            for left, right in bracket_style:
                start_pos = 0
                while True:
                    # 查找左括号
                    left_idx = modified_text.find(left, start_pos)
                    if left_idx == -1:
                        break

                    # 查找对应的右括号
                    right_idx = modified_text.find(right, left_idx)
                    if right_idx == -1:
                        break

                    # 检查括号内的内容
                    bracket_content = modified_text[left_idx + 1:right_idx]
                    should_delete = False

                    if letter_only:
                        should_delete = all(
                            self._是否是英文字母(char) for char in bracket_content if not char.isspace())
                    elif number_only:
                        should_delete = all(char.isdigit() for char in bracket_content if not char.isspace())
                    elif True_false_only:
                        # '是', '否', '对', '错', '真', '假', '正确', '错误', 'F', 'T', 'Y', 'N','X', 'x'
                        symbols = ['√', '×', '✔', '✗']
                        should_delete = all(char in symbols for char in bracket_content if not char.isspace())
                    else:
                        should_delete = True

                    if should_delete:
                        # 保留括号，只删除内容
                        modified_text = modified_text[:left_idx + 1] + modified_text[right_idx:]
                        start_pos = right_idx + 1
                    else:
                        start_pos = right_idx + 1

            return modified_text

        def 临时文件初始化操作(c):
            # 注册宋体
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            # Windows系统宋体路径
            simsun_path = "C:/Windows/Fonts/simsun.ttc"

            # 注册宋体
            pdfmetrics.registerFont(TTFont('simsun', simsun_path))

            # 设置宋体和字号
            c.setFont("simsun", 12)

            # 处理每个文本块
            for block in text_blocks:
                # 获取文本块的位置和内容
                x, y, x1, y1, text, block_no, block_type = block

                # 删除括号内的文本
                modified_text = 删除文本中的括号内容(text)

                # 绘制文本块
                c.drawString(x, height - y, modified_text.strip())

        output_path = output_pdf_path or 'output.pdf'
        temp_pdf = 'temp.pdf'
        self.创建新的PDF(temp_pdf, page_size=(width, height), 初始化操作=临时文件初始化操作)

        new_doc = fitz.open()
        # 复制原PDF中的其他页面
        for i in range(self.用于写入的PDF.page_count):
            if i != page - 1:
                new_doc.insert_pdf(self.用于写入的PDF, from_page=i, to_page=i)
            else:
                # 插入修改后的页面
                temp_doc = fitz.open(temp_pdf)
                new_doc.insert_pdf(temp_doc)
                temp_doc.close()

        new_doc.save(output_path)
        new_doc.close()
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)

    # def add_text_to_page(self, page_number, new_text):
    #     page = self.用于写入的PDF[page_number - 1]
    #
    #     # 1. 确保使用正确的字体
    #     font = "china-s"  # 使用内置字体
    #
    #     # 2. 获取页面尺寸并留出边距
    #     margin = 0  # 页面边距
    #     textbox_rect = fitz.Rect(
    #         margin,  # left
    #         margin,  # top
    #         page.rect.width - margin,  # right
    #         page.rect.height - margin  # bottom
    #     )
    #
    #     # 3. 插入文本，添加更多参数以便调试
    #     rc = page.insert_textbox(
    #         textbox_rect,
    #         new_text,
    #         fontname=font,
    #         fontsize=6.8,
    #         align=fitz.TEXT_ALIGN_LEFT,  # 文本对齐方式
    #         color=(0, 0, 0),  # 黑色文本
    #         stroke_opacity=1,
    #         fill_opacity=1
    #     )
    #
    #     # 4. 检查返回值
    #     if rc >= 0:
    #         print(f"成功插入文本，剩余未使用空间：{rc}")
    #     else:
    #         print("插入文本失败，文本框可能太小")
    #
    #     self.用于写入的PDF.save("output.pdf")

    def 在PDF的指定位置写入文本(self, 文本内容, 位置, 字体大小=12, 字体='宋体', 颜色=(0, 0, 0)):
        page_number, x0, x1, y0, y1 = 位置
        rect = fitz.Rect(x0, y0, x1, y1)
        self.用于写入的PDF[page_number].insertText(rect, 文本内容, fontname=字体, fontsize=字体大小, color=颜色)
        self.用于写入的PDF.save()

    def 新建PDF并写入文本(self, 要创建的PDF路径, 文本列表):

        # 注册中文字体(这里使用系统自带的宋体，根据实际情况修改路径)
        pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc'))

        # 创建文档
        doc = SimpleDocTemplate(
            要创建的PDF路径,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # 创建样式
        style = ParagraphStyle(
            'CustomStyle',
            fontName='SimSun',
            fontSize=12,
            leading=20,  # 行间距
            spaceAfter=8  # 段落间距
        )

        # 将文本转换为段落对象
        story = []
        for text in 文本列表:
            p = Paragraph(text, style)
            story.append(p)

        # 生成PDF
        doc.build(story)

    def 清空某页的所有内容(self, page: int):
        """
        清空某页的所有内容
        :param page: 页码
        :return: None
        """
        self.用于写入的PDF.delete_page(page - 1)
        self.用于写入的PDF.insert_page(page - 1)

        self.用于写入的PDF.save(r'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\clear_bracket_output.pdf')


# if __name__ == '__main__':
#     # 提取判断题答案
#     用于读取的PDF = input('请输入要读取的PDF路径：')
#     PDF工具箱 = PDF工具箱(用于读取的PDF路径=用于读取的PDF)
#     起始页码 = int(input('请输入起始页码：'))
#     结束页码 = int(input('请输入结束页码：'))
#     答案列表 = []
#     最大页码 = len(PDF工具箱.获取页面迭代器())
#     全部括号列表 = []
#     全部左括号列表 = ['（', '(', '【', '[', '{']
#     全部右括号列表 = ['）', ')', '】', ']', '}']
#     for bracket in 全部左括号列表:
#         for right_bracket in 全部右括号列表:
#             全部括号列表.append((bracket, right_bracket))
#     print('全部括号列表：\n', 全部括号列表)
#     选择的括号列表 = input('请从上述括号组合中选择需要提取的括号：\n')
#     选择的括号列表 = [tuple(bracket.split(',')) for bracket in 选择的括号列表.split(';')]
#     if 结束页码 > 最大页码:
#         结束页码 = 最大页码
#     if 起始页码 < 1:
#         起始页码 = 1
#     for page_number in range(起始页码 - 1, 结束页码):
#         答案列表.append(PDF工具箱.提取判断答案(page_number, symbol_list=选择的括号列表))
#     for 一页答案 in 答案列表:
#         for 答案 in 一页答案:
#             print(答案, end='\t')
#
#     # 提取括号内的文本
#     用于读取的PDF = input('请输入要读取的PDF路径：')
#     PDF工具箱 = PDF工具箱(用于读取的PDF路径=用于读取的PDF)
#     起始页码 = int(input('请输入起始页码：'))
#     结束页码 = int(input('请输入结束页码：'))
#     print('全部括号列表：\n', 全部括号列表)
#     选择的括号列表 = input('请从上述括号组合中选择需要提取的括号：\n')
#     选择的括号列表 = [tuple(bracket.split(',')) for bracket in 选择的括号列表.split(';')]
#     仅提取内部只有字母的括号 = input('是否仅提取内部只有字母的括号？(y/n)：')
#     if 仅提取内部只有字母的括号.lower() == 'y':
#         letter_only = True
#     else:
#         letter_only = False
#     仅提取内部只有数字的括号 = input('是否仅提取内部只有数字的括号？(y/n)：')
#     if 仅提取内部只有数字的括号.lower() == 'y':
#         number_only = True
#     else:
#         number_only = False
#     仅提取内部只有判断结果的括号 = input('是否仅提取内部只有判断结果的括号？(y/n)：')
#     if 仅提取内部只有判断结果的括号.lower() == 'y':
#         true_false_only = True
#     else:
#         true_false_only = False
#     最大页码 = len(PDF工具箱.获取页面迭代器())
#     if 结束页码 > 最大页码:
#         结束页码 = 最大页码
#     if 起始页码 < 1:
#         起始页码 = 1
#     for page_number in range(起始页码 - 1, 结束页码):
#         文本列表 = PDF工具箱.提取括号内的文本(page_number, bracket_style=选择的括号列表, letter_only=letter_only,
#                                               number_only=number_only, true_false_only=true_false_only)
#         for 文本 in 文本列表:
#             print(文本, end='\t')
#
#     # 删除括号内的文本
#     用于读取的PDF = input('请输入要读取的PDF路径：')
#     PDF工具箱 = PDF工具箱(用于写入的PDF路径=用于读取的PDF)
#     起始页码 = int(input('请输入起始页码：'))
#     结束页码 = int(input('请输入结束页码：'))
#     print('全部括号列表：\n', 全部括号列表)
#     选择的括号列表 = input('请从上述括号组合中选择需要删除的括号：\n')
#     选择的括号列表 = [tuple(bracket.split(',')) for bracket in 选择的括号列表.split(';')]
#     仅删除内部只有字母的括号 = input('是否仅删除内部只有字母的括号？(y/n)：')
#     if 仅删除内部只有字母的括号.lower() == 'y':
#         letter_only = True
#     else:
#         letter_only = False
#     仅删除内部只有数字的括号 = input('是否仅删除内部只有数字的括号？(y/n)：')
#     if 仅删除内部只有数字的括号.lower() == 'y':
#         number_only = True
#     else:
#         number_only = False
#     仅删除内部只有判断结果的括号 = input('是否仅删除内部只有判断结果的括号？(y/n)：')
#     if 仅删除内部只有判断结果的括号.lower() == 'y':
#         true_false_only = True
#     else:
#         true_false_only = False
#     输出PDF路径 = input('请输入输出PDF路径：')
#     最大页码 = len(PDF工具箱.获取页面迭代器())
#     if 结束页码 > 最大页码:
#         结束页码 = 最大页码
#     if 起始页码 < 1:
#         起始页码 = 1
#     for page_number in range(起始页码 - 1, 结束页码):
#         PDF工具箱.删除括号内的文本(page_number, bracket_style=选择的括号列表, letter_only=letter_only,
#                                    number_only=number_only, true_false_only=true_false_only,
#                                    output_pdf_path=输出PDF路径)
#
#     # 提取高亮文本
#     用于读取的PDF = input('请输入要读取的PDF路径：')
#     PDF工具箱 = PDF工具箱(用于读取的PDF路径=用于读取的PDF)
#     起始页码 = int(input('请输入起始页码：'))
#     结束页码 = int(input('请输入结束页码：'))
#     高亮文本列表 = []
#     最大页码 = len(PDF工具箱.获取页面迭代器())
#     if 结束页码 > 最大页码:
#         结束页码 = 最大页码
#     if 起始页码 < 1:
#         起始页码 = 1
#     for page_number in range(起始页码 - 1, 结束页码):
#         高亮文本列表.append(PDF工具箱.提取高亮文本(page_number))
#
#     for 高亮文本 in 高亮文本列表:
#         for 文本 in 高亮文本:
#             print(文本, end='\t')
#         print()
if __name__ == '__main__':
    PDF工具箱1 = PDF工具箱(用于读取的PDF路径=r'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\部分真题.pdf')
    res = PDF工具箱1.提取括号内的文本(1, letter_only=True)
    print(res)
    PDF工具箱2 = PDF工具箱(用于写入的PDF路径=r'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\部分真题.pdf')
    PDF工具箱2.删除括号内的文本(1, letter_only=True)
