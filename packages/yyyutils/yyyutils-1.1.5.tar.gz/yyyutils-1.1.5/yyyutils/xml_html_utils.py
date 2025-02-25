from lxml import etree
import os


class XMLUtils:
    """
    用于处理XML文件的工具类。——未完成
    """
    def __init__(self, xml_string_or_xml_file_path):
        if os.path.isfile(xml_string_or_xml_file_path):
            self.tree = etree.parse(xml_string_or_xml_file_path)
            self.root = self.tree.getroot()
            # 打印xml文件内容
            # print(etree.tostring(self.root, pretty_print=True).decode('utf-8'))
        else:
            self.root = etree.fromstring(xml_string_or_xml_file_path)

    def generate_xpath_expression(tag_name, attributes=None, index=None, text=None, axis=None):
        """
        生成XPath表达式，用于查找特定标签和可选的属性、索引、文本内容或轴。

        参数:
        tag_name (str): 标签名称
        attributes (list of tuples, 可选): 属性名称和值的列表，例如[("class", "my-class"), ("id", "my-id")]
        index (int, 可选): 元素的索引，例如选择第一个或最后一个元素
        text (str, 可选): 包含指定文本的元素
        axis (str, 可选): 使用XPath轴，如 "ancestor", "preceding" 等

        返回:
        str: 生成的XPath表达式
        """
        if not tag_name:
            raise ValueError("tag_name 参数不能为空")

        # 基础XPath表达式
        xpath = f"//{tag_name}"

        # 添加属性过滤
        if attributes and isinstance(attributes, list) and all(
                isinstance(pair, tuple) and len(pair) == 2 for pair in attributes):
            for attr_name, attr_value in attributes:
                xpath += f"[@{attr_name}='{attr_value}']"

        # 添加索引选择
        if index is not None and isinstance(index, int):
            xpath += f"[{index + 1}]"  # XPath中的位置索引从1开始

        # 添加文本内容搜索
        if text:
            xpath += f"[.='{text}']"

        # 添加轴查询
        if axis:
            if index is not None:
                xpath = f"{axis}::{tag_name}[{index + 1}]"
            else:
                xpath = f"{axis}::{tag_name}"

        return xpath

    def xml2html(self):
        html_str = etree.tostring(self.root, encoding='unicode', method='html')
        print(html_str)
        return html_str


if __name__ == '__main__':
    xml_utils = XMLUtils(r'D:\Python\Python38\Lib\site-packages\mytools\excel_word_utils\gchz\word\document.xml')
    xml_utils.xml2html()
