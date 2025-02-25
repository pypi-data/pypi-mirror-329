import math


class EngineerMeasureUtils:
    """
    工程测量静态工具类
    """

    @staticmethod
    def arctan(x, y):
        """
        输出角度都在0-360度之间，可区分四个象限
        :param x:
        :param y:
        :return:
        """
        angle = math.atan2(y, x)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    @staticmethod
    def coordinate_inversion(Xa, Ya, Xb, Yb):
        Dab = math.sqrt((Xb - Xa) ** 2 + (Yb - Ya) ** 2)
        alpha = EngineerMeasureUtils.arctan(Yb - Ya, Xb - Xa)
        return Dab, alpha

    @staticmethod
    def coordinate_forward_calculation(Xa, Ya, Dab, alpha):
        """
        弧度制输入
        :param Xa:
        :param Ya:
        :param Dab:
        :param alpha:
        :return:
        """
        Xb = Xa + Dab * math.cos(alpha)
        Yb = Ya + Dab * math.sin(alpha)
        return Xb, Yb

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
