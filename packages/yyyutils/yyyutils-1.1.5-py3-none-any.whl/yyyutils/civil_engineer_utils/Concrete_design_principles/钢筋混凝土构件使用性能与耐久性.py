from yyyutils.math_utils.math_utils import MathUtils
import re

PI = MathUtils.PI


class 通用工具类:
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
                if isinstance(value, float):
                    value = f"{value:.{decimal_places}f}"
                # r'\b' 确保只匹配完整的变量名
                new_formula = re.sub(r'\b' + re.escape(key) + r'\b', str(value), new_formula)
        if formula is None:
            new_formula = description
        if isinstance(result, float):
            print(f"计算结果：{new_formula} = {result:.{decimal_places}f}")
        else:
            print(f"计算结果：{new_formula} = {result}")

    @staticmethod
    def 受压区翼缘加强系数γf_(bf_, b, hf_, h0):
        """
        受压区翼缘加强系数γf_：
        :param bf_:
        :param b:
        :param hf_:
        :param h0:
        :return:
        """
        γf_ = (bf_ - b) * hf_ / (b * h0)
        通用工具类.debug_print(description='受压区翼缘加强系数γf_', formula='γf_ = (bf_ - b) * hf_ / (b * h0)',
                               params={'bf_': bf_, 'b': b, 'hf_': hf_, 'h0': h0},
                               result=γf_) if 通用工具类.debug else None
        return γf_

    @staticmethod
    def 按有效受拉区混凝土截面面积计算的纵向受拉钢筋配筋率ρte(As, Ate, Ap=0):
        """
        按有效受拉区混凝土截面面积计算的纵向受拉钢筋配筋率ρte：
        :param As:
        :param Ate:
        :param Ap:
        :return:
        """
        ρte = (As + Ap) / Ate
        通用工具类.debug_print(description='按有效受拉区混凝土截面面积计算的纵向受拉钢筋配筋率ρte',
                               formula='ρte = (As + Ap) / Ate',
                               params={'As': As, 'Ate': Ate, 'Ap': Ap},
                               result=ρte) if 通用工具类.debug else None
        if ρte < 0.01:
            ρte = MathUtils.limit_value(ρte, 0.01)
            if 受拉裂缝控制工具类.debug:
                print(f"结果小于0.01，取0.01")
                print(f"结果：{ρte:.3f}")
        return ρte

    @staticmethod
    def 纵向受拉钢筋应变不均匀系数ψ_原始(Mcr, M):
        """
        纵向受拉钢筋应变不均匀系数ψ：
        :param Mcr:
        :param M:
        :return:
        """
        ψ = 1.1 * (1 - Mcr / M)
        通用工具类.debug_print(description='纵向受拉钢筋应变不均匀系数ψ_原始', formula='ψ = 1.1 * (1 - Mcr / M)',
                               params={'Mcr': Mcr, 'M': M},
                               result=ψ) if 通用工具类.debug else None
        return ψ

    @staticmethod
    def 弹模比αE(Es, Ec):
        """
        弹模比αE：
        :param Es:
        :param Ec:
        :return:
        """
        αE = Es / Ec
        通用工具类.debug_print(description='弹模比αE', formula='αE = Es / Ec',
                               params={'Es': Es, 'Ec': Ec},
                               result=αE) if 通用工具类.debug else None
        return αE

    @staticmethod
    def 纵向受拉钢筋应变不均匀系数ψ_修正(ftk, ρte, σsq):
        """
        纵向受拉钢筋应变不均匀系数ψ：
        :param ftk:
        :param ρte:
        :param σsq:
        :return:
        """
        ψ = 1.1 - 0.65 * ftk / (ρte * σsq)
        通用工具类.debug_print(description='纵向受拉钢筋应变不均匀系数ψ_修正',
                               formula='ψ = 1.1 - 0.65 * ftk / (ρte * σsq)',
                               params={'ftk': ftk, 'ρte': ρte, 'σsq': σsq},
                               result=ψ) if 通用工具类.debug else None
        if ψ > 1 or ψ < 0.2:
            ψ = MathUtils.limit_value(ψ, 0.2, 1)
            if 受拉裂缝控制工具类.debug:
                print(f"结果超出范围，取0.2~1")
                print(f"结果：{ψ:.3f}")
        return ψ

    @staticmethod
    def 理论配筋率ρ(As, b, h0):
        """
        理论配筋率ρ：
        :param As:
        :param b:
        :param h0:
        :return:
        """
        ρ = As / (b * h0)
        通用工具类.debug_print(description='理论配筋率ρ', formula='ρ = As / (b * h0)',
                               params={'As': As, 'b': b, 'h0': h0},
                               result=ρ) if 通用工具类.debug else None
        return ρ


