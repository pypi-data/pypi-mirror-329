"""
TODO:
- 给ai优化（有错误的地方没有，有的话予以说明并修改优化）
"""
import math
import numpy as np
import pandas as pd
import itertools


class MathUtils:
    PI = math.pi

    def __init__(self):
        self.PI = math.pi

    @staticmethod
    def sqrt(x):
        """
        计算平方根
        :param x:
        :return:
        """
        return math.sqrt(x)

    @staticmethod
    def linear_interpolate(x1, x2, y1, y2, x):
        """
        线性内插法求值
        :return:
        """
        return (y2 - y1) / (x2 - x1) * (x - x1) + y1

    @staticmethod
    def combinations_iter(list_to_combine, r):
        """
        返回所有组合的迭代器
        :param list_to_combine:
        :param r:
        :return:
        """
        return itertools.combinations(list_to_combine, r)

    @staticmethod
    def combinations_list(list_to_combine, r):
        """
        返回所有组合的列表
        :param list_to_combine:
        :param r:
        :return:
        """
        return list(itertools.combinations(list_to_combine, r))

    @staticmethod
    def combinations_count(n, r):
        """
        计算所有组合的数量
        :param n: 待组合的元素个数
        :param r: 组合的元素个数
        :return:
        """
        return math.comb(n, r)

    @staticmethod
    def factorial(n):
        """
        计算阶乘
        参数:
            n: 待计算阶乘的数
        返回:
            阶乘结果
        """
        if n < 0:
            raise ValueError("阶乘不能用于负数")
        if n == 0:
            return 1
        return n * MathUtils.factorial(n - 1)

    @staticmethod
    def minimum_common_divisor(a, b):
        """
        最小公约数
        :param a:
        :param b:
        :return:
        """
        return math.gcd(a, b)

    @staticmethod
    def minimum_common_multiple(a, b):
        """
        最小公倍数
        :param a:
        :param b:
        :return:
        """
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def calculate_statistics(data):
        """
        计算数据的统计信息，包括均值、方差、标准差、最小值、最大值、中位数、四分位数等
        :param data: 待计算的数据
        :return:
        """
        data = np.array(data)
        mean = np.mean(data)
        variance = np.var(data)
        std = np.std(data)
        min_value = np.min(data)
        max_value = np.max(data)
        median = np.median(data)
        quartile1, quartile3 = np.percentile(data, [25, 75])
        # 中文名称
        return pd.Series({'均值': mean, '方差': variance, '标准差': std, '最小值': min_value, '最大值': max_value,
                          '中位数': median, '四分位数1': quartile1, '四分位数3': quartile3})

    @staticmethod
    def is_prime(n):
        """
        判断一个数是否为质数
        参数:
            n: 待判断的数字
        返回:
            布尔值，表示是否为质数
        """
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def any_to_decimal(number, source_base=10):
        """
        将任意进制数转换为十进制数

        参数:
            number: 输入的数字（字符串格式）
            source_base: 源数字的进制（2-36之间），默认为10进制

        返回:
            转换后的十进制数

        示例:
            any_to_decimal("1A", 16) => 26
            any_to_decimal("1010", 2) => 10
            any_to_decimal("777", 8) => 511
        """
        # 定义字符集：0-9 和 A-Z
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # 参数验证
        if not isinstance(number, str):
            number = str(number)
        number = number.upper()  # 转换为大写

        if source_base < 2 or source_base > 36:
            raise ValueError("进制必须在2到36之间")

        # 检查输入的数字是否合法
        valid_digits = digits[:source_base]
        if not all(d in valid_digits for d in number):
            raise ValueError(f"输入的数字包含非法字符，对于{source_base}进制，合法字符为: {valid_digits}")

        # 转换过程
        decimal = 0
        power = 0

        # 从右向左遍历每一位
        for digit in reversed(number):
            # 获取当前位的值
            value = digits.index(digit)
            # 累加：当前位值 * 进制的幂次方
            decimal += value * (source_base ** power)
            power += 1

        return decimal

    @staticmethod
    def decimal_to_any(decimal_num, target_base=10):
        """
        将十进制数转换为任意进制数

        参数:
            decimal_num: 输入的十进制数
            target_base: 目标进制（2-36之间），默认为10进制

        返回:
            转换后的目标进制数（字符串格式）

        示例:
            decimal_to_any(26, 16) => "1A"
            decimal_to_any(10, 2) => "1010"
            decimal_to_any(511, 8) => "777"
        """
        if decimal_num == 0:
            return "0"

        # 定义字符集：0-9 和 A-Z
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # 参数验证
        if target_base < 2 or target_base > 36:
            raise ValueError("进制必须在2到36之间")

        # 转换过程
        result = ""
        num = abs(decimal_num)  # 处理负数

        while num:
            result = digits[num % target_base] + result
            num //= target_base

        # 处理负数
        if decimal_num < 0:
            result = "-" + result

        return result

    @staticmethod
    def convert_between_bases(number, source_base=10, target_base=10):
        """
        在任意进制之间转换

        参数:
            number: 输入的数字（字符串格式）
            source_base: 源进制
            target_base: 目标进制

        返回:
            转换后的数字（字符串格式）

        示例:
            convert_between_bases("1A", 16, 2) => "11010"
            convert_between_bases("1010", 2, 16) => "A"
            convert_between_bases("777", 8, 16) => "1FF"
        """
        # 先转换为十进制
        decimal = MathUtils.any_to_decimal(number, source_base)
        # 再从十进制转换为目标进制
        return MathUtils.decimal_to_any(decimal, target_base)

    @staticmethod
    def new_round(number, digits=3) -> str:
        """
        实现了四舍五入（单进双不进）的功能，可以指定保留几位小数
        Parameters
        ----------
        number
        digits

        Returns
        -------

        """
        if digits == 0:
            raise ValueError('digits should be greater than 0')
        # 将数字转换为字符串，以便操作小数点后的具体位数
        num_str = str(number)

        # 分离整数部分和小数部分
        parts = num_str.split('.')

        if len(parts) == 2:
            integer_part = int(parts[0])
            decimal_part = parts[1]

            # 检查第四位小数
            if len(decimal_part) >= digits + 1:
                decimal_part = decimal_part[: digits + 1]
                fourth_digit = int(decimal_part[digits])  # 第四位小数
                third_digit = int(decimal_part[digits - 1])  # 第三位小数

                # 如果第四位是5，则根据第三位是否为奇数来决定是否进位
                if fourth_digit == 5:
                    if third_digit % 2 == 1:
                        # 第三位是奇数，进位
                        temp = str(int(decimal_part[:digits]) + 1)
                        if decimal_part[0] == '0':
                            decimal_part = '0' + temp
                        else:
                            decimal_part = temp
                        # 处理小数部分只剩下三位
                        if len(decimal_part) > digits:
                            integer_part += 1
                            decimal_part = decimal_part[1:]
                    else:
                        # 第三位是偶数，不进位
                        decimal_part = decimal_part[:digits]
                else:
                    return f'{str(round(number, digits)):0<{digits + len(parts[0]) + 1}}'

            # 重新组合数字并转换为浮点数
            result_str = str(integer_part) + '.' + decimal_part
            return f'{result_str:0<{digits + len(parts[0]) + 1}}'
        else:
            num_str += '.'
            return f'{num_str:0<{digits + len(num_str)}}'

    @staticmethod
    def dms_to_degrees(d, m, s) -> float:
        """
        将度分秒形式的坐标转换为度形式
        """
        d, m, s = float(d), float(m), float(s)
        decimal_degrees = d + m / 60 + s / 3600
        return decimal_degrees

    @staticmethod
    def degrees_to_dms(decimal_degrees) -> tuple:
        """
        将度形式的坐标转换为度分秒形式
        """
        if decimal_degrees < 0:
            sign = '-'
            decimal_degrees = abs(decimal_degrees)
        else:
            sign = ''
        degrees = int(decimal_degrees)
        minutes = int((decimal_degrees - degrees) * 60)
        seconds = round(decimal_degrees * 3600 - degrees * 3600 - minutes * 60)
        # 都保留为两位整数，不足的部分用0补齐
        degrees = str(degrees).zfill(2)
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        return f'{sign}{degrees}°{minutes}′{seconds}″', -float(degrees), -float(minutes), -float(seconds)

    @staticmethod
    def arcsin(x, degrees=True):
        """
        反正弦函数，返回角度或弧度，默认返回角度，保留两位小数
        """
        if x < -1 or x > 1:
            raise ValueError('x should be between -1 and 1')
        result = math.asin(x)
        if degrees:
            result = round(math.degrees(result), 2)
        else:
            result = round(result, 2)
        return result

    @staticmethod
    def arccos(x, degrees=True):
        """
        反余弦函数，返回角度或弧度，默认返回角度，保留两位小数
        """
        if x < -1 or x > 1:
            raise ValueError('x should be between -1 and 1')
        result = math.acos(x)
        if degrees:
            result = round(math.degrees(result), 2)
        else:
            result = round(result, 2)
        return result

    @staticmethod
    def arctan(x, degrees=True):
        """
        反正切函数，返回角度或弧度，默认返回角度，保留两位小数
        """
        result = math.atan(x)
        if degrees:
            result = round(math.degrees(result), 2)
        else:
            result = round(result, 2)
        return result

    @staticmethod
    def sin(x, degrees=True):
        """
        正弦函数，输入角度或弧度，默认角度
        :param x:
        :param degrees:
        :return:
        """
        if degrees:
            x = math.radians(x)
        result = math.sin(x)
        return result

    @staticmethod
    def cos(x, degrees=True):
        """
        余弦函数，输入角度或弧度，默认角度
        :param x:
        :param degrees:
        :return:
        """
        if degrees:
            x = math.radians(x)
        result = math.cos(x)
        return result

    @staticmethod
    def tan(x, degrees=True):
        """
        正切函数，输入角度或弧度，默认角度
        :param x:
        :param degrees:
        :return:
        """
        if degrees:
            x = math.radians(x)
        result = math.tan(x)
        return result

    @staticmethod
    def round_to_n(x, n):
        """
        实现四舍五入到指定位数的功能
        :param x: 待处理的数字
        :param n: 保留的小数位数
        :return: 处理后的数字
        """
        return round(x, n)

    @staticmethod
    def calculate_distance(point1, point2):
        """
        计算两点间欧氏距离
        参数:
            point1: 第一个点的坐标元组/列表 (x1, y1)
            point2: 第二个点的坐标元组/列表 (x2, y2)
        返回:
            两点间的距离
        """
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    @staticmethod
    def random_between(a, b, num=1):
        """
        在两个数值之间随机取值(均匀分布)，如果num大于1，则返回num个随机数的列表，否则返回单个随机数
        :param a: 最小值
        :param b: 最大值
        :param num: 随机数个数
        :return:
        """
        if num == 1:
            return np.random.uniform(a, b)
        else:
            return np.random.uniform(a, b, num)

    @staticmethod
    def random_int_between(a, b, num=1):
        """
        在两个整数之间随机取值(均匀分布)，如果num大于1，则返回num个随机数的列表，否则返回单个随机数
        :param a: 最小值
        :param b: 最大值
        :param num: 随机数个数
        :return:
        """
        if num == 1:
            return np.random.randint(a, b + 1)
        else:
            return np.random.randint(a, b + 1, num)

    @staticmethod
    def random_choice(seq, num=1):
        """
        从序列中随机取一个元素
        :param seq: 序列
        :param num: 随机数个数
        :return: 随机取出的元素
        """
        if num > len(seq):
            raise ValueError('num should be less than or equal to the length of the sequence')
        if num == 1:
            return np.random.choice(seq)
        else:
            return np.random.choice(seq, num)

    @staticmethod
    def random_shuffle(seq):
        """
        随机打乱一个序列
        :param seq: 序列
        :return: 打乱后的序列
        """
        np.random.shuffle(seq)
        return seq

    @staticmethod
    def random_normal(mean, std, num=1):
        """
        随机生成正态分布的随机数
        :param mean: 均值
        :param std: 标准差
        :param num: 随机数个数
        :return: 随机数列表
        """
        return np.random.normal(mean, std, num)

    @staticmethod
    def random_exponential(scale, num=1):
        """
        随机生成指数分布的随机数
        :param scale: 缩放因子
        :param num: 随机数个数
        :return: 随机数列表
        """
        return np.random.exponential(scale, num)

    @staticmethod
    def random_gamma(shape, scale, num=1):
        """
        随机生成伽马分布的随机数
        :param shape: 形状参数
        :param scale: 尺度参数
        :param num: 随机数个数
        :return: 随机数列表
        """
        return np.random.gamma(shape, scale, num)

    @staticmethod
    def split_by_step(start, end, step, include_end=True):
        """
        根据起始值、终止值、步长返回两个值之间的等差数列，支持正负步长
        :param start: 起始值
        :param end: 终止值
        :param step: 步长
        :param include_end: 是否包含终止值
        :return:
        """
        if step == 0:
            raise ValueError('step should not be 0')
        if step > 0:
            if start > end:
                raise ValueError('start should be less than or equal to end when step is positive')
            res = list(np.arange(start, end, step))
            if include_end and end not in res:
                res.append(end)
            return res
        else:
            if start < end:
                raise ValueError('start should be greater than or equal to end when step is negative')
            res = list(np.arange(start, end, step))
            if include_end and end not in res:
                res.append(end)
            return res

    @staticmethod
    def split_by_segments(start, end, segments_num):
        """
        根据起始值、终止值、分段数返回等差数列
        :param start: 起始值
        :param end: 终止值
        :param segments_num: 分段数
        :return:
        """
        if segments_num < 2:
            raise ValueError('num should be greater than or equal to 2')
        return list(np.linspace(start, end, segments_num + 1))

    @staticmethod
    def limit_value(value, min_value=None, max_value=None):
        """
        限制值在最小值和最大值之间，如果值小于最小值，则返回最小值；如果值大于最大值，则返回最大值
        如果最小值或最大值为None，则不限制对应边界
        :param value: 待限制的值
        :param min_value: 最小值
        :param max_value: 最大值
        :return: 限制后的值
        """
        if min_value is not None and value < min_value:
            return min_value
        elif max_value is not None and value > max_value:
            return max_value
        else:
            return value

    @staticmethod
    def find_min_greater_or_equal(x, lst, include_equal=True):
        """
        返回列表里面大于等于x的元素中的最小值。

        :param x: 要比较的值
        :param lst: 要搜索的列表
        :param include_equal: 是否包括等于x的值，默认为True
        :return: 列表中大于等于x的最小值，如果没有这样的元素，则返回None
        """
        if include_equal:
            return min(filter(lambda y: y >= x, lst), default=None)
        else:
            return min(filter(lambda y: y > x, lst), default=None)

    @staticmethod
    def find_max_less_or_equal(x, lst, include_equal=True):
        """
        返回列表里面小于等于x的元素中的最大值。

        :param x: 要比较的值
        :param lst: 要搜索的列表
        :param include_equal: 是否包括等于x的值，默认为True
        :return: 列表中小于等于x的最大值，如果没有这样的元素，则返回None
        """
        if include_equal:
            return max(filter(lambda y: y <= x, lst), default=None)
        else:
            return max(filter(lambda y: y < x, lst), default=None)

    @staticmethod
    def 两个数近似相等(a, b, tolerance=1e-6, a_bigger=False, b_bigger=False):
        """
        判断两个数是否近似相等
        :param a: 数值1
        :param b: 数值2
        :param tolerance: 容忍度，默认1e-6
        :param a_bigger: a是否大于b，默认为False
        :param b_bigger: b是否大于a，默认为False
        :return: 相等返回True，否则返回False
        """
        if a_bigger and a < b:
            return False
        if b_bigger and b < a:
            return False
        return abs(a - b) < tolerance

    @staticmethod
    def a近似小于等于b加上容忍度(a, b, tolerance=1e-6):
        """
        判断a是否近似小于b
        :param a: 数值1
        :param b: 数值2
        :param tolerance: 容忍度，默认1e-6
        :return: 小于返回True，否则返回False
        """
        return a <= b + tolerance

    @staticmethod
    def a近似大于等于b减去容忍度(a, b, tolerance=1e-6):
        """
        判断a是否近似大于b
        :param a: 数值1
        :param b: 数值2
        :param tolerance: 容忍度，默认1e-6
        :return: 大于返回True，否则返回False
        """
        return a >= b - tolerance

    @staticmethod
    def a近似小于等于b减去容忍度(a, b, tolerance=1e-6):
        """
        判断a是否近似小于等于b
        :param a: 数值1
        :param b: 数值2
        :param tolerance: 容忍度，默认1e-6
        :return: 小于等于返回True，否则返回False
        """
        return a <= b - tolerance

    @staticmethod
    def a近似大于等于b加上容忍度(a, b, tolerance=1e-6):
        """
        判断a是否近似大于等于b
        :param a: 数值1
        :param b: 数值2
        :param tolerance: 容忍度，默认1e-6
        :return: 大于等于返回True，否则返回False
        """
        return a >= b + tolerance


if __name__ == '__main__':
    result = MathUtils.linear_interpolate(50, 60, 0.856, 0.807, 58.18)
    print(result)
    print(MathUtils.calculate_statistics([1, 2, 3, 4, 5]))
    print(MathUtils.arcsin(-0.5))
    print(MathUtils.random_shuffle([1, 2, 3, 4, 5]))
    print(MathUtils.random_normal(0, 1, 10))
    print(MathUtils.random_exponential(1, 10))
    print(MathUtils.split_by_segments(0, 10.3, 5))
    print(MathUtils.split_by_step(10.1, 1.1, -2))
    print(MathUtils.combinations_count(5, 3))
