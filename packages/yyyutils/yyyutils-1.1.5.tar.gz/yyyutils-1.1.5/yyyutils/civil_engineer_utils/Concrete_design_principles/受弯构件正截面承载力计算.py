from yyyutils.math_utils.math_utils import MathUtils
import re

PI = MathUtils.PI


class 通用工具类:
    """
    所有单位使用国际单位
    """
    debug = True

    @staticmethod
    def debug_print(description='调试信息', formula=None, params=None, result=None, print_params=True,
                    decimal_places=3):
        """
        调试打印函数
        :param description: 调试信息的描述
        :param formula: 理论公式的字符串
        :param params: 参数字典，键为变量名，值为变量值
        :param result: 计算结果
        :param decimal_places: 保留的小数位数
        """

        print(f'\n{description:-^50}')
        print(f"理论公式：{formula}")
        if print_params:
            print(f"参数：{params}")
        new_formula = formula
        # 替换公式中的变量
        if formula is not None and params is not None:
            for key, value in params.items():
                # r'\b' 确保只匹配完整的变量名
                new_formula = re.sub(r'\b' + re.escape(key) + r'\b', f"{value:.{decimal_places}f}", new_formula)
        if formula is None:
            new_formula = description
        if isinstance(result, float):
            print(f"计算结果：{new_formula} = {result:.{decimal_places}f}")
        else:
            print(f"计算结果：{new_formula} = {result}")

    @staticmethod
    def 实际配筋率ρ1(As, A):
        """
        计算配筋率ρ
        :param As:
        :param A:
        :return:
        """
        res = As / A

        通用工具类.debug_print("实际配筋率ρ1", "ρ1 = As / A", {"As": As, "A": A}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 最小配筋率ρmin(ft, fy):
        """
        计算轴心受拉构件的最小配筋率ρmin
        :param ft:
        :param fy:
        :return:
        """
        res = max(0.002, 0.45 * ft / fy)
        通用工具类.debug_print("最小配筋率ρmin", "ρmin = max(0.002, 0.45 * ft / fy)", {"ft": ft, "fy": fy},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 判断是否少筋(ρ, ρmin):
        """
        判断是否为少筋构件
        :param ρ:
        :param ρmin:
        :return:
        """
        res = ρ < ρmin
        通用工具类.debug_print("判断是否为少筋构件", "ρ < ρmin", {"ρ": ρ, "ρmin": ρmin},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 判断是否超筋(ξ, ξb):
        """
        判断是否为超筋构件
        :param ξ:
        :param ξb:
        :return:
        """
        res = ξ > ξb
        通用工具类.debug_print("判断是否为超筋构件", "ξ > ξb", {"ξ": ξ, "ξb": ξb},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 矩形截面面积(b, h):
        """
        矩形截面面积计算公式
        :param b:
        :param h:
        :return:
        """
        res = b * h
        通用工具类.debug_print("矩形截面面积计算", "A = b * h", {"b": b, "h": h}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 圆形截面面积(d):
        """
        圆形截面面积计算公式
        :param d:
        :return:
        """
        res = PI * d ** 2 / 4
        通用工具类.debug_print("圆形截面面积计算", "A = π * d^2 / 4", {"d": d}, res) if 通用工具类.debug else None
        return res


class 矩形截面受弯构件正截面承载力计算_单筋梁_工具类(通用工具类):
    """
    所有单位使用国际单位
    """
    debug = True

    @staticmethod
    def 简化系数α1(C):
        """
        简化系数α1
        :param C: 混凝土强度等级
        :return:
        """
        if not isinstance(C, int):
            raise TypeError("混凝土强度等级C必须为整数！")

        if C <= 50:
            α1 = 1.0
        if C > 80:
            raise ValueError("混凝土强度等级超出范围C80，不能使用内插法计算！")
        if 50 < C <= 80:
            α1 = MathUtils.linear_interpolate(50, 80, 1.0, 0.94, C)
        通用工具类.debug_print("简化系数α1", "α1 = 1.0", {"C": C}, α1) if 通用工具类.debug else None
        return α1

    @staticmethod
    def 正截面承载力Mu_对受拉钢筋合力点取矩_原始(α1, fc, b, h0, x):
        """
        对受拉钢筋合力点取矩，使用原始公式计算正截面承载力（即不代入相对受压区高度）
        :param α1:
        :param fc:
        :param b:
        :param x:
        :param h0:
        :return:
        """
        res = α1 * fc * b * x * (h0 - x / 2)
        通用工具类.debug_print("计算正截面承载力Mu", "Mu = α1 * fc * b * x * (h0 - x / 2)",
                               {"α1": α1, "fc": fc, "b": b, "x": x, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 正截面承载力Mu_对受压区合力点取矩_原始(fy, As, h0, x):
        """
        对受压区合力点取矩，使用原始公式计算正截面承载力（即不代入相对受拉区高度）
        :param fy:
        :param As:
        :param h0:
        :param x:
        :return:
        """
        res = fy * As * (h0 - x / 2)
        通用工具类.debug_print("计算正截面承载力Mu", "Mu = fy * As * (h0 - x / 2)",
                               {"fy": fy, "As": As, "h0": h0, "x": x}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 正截面承载力Mu_对受拉钢筋合力点取矩_修正(α1, αs, fc, b, h0):
        """
        对受拉钢筋合力点取矩，使用修正公式计算正截面承载力（代入相对受压区高度）
        :param α1:
        :param αs:
        :param fc:
        :param b:
        :param h0:
        :return:
        """
        res = α1 * fc * b * h0 ** 2 * αs
        通用工具类.debug_print("计算正截面承载力Mu", "Mu = α1 * fc * b * h0^2 * αs",
                               {"α1": α1, "αs": αs, "fc": fc, "b": b, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 正截面承载力Mu_对受压区合力点取矩_修正(γs, fy, As, h0):
        """
        对受压区合力点取矩，使用修正公式计算正截面承载力（代入相对受拉区高度）
        :param γs:
        :param fy:
        :param As:
        :param h0:
        :return:
        """
        res = γs * fy * As * h0
        通用工具类.debug_print("计算正截面承载力Mu", "Mu = γs * fy * As * h0",
                               {"γs": γs, "fy": fy, "As": As, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def αs(ξ):
        """
        αs计算公式
        :param ξ:
        :return:
        """
        res = ξ * (1 - 0.5 * ξ)
        通用工具类.debug_print("计算αs", "αs = ξ * (1 - 0.5 * ξ)", {"ξ": ξ}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def γs(ξ):
        """
        γs计算公式
        :param ξ:
        :return:
        """
        res = 1 - 0.5 * ξ
        通用工具类.debug_print("计算γs", "γs = 1 - 0.5 * ξ", {"ξ": ξ}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 由γs计算ξ(γs):
        """
        ξ计算公式
        :param γs:
        :return:
        """
        res = (1 - γs) * 2
        通用工具类.debug_print("计算ξ", "ξ = (1 - γs) * 2", {"γs": γs}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 相对受压区高度ξ(h0, x):
        """
        相对受压区高度ξ计算公式
        :param h0:
        :param x:
        :return:
        """
        res = x / h0
        通用工具类.debug_print("计算相对受压区高度ξ", "ξ = x / h0", {"x": x, "h0": h0},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋合力点到受拉混凝土边缘的距离as_多排(c, A1, d1, dcu=0, A2=0, d2=0, A3=0, d3=0):
        """
        受拉钢筋合力点到受拉混凝土边缘的距离as，A1为最靠近边缘的一排受拉钢筋
        :param c:
        :param A1:
        :param d1:
        :param A2:
        :param d2:
        :param A3:
        :param d3:
        :return:
        """
        res = (A1 * (c + d1 / 2) + A2 * (c + d1 + d1 + d2 / 2) + A3 * (c + d1 + d1 + d2 + d2 + d3 / 2)) / (A1 + A2 + A3)
        通用工具类.debug_print("计算受拉钢筋合力点到受拉混凝土边缘的距离as",
                               "as = (A1*(c+d1/2)+A2*(c+d1+d1+d2/2)+A3*(c+d1+d1+d2+d2+d3/2))/(A1+A2+A3)",
                               {"c": c, "A1": A1, "d1": d1, "A2": A2, "d2": d2, "A3": A3, "d3": d3},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋合力点到受拉混凝土边缘的距离as_一排(c, d, dcu=0):
        """
        受拉钢筋合力点到受拉混凝土边缘的距离as，A1为最靠近边缘的一排受拉钢筋
        :param c:
        :param d:
        :param dcu:
        :return:
        """
        res = c + d / 2 + dcu
        通用工具类.debug_print("计算受拉钢筋合力点到受拉混凝土边缘的距离as", "as = c + d / 2 + dcu",
                               {"c": c, "d": d, "dcu": dcu}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋合力点到受压混凝土边缘的距离h0(h, as_):
        """
        受拉钢筋合力点到受压混凝土边缘的距离h0
        :param h:
        :param as_:
        :return:
        """
        res = h - as_
        通用工具类.debug_print("计算受拉钢筋合力点到受压混凝土边缘的距离h0", "h0 = h - as_", {"h": h, "as_": as_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受压区高度x(α1, fy, As, fc, b):
        """
        受压区高度x计算公式
        :param α1:
        :param fy:
        :param As:
        :param fc:
        :param b:
        :return:
        """
        res = fy * As / (α1 * fc * b)
        通用工具类.debug_print("计算受压区高度x", "x = fy * As / (α1 * fc * b)",
                               {"α1": α1, "fy": fy, "As": As, "fc": fc, "b": b}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受压区合力点到受拉混凝土边缘的距离as_估算_两排_梁(h):
        as_ = h - 0.06
        通用工具类.debug_print("计算受压区合力点到受拉混凝土边缘的距离as_估算_两排", "as_ = h - 0.06", {"h": h},
                               as_) if 通用工具类.debug else None
        return as_

    @staticmethod
    def 受压区合力点到受拉混凝土边缘的距离as_估算_一排_梁(h):
        as_ = h - 0.035
        通用工具类.debug_print("计算受压区合力点到受拉混凝土边缘的距离as_估算_一排", "as_ = h - 0.035", {"h": h},
                               as_) if 通用工具类.debug else None
        return as_

    @staticmethod
    def αs_对受拉钢筋合力点取矩(α1, M, fc, b, h0):
        """
        αs计算公式，使用修正公式计算
        :param α1:
        :param M:
        :param fc:
        :param b:
        :param h0:
        :return:
        """
        res = M / (α1 * fc * b * h0 ** 2)
        通用工具类.debug_print("计算αs_对受拉钢筋合力点取矩", "αs = M / (α1 * fc * b * h0^2)",
                               {"α1": α1, "M": M, "fc": fc, "b": b, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def γs_对受压区合力点取矩(M, fy, As, h0):
        """
        γs计算公式，使用修正公式计算
        :param M:
        :param fy:
        :param As:
        :param h0:
        :return:
        """
        res = M / (fy * As * h0)
        通用工具类.debug_print("计算γs_对受压区合力点取矩", "γs = M / (fy * As * h0)",
                               {"M": M, "fy": fy, "As": As, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 由αs计算相对受压区高度ξ(αs):
        """
        相对受压区高度ξ计算公式
        :param αs:
        :return:
        """
        res = 1 - (1 - 2 * αs) ** 0.5
        通用工具类.debug_print("计算相对受压区高度ξ", "ξ = 1 - (1 - 2 * αs)^0.5", {"αs": αs},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 纵向受拉钢筋面积As(ρ, b, h0):
        """
        纵向受拉钢筋面积As计算公式
        :param ρ:
        :param b:
        :param h0:
        :return:
        """
        res = ρ * b * h0
        通用工具类.debug_print("计算纵向受拉钢筋面积As", "As = ρ * b * h0", {"ρ": ρ, "b": b, "h0": h0},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋配筋率ρ(α1, fc, fy, ξ):
        """
        受拉钢筋配筋率ρ计算公式
        :param α1:
        :param fc:
        :param fy:
        :param ξ:
        :return:
        """
        res = (α1 * fc * ξ) / fy
        通用工具类.debug_print("计算受拉钢筋配筋率ρ", "ρ = (α1 * fc * ξ) / fy",
                               {"α1": α1, "fc": fc, "fy": fy, "ξ": ξ}, res) if 通用工具类.debug else None
        return res


class 矩形截面受弯构件正截面承载力计算_双筋梁_工具类(通用工具类):
    """
    所有单位均为国际单位
    """
    debug = True

    @staticmethod
    def 简化系数α1(C):
        """
        简化系数α1
        :param C: 混凝土强度等级
        :return:
        """
        if not isinstance(C, int):
            raise TypeError("混凝土强度等级C必须为整数！")

        if C <= 50:
            α1 = 1.0
        if C > 80:
            raise ValueError("混凝土强度等级超出范围C80，不能使用内插法计算！")
        if 50 < C <= 80:
            α1 = MathUtils.linear_interpolate(50, 80, 1.0, 0.94, C)
        通用工具类.debug_print("简化系数α1", "α1 = 1.0", {"C": C}, α1) if 通用工具类.debug else None
        return α1

    @staticmethod
    def 使用轴力公式计算用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs_(As_, fy_, fy):
        """
        用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs_
        :param As_:
        :param fy_:
        :param fy:
        :return:
        """
        res = fy_ * As_ / fy
        通用工具类.debug_print("计算用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs_",
                               "As2_x大于等于2αs_ = fy_ * As_ / fy",
                               {"As_": As_, "fy_": fy_, "fy": fy}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 使用Mu2计算用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs__(Mu2, fy, h0, as__):
        """
        用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs_
        :param Mu2:
        :param fy:
        :param h0:
        :param as__:
        :return:
        """
        res = Mu2 / (fy * (h0 - as__))
        通用工具类.debug_print("计算用于与受压钢筋形成抵抗力矩的受拉钢筋面积As2_x大于等于2αs_",
                               "As2_x大于等于2αs_ = Mu2 / (fy * (h0 - as__))",
                               {"Mu2": Mu2, "fy": fy, "h0": h0, "as__": as__}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 使用Mu2公式计算受拉钢筋与受压钢筋形成的抵抗力矩Mu2(As2, fy, h0, as__):
        """
        受拉钢筋与受压钢筋形成的抵抗力矩
        :param As2:
        :param fy:
        :param h0:
        :param as__:
        :return:
        """
        res = As2 * (h0 - as__) * fy
        通用工具类.debug_print("计算受拉钢筋与受压钢筋形成的抵抗力矩Mu2",
                               "Mu2 = As2 * (h0 - as__) * fy",
                               {"As2": As2, "fy": fy, "h0": h0, "as__": as__}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 使用M减去Mu1计算受拉钢筋与受压钢筋形成的抵抗力矩Mu2(M, Mu1):
        """
        受拉钢筋与受压钢筋形成的抵抗力矩
        :param M:
        :param Mu1:
        :return:
        """
        res = M - Mu1
        通用工具类.debug_print("计算受拉钢筋与受压钢筋形成的抵抗力矩Mu2", "Mu2 = M - Mu1", {"M": M, "Mu1": Mu1},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋合力点到受压混凝土边缘的距离h0(h, as_):
        """
        受拉钢筋合力点到受压混凝土边缘的距离h0
        :param h:
        :param as_: 直接估计
        :return:
        """
        res = h - as_
        通用工具类.debug_print("计算受拉钢筋合力点到受压混凝土边缘的距离h0", "h0 = h - as_", {"h": h, "as_": as_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 使用M减去Mu2计算受拉钢筋与受压混凝土形成的抵抗力矩Mu1(M, Mu2):
        """
        受拉钢筋与受压混凝土形成的抵抗力矩Mu1
        :param M:
        :param Mu2:
        :return:
        """
        res = M - Mu2
        通用工具类.debug_print("计算受拉钢筋与受压混凝土形成的抵抗力矩Mu1", "Mu1 = M - Mu2", {"M": M, "Mu2": Mu2},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def αs(α1, Mu1, fc, b, h0):
        """
        αs计算公式
        :param α1:
        :param Mu1:
        :param fc:
        :param b:
        :param h0:
        :return:
        """
        res = Mu1 / (α1 * fc * b * h0 ** 2)
        通用工具类.debug_print("计算αs", "αs = Mu1 / (α1 * fc * b * h0^2)",
                               {"α1": α1, "Mu1": Mu1, "fc": fc, "b": b, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def ξ(αs):
        """
        相对受压区高度ξ计算公式
        :param αs:
        :return:
        """
        res = 1 - (1 - 2 * αs) ** 0.5
        通用工具类.debug_print("计算相对受压区高度ξ", "ξ = 1 - (1 - 2 * αs)^0.5", {"αs": αs},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def γs(ξ):
        """
        相对受压区高度γs计算公式
        :param ξ:
        :return:
        """
        res = 1 - 0.5 * ξ
        通用工具类.debug_print("计算相对受压区高度γs", "γs = 1 - 0.5 * ξ", {"ξ": ξ},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 使用单筋梁Mu公式计算用于与受压混凝土形成抵抗力矩的受拉钢筋面积As1_x大于等于2αs_(γs, Mu1, fy, h0):
        """
        用于与受压混凝土形成抵抗力矩的受拉钢筋面积As1_x大于等于2αs_
        :param γs:
        :param Mu1:
        :param fy:
        :param h0:
        :return:
        """
        res = Mu1 / (γs * fy * h0)
        通用工具类.debug_print("计算用于与受压混凝土形成抵抗力矩的受拉钢筋面积As1_x大于等于2αs_",
                               "As1_x大于等于2αs_ = Mu1 / (γs * fy * h0)",
                               {"γs": γs, "Mu1": Mu1, "fy": fy, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋总面积As(As1, As2):
        """
        受拉钢筋总面积As
        :param As1:
        :param As2:
        :return:
        """
        res = As1 + As2
        通用工具类.debug_print("计算受拉钢筋总面积As", "As = As1 + As2", {"As1": As1, "As2": As2},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def x(ξ, h0):
        """
        受压区高度x计算公式
        :param ξ:
        :param h0:
        :return:
        """
        res = h0 * ξ
        通用工具类.debug_print("计算受压区高度x", "x = h0 * ξ", {"ξ": ξ, "h0": h0},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 使用Mu1公式计算受拉钢筋与受压混凝土形成的抵抗力矩Mu1(α1, αs, fc, b, h0):
        """
        受拉钢筋与受压混凝土形成的抵抗力矩Mu1
        :param α1:
        :param αs:
        :param fc:
        :param b:
        :param h0:
        :return:
        """
        res = α1 * αs * fc * b * h0 ** 2
        通用工具类.debug_print("计算受拉钢筋与受压混凝土形成的抵抗力矩Mu1", "Mu1 = α1 * αs * fc * b * h0^2",
                               {"α1": α1, "αs": αs, "fc": fc, "b": b, "h0": h0}, res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 验算公式适用条件x大于等于2αs_(x, αs__):
        """
        验算公式适用条件x大于等于2αs_
        :param x:
        :param αs__:
        :return:
        """
        res = x > 2 * αs__
        通用工具类.debug_print("验算公式适用条件x大于等于2αs_", "x大于等于2αs_", {"x": x, "αs__": αs__},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受压钢筋面积As_(As2, fy, fy_):
        """
        受压钢筋面积As_
        :param As2:
        :param fy:
        :param fy_:
        :return:
        """
        res = As2 * fy / fy_
        通用工具类.debug_print("计算受压钢筋面积As_", "As_ = As2 * fy / fy_", {"As2": As2, "fy": fy, "fy_": fy_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 受拉钢筋面积As_对受压区混凝土和受压钢筋合力点取矩_x小于2αs_(M, fy, h0, as__):
        """
        受拉钢筋面积As_对受压区混凝土和受压钢筋合力点取矩_x小于2αs_
        :param fy:
        :param h0:
        :param as__:
        :return:
        """
        res = M / (fy * (h0 - as__))
        通用工具类.debug_print("计算受拉钢筋面积As_对受压区混凝土和受压钢筋合力点取矩_x小于2αs_",
                               "As_ = M / (fy * (h0 - as__))", {"M": M, "fy": fy, "h0": h0, "as__": as__},
                               res) if 通用工具类.debug else None

        return res


class T形截面受弯构件正截面承载力计算_工具类(通用工具类):
    """
    单位均为国际单位
    """
    debug = True

    @staticmethod
    def 简化系数α1(C):
        """
        简化系数α1
        :param C: 混凝土强度等级
        :return:
        """
        if not isinstance(C, int):
            raise TypeError("混凝土强度等级C必须为整数！")

        if C <= 50:
            α1 = 1.0
        if C > 80:
            raise ValueError("混凝土强度等级超出范围C80，不能使用内插法计算！")
        if 50 < C <= 80:
            α1 = MathUtils.linear_interpolate(50, 80, 1.0, 0.94, C)
        通用工具类.debug_print("计算简化系数α1", "α1 = 1.0", {"C": C},
                               α1) if 通用工具类.debug else None
        return α1

    @staticmethod
    def 判别T形截面类型_截面复核(α1, As, fc, fy, bf_, hf_):
        """
        判别T形截面类型
        :param α1:
        :param fc:
        :param fy:
        :param bf_:
        :param hf_:
        :return:
        """
        type = "第一类T形截面" if fy * As <= α1 * fc * bf_ * hf_ else "第二类T形截面"
        通用工具类.debug_print("判别T形截面类型", "如果 fy*As<=α1*fc*bf_*hf_，则为第一类T形截面；否则为第二类T形截面",
                               {"α1": α1, "As": As, "fc": fc, "fy": fy, "bf_": bf_, "hf_": hf_},
                               type) if 通用工具类.debug else None
        return type

    @staticmethod
    def 判别T形截面类型_截面设计(α1, M, fc, bf_, hf_, h0):
        """
        判别T形截面类型
        :param α1:
        :param M:
        :param fc:
        :param bf_:
        :param hf_:
        :param h0:
        :return:
        """
        type = "第一类T形截面" if M <= α1 * fc * bf_ * hf_ * (h0 - hf_ / 2) else "第二类T形截面"
        通用工具类.debug_print("判别T形截面类型",
                               "如果 M<=α1*fc*bf_*hf_*(h0-hf_/2)，则为第一类T形截面；否则为第二类T形截面",
                               {"α1": α1, "M": M, "fc": fc, "bf_": bf_, "hf_": hf_, "h0": h0},
                               (α1 * fc * bf_ * hf_ * (h0 - hf_ / 2), type)) if 通用工具类.debug else None
        return type

    @staticmethod
    def 正截面承载力Mu_第二类T形截面_对受拉钢筋合力点取矩_原始(α1, fc, b, bf_, hf_, h0, x):
        res = α1 * fc * b * x * (h0 - x / 2) + α1 * fc * (bf_ - b) * hf_ * (h0 - hf_ / 2)
        通用工具类.debug_print("正截面承载力Mu_对受拉钢筋合力点取矩_原始",
                               "Mu = α1 * fc * b * x * (h0 - x / 2) + α1 * fc * (bf_ - b) * hf_ * (h0 - hf_ / 2)",
                               {"α1": α1, "fc": fc, "b": b, "bf_": bf_, "hf_": hf_, "h0": h0, "x": x},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 正截面承载力Mu_第二类T形截面_对受拉钢筋合力点取矩_修正(α1, ξ, fc, b, h0, bf_, hf_):
        """
        计算正截面承载力Mu_对受拉钢筋合力点取矩_修正
        :param α1:
        :param ξ:
        :param fc:
        :param b:
        :param h0:
        :param bf_:
        :param hf_:
        :return:
        """
        res = α1 * ξ * fc * b * h0 ** 2 * (1 - 0.5 * ξ) + α1 * fc * (bf_ - b) * hf_ * (h0 - hf_ / 2)
        通用工具类.debug_print("正截面承载力Mu_对受拉钢筋合力点取矩_修正",
                               "Mu = α1 * ξ * fc * b * h0^2 * (1 - 0.5 * ξ) + α1 * fc * (bf_ - b) * hf_ * (h0 - hf_ / 2)",
                               {"α1": α1, "ξ": ξ, "fc": fc, "b": b, "h0": h0, "bf_": bf_, "hf_": hf_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 由轴力平衡计算与挑出部分翼缘形成抵抗力矩的受拉钢筋面积As2_第二类T形截面(α1, fy, fc, b, bf_, hf_):
        """
        通过轴力平衡计算与挑出部分翼缘形成抵抗力矩的受拉钢筋面积As2
        :param α1:
        :param fy:
        :param b:
        :param bf_:
        :param hf_:
        :return:
        """
        res = (α1 * fc * (bf_ - b) * hf_) / fy
        通用工具类.debug_print("由轴力平衡计算与挑出部分翼缘形成抵抗力矩的受拉钢筋面积As2",
                               "As2 = (α1 * fc * (bf_ - b) * hf_) / fy",
                               {"α1": α1, "fy": fy, "fc": fc, "b": b, "bf_": bf_, "hf_": hf_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 由弯矩平衡计算Mu2_第二类T形截面_对挑出部分翼缘中和轴取矩(fy, As2, h0, hf_):
        """
        通过弯矩平衡计算Mu2_对挑出部分翼缘中和轴取矩
        :param fy:
        :param As2:
        :param h0:
        :param hf:
        :return:
        """
        res = fy * As2 * (h0 - hf_ / 2)
        通用工具类.debug_print("由弯矩平衡计算Mu2_对挑出部分翼缘中和轴取矩",
                               "Mu2 = fy * As2 * (h0 - hf_ / 2)",
                               {"fy": fy, "As2": As2, "h0": h0, "hf_": hf_},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由Mu减Mu2计算Mu1_第二类T形截面(Mu, Mu2):
        """
        通过Mu减Mu2计算Mu1
        :param Mu:
        :param Mu2:
        :return:
        """
        res = Mu - Mu2
        通用工具类.debug_print("由Mu减Mu2计算Mu1", "Mu1 = Mu - Mu2", {"Mu": Mu, "Mu2": Mu2},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由弯矩平衡计算αs_第二类T形截面_对受拉钢筋合力点取矩(α1, Mu1, fc, b, h0):
        """
        通过弯矩平衡计算αs_对受拉钢筋合力点取矩
        :param α1:
        :param fc:
        :param b:
        :param h0:
        :param x:
        :return:
        """
        res = Mu1 / (α1 * fc * b * h0 ** 2)
        通用工具类.debug_print("由弯矩平衡计算αs_对受拉钢筋合力点取矩",
                               "αs_ = Mu1 / (α1 * fc * b * h0^2)",
                               {"α1": α1, "Mu1": Mu1, "fc": fc, "b": b, "h0": h0},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由αs计算ξ_第二类T形截面(αs):
        """
        通过αs计算ξ
        :param αs:
        :return:
        """
        res = 1 - (1 - 2 * αs) ** 0.5
        通用工具类.debug_print("由αs计算ξ_第二类T形截面", "ξ = 1 - (1 - 2 * αs)^0.5", {"αs": αs},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由ξ计算γs_第二类T形截面(ξ):
        """
        通过ξ计算γs
        :param ξ:
        :return:
        """
        res = 1 - 0.5 * ξ
        通用工具类.debug_print("由ξ计算γs_第二类T形截面", "γs = 1 - 0.5 * ξ", {"ξ": ξ},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由弯矩平衡计算As1_第二类T形截面_对受压区合力点取矩(γs, Mu1, fy, h0):
        """
        通过弯矩平衡计算As1_对受压区合力点取矩
        :param γs:
        :param Mu1:
        :param fy:
        :param h0:
        :return:
        """
        res = Mu1 / (γs * fy * h0)
        通用工具类.debug_print("由弯矩平衡计算As1_对受压区合力点取矩",
                               "As1 = Mu1 / (γs * fy * h0)",
                               {"γs": γs, "Mu1": Mu1, "fy": fy, "h0": h0},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由配筋率计算As1_第二类T形截面(ρ, b, h0):
        """
        通过配筋率计算As1
        :param ρ:
        :param b:
        :param h0:
        :return:
        """
        res = ρ * b * h0
        通用工具类.debug_print("由配筋率计算As1_第二类T形截面", "As1 = ρ * b * h0", {"ρ": ρ, "b": b, "h0": h0},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 理论配筋率ρ_第二类T形截面(α1, ξ, fc, fy):
        """
        理论配筋率ρ
        :param α1:
        :param ξ:
        :param fc:
        :param fy:
        :return:
        """
        res = α1 * ξ * fc / fy
        通用工具类.debug_print("理论配筋率ρ_第二类T形截面", "ρ = α1 * ξ * fc / fy",
                               {"α1": α1, "ξ": ξ, "fc": fc, "fy": fy},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 受拉钢筋总面积As_第二类T形截面(As1, As2):
        """
        受拉钢筋总面积As
        :param As1:
        :param As2:
        :return:
        """
        res = As1 + As2
        通用工具类.debug_print("受拉钢筋总面积As_第二类T形截面", "As = As1 + As2", {"As1": As1, "As2": As2},
                               res) if 通用工具类.debug else None

        return res

    @staticmethod
    def 由轴力平衡计算x_第二类T形截面(α1, fc, fy, As, b, bf_, hf_):
        """
        通过轴力平衡计算x_第二类T形截面
        :param α1:
        :param fc:
        :param fy:
        :param As:
        :param b:
        :param bf_:
        :param hf_:
        :return:
        """
        res = (fy * As - α1 * fc * (bf_ - b) * hf_) / (α1 * fc * b)
        通用工具类.debug_print("由轴力平衡计算x_第二类T形截面",
                               "x = (fy * As - α1 * fc * (bf_ - b) * hf_) / (α1 * fc * b)",
                               {"α1": α1, "fc": fc, "fy": fy, "As": As, "b": b, "bf_": bf_, "hf_": hf_},
                               res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 由as计算h0(h, as_):
        """
        通过as计算h0
        :param h:
        :param as_:
        :return:
        """
        h0 = h - as_
        通用工具类.debug_print("由as计算h0", "h0 = h - as_", {"h": h, "as_": as_}, h0) if 通用工具类.debug else None
        return h0


if __name__ == '__main__':
    # 判断类型
    α1 = T形截面受弯构件正截面承载力计算_工具类.简化系数α1(C=30)
    h0 = T形截面受弯构件正截面承载力计算_工具类.由as计算h0(0.7, 0.06)
    T形截面受弯构件正截面承载力计算_工具类.判别T形截面类型_截面设计(α1, 650000, 14.3e6, 0.6, 0.12, h0)  # 第二类T形截面
    As2 = T形截面受弯构件正截面承载力计算_工具类.由轴力平衡计算与挑出部分翼缘形成抵抗力矩的受拉钢筋面积As2_第二类T形截面(
        α1,
        300e6,
        14.3e6,
        0.3,
        0.6,
        0.12)
    Mu2 = T形截面受弯构件正截面承载力计算_工具类.由弯矩平衡计算Mu2_第二类T形截面_对挑出部分翼缘中和轴取矩(300e6, As2,
                                                                                                          h0, 0.12)
    Mu1 = T形截面受弯构件正截面承载力计算_工具类.由Mu减Mu2计算Mu1_第二类T形截面(650000, Mu2)
    αs = T形截面受弯构件正截面承载力计算_工具类.由弯矩平衡计算αs_第二类T形截面_对受拉钢筋合力点取矩(α1, Mu1, 14.3e6,
                                                                                                    0.3, h0)
    ξ = T形截面受弯构件正截面承载力计算_工具类.由αs计算ξ_第二类T形截面(αs)
    γs = T形截面受弯构件正截面承载力计算_工具类.由ξ计算γs_第二类T形截面(ξ)
    As1 = T形截面受弯构件正截面承载力计算_工具类.由弯矩平衡计算As1_第二类T形截面_对受压区合力点取矩(γs, Mu1, 300e6, h0)
    ρ = T形截面受弯构件正截面承载力计算_工具类.理论配筋率ρ_第二类T形截面(α1, ξ, 14.3e6, 300e6)
    As11 = T形截面受弯构件正截面承载力计算_工具类.由配筋率计算As1_第二类T形截面(ρ, 0.3, h0)
    As = T形截面受弯构件正截面承载力计算_工具类.受拉钢筋总面积As_第二类T形截面(As1, As2)
    通用工具类.判断是否超筋(ξ, 0.55)
    通用工具类.判断是否少筋(通用工具类.实际配筋率ρ1(As, 通用工具类.矩形截面面积(0.3, 0.7)),
                            通用工具类.最小配筋率ρmin(1.43e6, 300e6))
    print(As)
    print(As1)
    print(As11)
    print(As2)