class 受拉裂缝控制工具类(通用工具类):
    @staticmethod
    def 最大裂缝宽度ωmax_荷载准永久组合_考虑长期作用_混规(αcr, ψ, σsq, Es, cs, deq, ρte):
        """
        适用条件：矩形、T形、倒T形、I形截面钢筋混凝土受拉、受弯、偏心受压构件。
        :param αcr:
        :param ψ:
        :param σsq:
        :param Es:
        :param cs:
        :param deq:
        :param ρte:
        :return:
        """
        res = αcr * ψ * σsq / Es * (1.9 * cs + 0.08 * deq / ρte)
        通用工具类.debug_print(description='最大裂缝宽度ωmax_荷载准永久组合_考虑长期作用_混规',
                               formula='ωmax = αcr * ψ * σsq / Es * (1.9 * cs + 0.08 * deq / ρte)',
                               params={'αcr': αcr, 'ψ': ψ, 'σsq': σsq, 'Es': Es, 'cs': cs, 'deq': deq, 'ρte': ρte},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 开裂截面受拉钢筋应力σsq(Mq, As, γs, h0):
        """
        开裂截面受拉钢筋应力σsq：
        :param Mq:
        :param As:
        :param γs:
        :param h0:
        :return:
        """
        σsq = Mq / (As * γs * h0)
        通用工具类.debug_print(description='开裂截面受拉钢筋应力σsq', formula='σsq = Mq / (As * γs * h0)',
                               params={'Mq': Mq, 'As': As, 'γs': γs, 'h0': h0},
                               result=σsq) if 通用工具类.debug else None

        return σsq

    @staticmethod
    def 开裂截面内力臂长度系数γs(αE, ρ, γf_):
        """
        开裂截面内力臂长度系数γs：
        :param αE:
        :param ρ:
        :param γf_:
        :return:
        """
        γs = 1 - 0.4 * (αE * ρ) ** 0.5 / (1 + 2 * γf_)
        通用工具类.debug_print(description='开裂截面内力臂长度系数γs',
                               formula='γs = 1 - 0.4 * (αE * ρ)^0.5 / (1 + 2 * γf_)',
                               params={'αE': αE, 'ρ': ρ, 'γf_': γf_},
                               result=γs) if 通用工具类.debug else None
        return γs

    @staticmethod
    def 构件受力特征系数αcr(defualt_choice=None):
        """
        受力特征系数：
        轴心受拉构件：αcr = 2.7
        偏心受拉构件：αcr = 2.4
        受弯构件：αcr = 1.9
        偏心受压构件：αcr = 1.9
        """
        αcr = 0
        if defualt_choice is not None:
            choice = str(defualt_choice)
        else:
            choice = input("请输入构件类型（1.轴心受拉；2.偏心受拉；3.受弯；4.偏心受压）：")
        if choice == "1":
            αcr = 2.7
        elif choice == "2":
            αcr = 2.4
        elif choice == "3":
            αcr = 1.9
        elif choice == "4":
            αcr = 1.9
        else:
            print("输入错误，请重新输入！")
        通用工具类.debug_print(description='构件受力特征系数αcr',
                               params={'构件类型': choice},
                               result=αcr) if 通用工具类.debug else None
        return αcr

    @staticmethod
    def 最外层纵向钢筋外边缘至受拉底边的距离cs(cs_):
        """
        最外层纵向钢筋外边缘至受拉底边的距离：
        """
        cs = MathUtils.limit_value(cs_, 0.02, 0.065)
        通用工具类.debug_print(description='最外层纵向钢筋外边缘至受拉底边的距离cs', formula='cs = 0.02~0.065',
                               params={'cs_': cs_},
                               result=cs) if 通用工具类.debug else None
        return cs

    @staticmethod
    def 等效直径deq(*i组直径_数量_粘结特性系数):
        """
        查阅表9.2
        参数都以（直径，数量，粘结特性系数）为一组
        :param i组直径_数量_粘结特性系数:
        :return:
        """
        temp1 = 0
        temp2 = 0
        for t in i组直径_数量_粘结特性系数:
            d, n, ν = t
            temp1 += n * d ** 2
            temp2 += n * ν * d
        deq = temp1 / temp2
        通用工具类.debug_print(description='等效直径deq', formula='deq = Σn * d^2 / Σn * ν * d',
                               params={'i组直径_数量_粘结特性系数': i组直径_数量_粘结特性系数},
                               result=deq) if 通用工具类.debug else None
        return deq


class 构件的刚度与变形控制工具类(通用工具类):
    """
    所有单位均为国际单位
    """

    @staticmethod
    def 梁的短期刚度Bs(Es, As, h0, ψ, αE, ρ, γf_):
        """
        梁的短期刚度Bs：
        :param Es:
        :param As:
        :param h0:
        :param ψ:
        :param αE:
        :param ρ:
        :param γf_:
        :return:
        """
        Bs = Es * As * h0 ** 2 / (1.15 * ψ + 0.2 + 6 * αE * ρ / (1 + 3.5 * γf_))
        通用工具类.debug_print(description='梁的短期刚度Bs',
                               formula='Bs = Es * As * h0^2 / (1.15 * ψ + 0.2 + 6 * αE * ρ / (1 + 3.5 * γf_))',
                               params={'Es': Es, 'As': As, 'h0': h0, 'ψ': ψ, 'αE': αE, 'ρ': ρ, 'γf_': γf_},
                               result=Bs) if 通用工具类.debug else None
        return Bs

    @staticmethod
    def 受拉钢筋合力点到受压区边缘的距离h0(h, αs):
        """
        受拉钢筋合力点到受压区边缘的距离h0：
        :param h:
        :param αs:
        :return:
        """
        h0 = h - αs
        通用工具类.debug_print(description='受拉钢筋合力点到受压区边缘的距离h0', formula='h0 = h - αs',
                               params={'h': h, 'αs': αs},
                               result=h0) if 通用工具类.debug else None
        return h0

    @staticmethod
    def 弹模比αE(Es, Ec):
        """
        弹模比αE：
        :param Es:
        :param Ec:
        :return:
        """
        αE = Es / Ec
        通用工具类.debug_print(description='弹模比αE', formula='αE = Es / Ec',
                               params={'Es': Es, 'Ec': Ec},
                               result=αE) if 通用工具类.debug else None
        return αE

    @staticmethod
    def 理论配筋率ρ(As, b, h0):
        """
        配筋率ρ：
        :param As:
        :param b:
        :param h0:
        :return:
        """
        ρ = As / (b * h0)
        通用工具类.debug_print(description='理论配筋率ρ', formula='ρ = As / (b * h0)',
                               params={'As': As, 'b': b, 'h0': h0},
                               result=ρ) if 通用工具类.debug else None
        return ρ

    @staticmethod
    def 梁的长期刚度B(Bs, θ):
        """
        梁的长期刚度B：
        :param Bs:
        :param θ:
        :return:
        """
        B = Bs / θ
        通用工具类.debug_print(description='梁的长期刚度B', formula='B = Bs / θ',
                               params={'Bs': Bs, 'θ': θ},
                               result=B) if 通用工具类.debug else None
        return B

    @staticmethod
    def 放大系数θ(ρ_, ρ, 是否为翼缘受拉的倒T形梁=False):
        """
        放大系数θ：
        :param ρ_:
        :param ρ:
        :return:
        """
        bigger = 1.2 if 是否为翼缘受拉的倒T形梁 else 1
        θ = (2 - 0.4 * (ρ_ / ρ)) * bigger
        通用工具类.debug_print(description='放大系数θ', formula='θ = (2 - 0.4 * (ρ_ / ρ)) * bigger',
                               params={'ρ_': ρ_, 'ρ': ρ, '是否为翼缘受拉的倒T形梁': 是否为翼缘受拉的倒T形梁},
                               result=θ) if 通用工具类.debug else None
        return θ

    @staticmethod
    def 简支梁的梁跨中挠度f(Mq, l0, B):
        """
        简支梁的梁跨中挠度：
        :param Mq:
        :param l0:
        :param B:
        :return:
        """
        f = (5 / 48) * Mq * l0 / B
        通用工具类.debug_print(description='简支梁的梁跨中挠度f', formula='f = (5 / 48) * Mq * l0 / B',
                               params={'Mq': Mq, 'l0': l0, 'B': B},
                               result=f) if 通用工具类.debug else None
        return f


if __name__ == '__main__':
    受拉裂缝控制工具类.构件受力特征系数αcr()
