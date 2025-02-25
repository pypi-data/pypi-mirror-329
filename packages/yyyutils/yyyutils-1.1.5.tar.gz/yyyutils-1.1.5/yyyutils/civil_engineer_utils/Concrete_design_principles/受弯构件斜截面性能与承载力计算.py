from yyyutils.math_utils.math_utils import MathUtils
import re

PI = MathUtils.PI


class 通用工具类:
    """
    单位均使用国际单位
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
    def 受拉钢筋合力点到受压区边缘距离h0(h, as_):
        """
        受拉钢筋合力点到受压区边缘距离h0
        :param h:
        :param as_:
        :return:
        """
        res = h - as_
        通用工具类.debug_print(description='受拉钢筋合力点到受压区边缘距离h0', formula='h0 = h - as_',
                               params={'h': h, 'as_': as_},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 箍筋各肢全截面面积Asv(n, Asv1):
        """
        箍筋各肢全截面面积Asv
        :param n:
        :param Asv1:
        :return:
        """
        Asv = n * Asv1
        通用工具类.debug_print(description='箍筋各肢全截面面积Asv', formula='Asv = n * Asv1',
                               params={'n': n, 'Asv1': Asv1},
                               result=Asv) if 通用工具类.debug else None
        return Asv

    @staticmethod
    def 最小箍筋配筋率ρsvmin(ft, fyv):
        """
        最小箍筋配筋率ρsvmin
        :param ft:
        :param fyv:
        :return:
        """
        ρsvmin = 0.24 * ft / fyv
        通用工具类.debug_print(description='最小箍筋配筋率ρsvmin', formula='ρsvmin = 0.24 * ft / fyv',
                               params={'ft': ft, 'fyv': fyv},
                               result=ρsvmin) if 通用工具类.debug else None
        return ρsvmin

    @staticmethod
    def hw(h0, hf_):
        """
        hw
        :param h0:
        :param hf_:
        :return:
        """
        hw = h0 - hf_
        通用工具类.debug_print(description='hw', formula='hw = h0 - hf_',
                               params={'h0': h0, 'hf_': hf_},
                               result=hw) if 通用工具类.debug else None
        return hw

    @staticmethod
    def 判断是否为斜拉破坏(ρsv, ρsvmin):
        """
        判断是否为斜拉破坏
        :param ρsv:
        :param ρsvmin:
        :return:
        """
        if ρsv < ρsvmin:
            res = True
        else:
            res = False
        通用工具类.debug_print(description='判断是否为斜拉破坏', formula='如果 ρsv < ρsvmin，则为斜拉破坏',
                               params={'ρsv': ρsv, 'ρsvmin': ρsvmin},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 判断是否为斜压破坏(Vu, hw, b, βc, fc, h0):
        """
        判断是否为斜压破坏
        :param hw:
        :param b:
        :param βc:
        :param fc:
        :param h0:
        :return:
        """
        if hw / b <= 4:
            res = Vu > 0.25 * βc * fc * b * h0
            通用工具类.debug_print(description='判断是否为斜压破坏',
                                   formula='如果 Vu > 0.25 * βc * fc * b * h0，则为斜压破坏',
                                   params={'Vu': Vu, 'βc': βc, 'fc': fc, 'b': b, 'h0': h0},
                                   result=res) if 通用工具类.debug else None
        if hw / b >= 6:
            res = Vu > 0.2 * βc * fc * b * h0
            通用工具类.debug_print(description='判断是否为斜压破坏',
                                   formula='如果 4 < hw / b < 6，则 Vu > 0.025 * (14 - hw / b) * βc * fc * b * h0',
                                   params={'Vu': Vu, 'βc': βc, 'fc': fc, 'b': b, 'h0': h0, 'hw': hw},
                                   result=res) if 通用工具类.debug else None
        if 4 < hw / b < 6:
            res = Vu > 0.025 * (14 - hw / b) * βc * fc * b * h0
            通用工具类.debug_print(description='判断是否为斜压破坏',
                                   formula='如果 4 < hw / b < 6，则 Vu > 0.025 * (14 - hw / b) * βc * fc * b * h0',
                                   params={'Vu': Vu, 'βc': βc, 'fc': fc, 'b': b, 'h0': h0, 'hw': hw},
                                   result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 计算剪跨比λ(a, h0):
        """
        计算剪跨比λ
        :param a:
        :param h0:
        :return:
        """
        λ = a / h0
        通用工具类.debug_print(description='计算剪跨比λ', formula='λ = a / h0',
                               params={'a': a, 'h0': h0},
                               result=λ) if 通用工具类.debug else None
        return λ

    @staticmethod
    def 广义剪跨比λ(M, V, h0):
        """
        广义剪跨比λ
        :param M:
        :param V:
        :param h0:
        :return:
        """
        λ = M / (V * h0)
        通用工具类.debug_print(description='广义剪跨比λ', formula='λ = M / (V * h0)',
                               params={'M': M, 'V': V, 'h0': h0},
                               result=λ) if 通用工具类.debug else None
        return λ


class 受弯构件斜截面性能与承载力计算工具类(通用工具类):
    """
    受弯构件斜截面性能与承载力计算工具类
    """

    @staticmethod
    def 混凝土强度影响系数βc(C):
        """
         混凝土强度影响系数βc
        :param C:
        :return:
        """
        if not isinstance(C, int):
            raise TypeError("混凝土强度等级C必须为整数！")

        if C <= 50:
            βc = 1.0
        if C > 80:
            raise ValueError("混凝土强度等级超出范围C80，不能使用内插法计算！")
        if 50 < C <= 80:
            βc = MathUtils.linear_interpolate(50, 80, 1.0, 0.8, C)
        通用工具类.debug_print(description='混凝土强度影响系数βc', formula='βc = 1.0',
                               params={'C': C},
                               result=βc) if 通用工具类.debug else None
        return βc

    @staticmethod
    def 斜截面最大剪力设计值Vu(Vc, Vsv=0, Vsb=0):
        """
        最大剪力设计值Vu
        :param Vc:
        :param Vsv:
        :param Vsb:
        :return:
        """
        Vu = Vc + Vsv + Vsb
        通用工具类.debug_print(description='最大剪力设计值Vu', formula='Vu = Vc + Vsv + Vsb',
                               params={'Vc': Vc, 'Vsv': Vsv, 'Vsb': Vsb},
                               result=Vu) if 通用工具类.debug else None
        return Vu

    @staticmethod
    def 剪压区混凝土_无腹筋梁_一般梁_抗剪能力Vc(ft, b, h0):
        """
        剪压区混凝土_无腹筋梁_一般梁_抗剪能力Vc
        :param ft:
        :param b:
        :param h0:
        :return:
        """
        Vc = 0.7 * ft * b * h0
        通用工具类.debug_print(description='剪压区混凝土_无腹筋梁_一般梁_抗剪能力Vc', formula='Vc = 0.7 * ft * b * h0',
                               params={'ft': ft, 'b': b, 'h0': h0},
                               result=Vc) if 通用工具类.debug else None
        return Vc

    @staticmethod
    def 剪压区混凝土_无腹筋梁_集中荷载梁_抗剪能力Vc(λ, ft, b, h0):
        """
        剪压区混凝土_无腹筋梁_集中荷载梁_抗剪能力Vc
        :param λ:
        :param ft:
        :param b:
        :param h0:
        :return:
        """
        Vc = 1.75 / (λ + 1) * ft * b * h0
        通用工具类.debug_print(description='剪压区混凝土_无腹筋梁_集中荷载梁_抗剪能力Vc',
                               formula='Vc = 1.75 / (λ + 1) * ft * b * h0',
                               params={'λ': λ, 'ft': ft, 'b': b, 'h0': h0},
                               result=Vc) if 通用工具类.debug else None
        return Vc

    @staticmethod
    def 箍筋配筋率ρsv(Asv, b, s):
        """
        箍筋配筋率ρsv
        :param Asv:
        :param b:
        :param s:
        :return:
        """
        ρsv = Asv / (b * s)
        通用工具类.debug_print(description='箍筋配筋率ρsv', formula='ρsv = Asv / (b * s)',
                               params={'Asv': Asv, 'b': b, 's': s},
                               result=ρsv) if 通用工具类.debug else None
        return ρsv

    @staticmethod
    def 与斜裂缝相交的箍筋抗剪能力Vsv(h0, s, Asv, fyv):
        """
        与斜裂缝相交的箍筋抗剪能力Vsv
        :param h0:
        :param s:
        :param Asv:
        :param fyv:
        :return:
        """
        Vsv = h0 / s * Asv * fyv
        通用工具类.debug_print(description='与斜裂缝相交的箍筋抗剪能力Vsv', formula='Vsv = h0 / s * Asv * fyv',
                               params={'h0': h0, 's': s, 'Asv': Asv, 'fyv': fyv},
                               result=Vsv) if 通用工具类.debug else None
        return Vsv

    @staticmethod
    def 与斜裂缝相交的弯起钢筋抗剪能力Vsb(fy, Asb, αsb):
        """
        与斜裂缝相交的弯起钢筋抗剪能力Vsb
        :param fy:
        :param Asb:
        :param αsb:
        :return:
        """
        Vsb = 0.8 * fy * Asb * MathUtils.sin(αsb)
        通用工具类.debug_print(description='与斜裂缝相交的弯起钢筋抗剪能力Vsb',
                               formula='Vsb = 0.8 * fy * Asb * sin(αsb)',
                               params={'fy': fy, 'Asb': Asb, 'αsb': αsb},
                               result=Vsb) if 通用工具类.debug else None
        return Vsb

    @staticmethod
    def 判断是否需要按计算设置腹筋(V, Vc):
        """
        判断是否需要设置腹筋
        :param V:
        :param Vc:
        :return:
        """
        if V < Vc:
            res = False
        else:
            res = True
        通用工具类.debug_print(description='判断是否需要按计算设置腹筋', formula='如果 V < Vc，则不需要按计算设置腹筋',
                               params={'V': V, 'Vc': Vc},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 与斜裂缝相交的箍筋抗剪能力Vsv_由V减Vc减Vsb(V, Vc, Vsb=0):
        """
        与斜裂缝相交的箍筋抗剪能力Vsv_V减Vc减Vsb
        :param V:
        :param Vc:
        :param Vsb:
        :return:
        """
        Vsv = V - Vc - Vsb
        通用工具类.debug_print(description='与斜裂缝相交的箍筋抗剪能力Vsv_V减Vc减Vsb', formula='Vsv = V - Vc - Vsb',
                               params={'V': V, 'Vc': Vc, 'Vsb': Vsb},
                               result=Vsv) if 通用工具类.debug else None
        return Vsv

    @staticmethod
    def 箍筋间距s_由Vsv(h0, Asv, fyv, Vsv):
        """
        箍筋间距s_由Vsv
        :param h0:
        :param Asv:
        :param fyv:
        :param Vsv:
        :return:
        """
        s = h0 * Asv * fyv / Vsv
        通用工具类.debug_print(description='箍筋间距s_由Vsv', formula='s = h0 * Asv * fyv / Vsv',
                               params={'h0': h0, 'Asv': Asv, 'fyv': fyv, 'Vsv': Vsv},
                               result=s) if 通用工具类.debug else None
        return s

    @staticmethod
    def 正截面抗弯承载力Mu正(fy, As1, z, Asb, zsb):
        """
        正截面抗弯承载力Mu正
        :param fy:
        :param As1:
        :param z:
        :param Asb:
        :param zsb:
        :return:
        """
        Mu = fy * As1 * z + fy * Asb * zsb
        通用工具类.debug_print(description='正截面抗弯承载力Mu正', formula='Mu = fy * As1 * z + fy * Asb * zsb',
                               params={'fy': fy, 'As1': As1, 'z': z, 'Asb': Asb, 'zsb': zsb},
                               result=Mu) if 通用工具类.debug else None
        return Mu


if __name__ == '__main__':
    as_ = 0.04
    ft = 1.1e6
    fc = 9.6e6
    fyv = 270e6
    b, h = 0.2, 0.4
    s = 0.2
    n, Asv1 = 2, 50.3e-6
    βc = 受弯构件斜截面性能与承载力计算工具类.混凝土强度影响系数βc(20)
    h0 = 受弯构件斜截面性能与承载力计算工具类.受拉钢筋合力点到受压区边缘距离h0(h, as_)
    Vc = 受弯构件斜截面性能与承载力计算工具类.剪压区混凝土_无腹筋梁_一般梁_抗剪能力Vc(ft, b, h0)
    Asv = 受弯构件斜截面性能与承载力计算工具类.箍筋各肢全截面面积Asv(n, Asv1)
    Vsv = 受弯构件斜截面性能与承载力计算工具类.与斜裂缝相交的箍筋抗剪能力Vsv(h0, s, Asv, fyv)
    Vu = 受弯构件斜截面性能与承载力计算工具类.斜截面最大剪力设计值Vu(Vc, Vsv)
    ρsv = 受弯构件斜截面性能与承载力计算工具类.箍筋配筋率ρsv(Asv, b, s)
    ρsvmin = 受弯构件斜截面性能与承载力计算工具类.最小箍筋配筋率ρsvmin(ft, fyv)
    受弯构件斜截面性能与承载力计算工具类.判断是否为斜压破坏(Vu, h, b, βc, fc, h0)
    受弯构件斜截面性能与承载力计算工具类.判断是否为斜拉破坏(ρsv, ρsvmin)
