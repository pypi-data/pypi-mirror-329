from yyyutils.math_utils.math_utils import MathUtils


class BaseCulvert:
    def __init__(self, g=9.8, B=None, b=None, delta=None, H=None, h=None, p=None, p_=None, z=None, delta_h=None,
                 alpha=1,
                 debug=False):
        """
        基本参数
        :param B: 上游渠道宽度
        :param b: 堰宽
        :param delta: 堰顶厚度
        :param H: 堰前水头
        :param h: 下游水深
        :param p: 堰上游坎高
        :param p_: 堰下游坎高
        :param z: 堰上下游水位差
        :param g: 重力加速度
        :param alpha: 动能修正系数
        :param debug: 是否输出调试信息
        """
        self.g = g
        self.B = B
        self.b = b
        self.delta = delta
        self.H = H
        self.h = h
        self.p = p
        self.p_ = p_
        self.z = z
        self.alpha = alpha
        self.a1 = 0.19
        self.a2 = 0.1
        self.debug = debug
        self.delta_h = delta_h
        if delta_h is None and h is not None and p_ is not None:
            self.delta_h = self.h - self.p_

    class ThinWallWeir:
        def __init__(self, base_culvert_instance):
            self.base_culvert_instance = base_culvert_instance

        def __getattr__(self, item):
            return getattr(self.base_culvert_instance, item)

        class RectangularWeir:
            def __init__(self, thin_wall_weir_instance):
                self.thin_wall_weir_instance = thin_wall_weir_instance

            def __getattr__(self, item):
                return getattr(self.thin_wall_weir_instance, item)

            def Q_by_m0(self, m0):
                """
                计算流量，无侧向收缩
                :return: 流量
                """
                Q = m0 * self.b * (2 * self.g) ** 0.5 * self.H ** 1.5
                if self.debug:
                    print(f"理论公式: m0 * b *√(2g) * H^1.5")
                    print(f"代入计算: {m0} * {self.b} * √(2*{self.g}) * {self.H}^1.5")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def Q_by_mc(self, mc):
                """
                计算流量，侧向收缩
                :return: 流量
                """
                Q = mc * self.b * (2 * self.g) ** 0.5 * self.H ** 1.5
                if self.debug:
                    print(f"理论公式: mc * b *√(2g) * H^1.5")
                    print(f"代入计算: {mc} * {self.b} * √(2*{self.g}) * {self.H}^1.5")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def Q_by_sigma_m0(self, sigma, m0):
                Q = sigma * m0 * self.b * (2 * self.g) ** 0.5 * self.H ** 1.5
                if self.debug:
                    print(f"理论公式: sigma*m0*b*√(2g)*H^1.5")
                    print(f"代入计算: {sigma}*{m0}*{self.b}*√(2*{self.g})*{self.H}^1.5")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def sigma_by_bazant(self):
                sigma = 1.05 * (1 + 0.2 * self.delta_h / self.p_) * (self.z / self.H) ** (1 / 3)
                if self.debug:
                    print(f"Bazant公式: 1.05*(1+0.2*delta_h/p_)*(z/H)^(1/3)")
                    print(f"代入计算: 1.05*(1+0.2*({self.delta_h}/{self.p_})*({self.z}/{self.H})^(1/3)")
                    print(f"sigma计算结果: {round(sigma, 3)}")
                return sigma

            def mc(self):
                mc = (0.405 + 0.0027 / self.H - 0.03 * (self.B - self.b) / self.H) * (
                        1 + 0.55 * (self.B / self.b) ** 2 * (self.H / (self.H + self.p)) ** 2)
                if self.debug:
                    print(f"Bazant公式: (0.405+0.0027/H-0.03*(B-b)/H)*(1+0.55*(B/b)^2*(H/(H+p))^2)")
                    print(
                        f"代入计算: (0.405+0.0027/{self.H}-0.03*({self.B}-{self.b})/{self.H})*(1+0.55*({self.B}/{self.b})^2*({self.H}/({self.H}+{self.p}))^2)")
                    print(f"mc计算结果: {round(mc, 3)}")
                return mc

            def m0_by_Rehbock(self):
                m0 = 0.403 + 0.053 * self.H / self.p
                if self.debug:
                    print(f"Rehbock公式: 0.403+0.053*H/p")
                    print(f"代入计算: 0.403+0.053*{self.H}/{self.p}")
                    print(f"m0计算结果: {round(m0, 3)}")
                return m0

            def m0_by_Bazant(self):
                m0 = (0.405 + 0.0027 / self.H) * (1 + 0.55 * (self.B / self.b) ** 2 * (self.H / (self.H + self.p)) ** 2)
                if self.debug:
                    print(f"Bazant公式: (0.405+0.0027/H)*(1+0.55*(B/b)^2*(H/(H+p))^2)")
                    print(
                        f"代入计算: (0.405+0.0027/{self.H})*(1+0.55*({self.B}/{self.b})^2*({self.H}/({self.H}+{self.p}))^2)")
                    print(f"m0计算结果: {round(m0, 3)}")
                return m0

            def H_by_m0(self, m0):
                H = (self.Q / (m0 * self.b * (2 * self.g) ** 0.5)) ** (1 / 1.5)
                if self.debug:
                    print(f"理论公式: Q/(m0*b*√(2g))^(2/3)")
                    print(f"代入计算: {self.Q}/({m0}*{self.b}*√(2*{self.g}))^(2/3)")
                    print(f"H计算结果: {round(H, 3)}")
                return H

    class WideCrestedWeir:
        def __init__(self, base_culvert_instance):
            self.base_culvert_instance = base_culvert_instance

        def __getattr__(self, item):
            return getattr(self.base_culvert_instance, item)

        class RectangularWeir:
            def __init__(self, wide_crested_weir_instance):
                self.wide_crested_weir_instance = wide_crested_weir_instance

            def __getattr__(self, item):
                return getattr(self.wide_crested_weir_instance, item)

            def judge_weir_type(self):
                """
                需要在base_culvert_instance中设置b, B, H,p_
                :return:
                """
                type2, type3 = '', ''
                try:
                    if self.delta_h is not None:
                        if 0.8 * self.H > self.delta_h:
                            type2 = '自由式'
                        else:
                            type2 = '淹没式'
                    if self.b is not None and self.B is not None:
                        if self.b < self.B:
                            type3 = '侧收缩'
                        elif self.b == self.B:
                            type3 = '无侧收缩'
                        else:
                            pass
                except ValueError as e:
                    pass
                if self.debug:
                    print(f"堰流类型: 宽顶堰 {type2} {type3}")
                return type2, type3

            def Q_by_H0_free_weir_no_side_contraction(self, m, H0=None):
                Q = m * self.b * (2 * self.g) ** 0.5 * H0 ** 1.5
                if self.debug:
                    print(f"理论公式: m*b*√(2g)*H0^1.5")
                    print(f"代入计算: {m}*{self.b}*√(2*{self.g})*{H0}^1.5")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def Q_by_sigma_H0_submerged_weir_no_side_contraction(self, m, sigma, H0):
                Q = sigma * m * self.b * (2 * self.g) ** 0.5 * H0 ** 1.5
                if self.debug:
                    print(f"理论公式: sigma*m*b*√(2g)*H0^1.5")
                    print(f"代入计算: {sigma}*{m}*{self.b}*√(2*{self.g})*{H0}^1.5")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def Q_by_H0_free_weir_side_contraction(self, m, epsilon, H0):
                Q = m * epsilon * self.b * (2 * self.g) ** 0.5 * H0 ** 1.5
                if self.debug:
                    print(f"理论公式: m*epsilon*b*√(2g)*H0^1.5*(1+0.05*(B/b)^2)")
                    print(f"代入计算: {m}*{epsilon}*{self.b}*√(2*{self.g})*{H0}^1.5*(1+0.05*({self.B}/{self.b})^2)")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def Q_by_sigma_H0_submerged_weir_side_contraction(self, m, epsilon, sigma, H0):
                Q = sigma * m * epsilon * self.b * (2 * self.g) ** 0.5 * H0 ** 1.5
                if self.debug:
                    print(f"理论公式: sigma*m*epsilon*b*√(2g)*H0^1.5*(1+0.05*(B/b)^2)")
                    print(
                        f"代入计算: {sigma}*{m}*{epsilon}*{self.b}*√(2*{self.g})*{H0}^1.5*(1+0.05*({self.B}/{self.b})^2)")
                    print(f"Q计算结果: {round(Q, 3)}")
                return Q

            def epsilon_right_angle_edge_inlet(self):
                h_ = self.p / self.H
                if self.debug:
                    print(f"理论公式: p/H")
                    print(f"代入计算: {self.p}/{self.H}")
                    print(f"h_计算结果: {round(h_, 3)}")
                epsilon = 1 - self.a1 / (0.2 + h_) ** (1 / 3) * (self.b / self.B) ** (1 / 4) * (1 - self.b / self.B)
                if self.debug:
                    print(f"理论公式: 1-a1/(0.2+h_)^(1/3)*(b/B)^(1/4)*(1-b/B)")
                    print(
                        f"代入计算: 1-{self.a1}/({0.2}+{h_})^({1 / 3})*({self.b}/{self.B})^({1 / 4})*(1-{self.b}/{self.B})")
                    print(f"epsilon计算结果: {round(epsilon, 3)}")
                return epsilon

            def epsilon_rounded_edge_inlet(self):
                h_ = self.p / self.H
                if self.debug:
                    print(f"理论公式: p/H")
                    print(f"代入计算: {self.p}/{self.H}")
                    print(f"h_计算结果: {round(h_, 3)}")
                epsilon = 1 - self.a2 / (0.2 + h_) ** (1 / 3) * (self.b / self.B) ** (1 / 4) * (1 - self.b / self.B)
                if self.debug:
                    print(f"理论公式: 1-a2/(0.2+h_)^(1/3)*(b/B)^(1/4)*(1-b/B)")
                    print(
                        f"代入计算: 1-{self.a2}/({0.2}+{h_})^({1 / 3})*({self.b}/{self.B})^({1 / 4})*(1-{self.b}/{self.B})")
                    print(f"epsilon计算结果: {round(epsilon, 3)}")
                return epsilon

            def v0(self, Q):
                v0 = Q / (self.b * (self.H + self.p))
                if self.debug:
                    print(f"理论公式: Q/(b*(H+p))")
                    print(f"代入计算: {Q}/({self.b}*({self.H}+{self.p}))")
                    print(f"v0计算结果: {round(v0, 3)}")
                return v0

            def H0(self, v0):
                H0 = self.H + (self.alpha * v0 ** 2) / (2 * self.g)
                if self.debug:
                    print(f"理论公式: H+(alpha*v0^2)/(2g)")
                    print(f"代入计算: {self.H}+({self.alpha}*{v0}^2)/(2*{self.g})")
                    print(f"H0计算结果: {round(H0, 3)}")
                return H0

            def m_by_LieJin_right_angle_edge_inlet(self):
                h_ = self.p / self.H
                if self.debug:
                    print(f"理论公式: p/H")
                    print(f"代入计算: {self.p}/{self.H}")
                    print(f"h_计算结果: {round(h_, 3)}")
                m = 0.32 if h_ >= 3 else 0.32 + 0.01 * (3 - h_) / (0.46 + 0.75 * h_)
                if self.debug:
                    print(f"理论公式: 0.32 if h_>=3 else 0.32+0.01*(3-h_)/(0.46*0.75*h_)")
                    print(f"代入计算: 0.32 if {h_}>=3 else 0.32+0.01*(3-{h_})/({0.46}*{0.75}*{h_})")
                    print(f"m计算结果: {round(m, 3)}")
                m = MathUtils.limit_value(m, 0.32, 0.385)
                if self.debug:
                    print(f"m限制结果: {round(m, 3)}")
                return m

            def m_by_LieJin_rounded_edge_inlet(self):
                h_ = self.p / self.H
                if self.debug:
                    print(f"理论公式: p/H")
                    print(f"代入计算: {self.p}/{self.H}")
                    print(f"h_计算结果: {round(h_, 3)}")
                m = 0.36 if h_ >= 3 else 0.36 + 0.01 * (3 - h_) / (1.2 + 1.5 * h_)
                # 把m限制在0.32-0.385之间

                if self.debug:
                    print(f"理论公式: 0.36 if h_>=3 else 0.36+0.01*(3-h_)/(1.2*1.5*h_)")
                    print(f"代入计算: 0.36 if {h_}>=3 else 0.36+0.01*(3-{h_})/({1.2}*{1.5}*{h_})")
                    print(f"m计算结果: {round(m, 3)}")
                m = MathUtils.limit_value(m, 0.32, 0.385)
                if self.debug:
                    print(f"m限制结果: {round(m, 3)}")
                return m

    class SmallBridgeAperture:
        def __init__(self, base_culvert_instance):
            self.base_culvert_instance = base_culvert_instance
            self.standard_b = [4, 5, 6, 8, 10, 12, 16, 20]

        def __getattr__(self, item):
            return getattr(self.base_culvert_instance, item)

        def judge_weir_type(self, hc):
            type = '自由式' if 1.3 * hc > self.h else '淹没式'
            if self.debug:
                print(f"理论公式: 自由式: 1.3*hc>h, 淹没式: 1.3*hc<=h")
                print(f"代入计算: 1.3*hc={1.3 * hc} h={self.h}")
                print(f"堰流类型: {type}")
            return type

        def hc_by_v_(self, v_, psi):
            hc = (v_ ** 2) * (psi ** 2) * self.alpha / self.g
            if self.debug:
                print(f"理论公式: (v^2)*(psi^2)*alpha/g")
                print(f"代入计算: ({v_}^2)*({psi}^2)*{self.alpha}/{self.g}")
                print(f"hc计算结果: {round(hc, 3)}")
            return hc

        def hc_by_Q(self, Q, B, epsilon):
            hc = ((self.alpha * Q ** 2) / self.g / (epsilon * B ** 2)) ** (1 / 3)
            if self.debug:
                print(f"理论公式: ((alpha*Q^2)/g/(epsilon*B^2))^(1/3)")
                print(f"代入计算: (({self.alpha}*{Q}^2)/{self.g}/({epsilon}*{B}^2))^(1/3)")
                print(f"hc计算结果: {round(hc, 3)}")
            return hc

        def hc_by_H_(self, H_, fai, psi):
            hc = 2 * self.alpha * fai ** 2 * psi ** 2 / (1 + 2 * self.alpha * fai ** 2 * psi ** 3) * H_
            if self.debug:
                print(f"理论公式: 2*alpha*fai^2*psi^2/(1+2*alpha*fai^2*psi^3)*H_")
                print(f"代入计算: 2*{self.alpha}*{fai}^2*{psi}^2/({1}+2*{self.alpha}*{fai}^2*{psi}^3)*{H_}")
                print(f"hc计算结果: {round(hc, 3)}")
            return hc

        def H(self, Q, epsilon):
            H = Q / (epsilon * self.B * self.h)
            if self.debug:
                print(f"理论公式: Q/(epsilon*B*h)")
                print(f"代入计算: {Q}/({epsilon}*{self.B}*{self.h})")
                print(f"H计算结果: {round(H, 3)}")
            return H

        def b_free_weir_by_v_(self, v_, Q, hc, psi, epsilon):
            """
            计算孔径b
            :param Q:
            :param psi:
            :param epsilon:
            :return:
            """
            b = Q / (epsilon * psi * hc * v_)
            if self.debug:
                print(f"理论公式: Q/(epsilon*psi*hc*v)")
                print(f"代入计算: {Q}/({epsilon}*{psi}*{hc}*{v_})")
                print(f"b计算结果: {round(b, 3)}")
            # 取大于等于b的standard_b中的最小值
            b = MathUtils.find_min_greater_or_equal(b, self.standard_b)
            if self.debug:
                print(f"b标准孔径: {round(b, 3)}")
            return b

        def b_free_weir_by_H_(self, Q, H_, hc, fai, psi, epsilon):
            b = Q / (epsilon * psi * fai * hc * (2 * self.g * (H_ - psi * hc)) ** 0.5)
            if self.debug:
                print(f"理论公式: Q/(epsilon*psi*fai*hc*(2*g*(H_-psi*hc))^0.5)")
                print(f"代入计算: {Q}/({epsilon}*{psi}*{fai}*{hc}*(2*{self.g}*({H_}-{psi}*{hc}))^0.5)")
                print(f"b计算结果: {round(b, 3)}")
            # 取大于等于b的standard_b中的最小值
            b = MathUtils.find_min_greater_or_equal(b, self.standard_b)
            if self.debug:
                print(f"b标准孔径: {round(b, 3)}")
            return b

        def b_submerged_weir_by_v_(self, v_, Q, epsilon):
            b = Q / (epsilon * self.h * v_)
            if self.debug:
                print(f"理论公式: Q/(epsilon*h*v)")
                print(f"代入计算: {Q}/({epsilon}*{self.h}*{v_})")
                print(f"b计算结果: {round(b, 3)}")
            # 取大于等于b的standard_b中的最小值
            b = MathUtils.find_min_greater_or_equal(b, self.standard_b)
            if self.debug:
                print(f"b标准孔径: {round(b, 3)}")
            return b

        def b_submerged_weir_by_H_(self, Q, H_, epsilon, fai):
            b = Q / (epsilon * fai * self.h * (2 * self.g * (H_ - self.h)) ** 0.5)
            if self.debug:
                print(f"理论公式: Q/(epsilon*fai*h*(2*g*(H_-h))^0.5)")
                print(f"代入计算: {Q}/({epsilon}*{fai}*{self.h}*(2*{self.g}*({H_}-{self.h}))^0.5)")
                print(f"b计算结果: {round(b, 3)}")
            # 取大于等于b的standard_b中的最小值
            b = MathUtils.find_min_greater_or_equal(b, self.standard_b)
            if self.debug:
                print(f"b标准孔径: {round(b, 3)}")
            return b

        def H0_submerged_weir(self, v, fai, ):
            H0 = v ** 2 / 2 / self.g / fai ** 2 + self.h
            if self.debug:
                print(f"理论公式: v^2/2/g/fai^2+h")
                print(f"代入计算: {v}^2/2/{self.g}/{fai}^2+{self.h}")
                print(f"H0计算结果: {round(H0, 3)}")
            return H0

        def H0_free_weir(self, v, hc, fai, psi):
            H0 = v ** 2 / 2 / self.g / fai ** 2 + psi * hc
            if self.debug:
                print(f"理论公式: v^2/2/g/fai^2+psi*hc")
                print(f"代入计算: {v}^2/2/{self.g}/{fai}^2+{psi}*{hc}")
                print(f"H0计算结果: {round(H0, 3)}")
            return H0

        def v_submerged_weir(self, Q, epsilon, B):
            v = Q / (epsilon * B * self.h)
            if self.debug:
                print(f"理论公式: Q/(epsilon*B*h)")
                print(f"代入计算: {Q}/({epsilon}*{B}*{self.h})")
                print(f"v计算结果: {round(v, 3)}")
            return v

        def v_free_weir(self, Q, B, hc, epsilon, psi):
            v = Q / (epsilon * B * psi * hc)
            if self.debug:
                print(f"理论公式: Q/(epsilon*B*psi*hc)")
                print(f"代入计算: {Q}/({epsilon}*{B}*{psi}*{hc})")
                print(f"v计算结果: {round(v, 3)}")
            return v

    def judge_weir_type(self, zp_c=None):
        type1, type2, type3 = '', '', ''
        try:
            if self.delta is not None and self.H is not None:
                rwt = self.relative_weir_thickness()
                if rwt < 0.67:
                    type1 = '薄壁堰'
                    if zp_c is not None and self.z is not None and self.p_ is not None:
                        if self.z / self.p_ <= zp_c:
                            type2 = '淹没式'
                        else:
                            type2 = '自由式'
                elif 0.67 <= rwt < 2.5:
                    type2 = '实用断面堰'
                elif 2.5 <= rwt < 10:
                    type3 = '宽顶堰'
                    if self.delta_h is not None:
                        if 0.8 * self.H > self.delta_h:
                            type2 = '自由式'
                        else:
                            type2 = '淹没式'
                else:
                    raise ValueError('相对堰厚>10，不属于堰流范围')
            if self.b is not None and self.B is not None:
                if self.b < self.B:
                    type3 = '侧收缩'
                elif self.b == self.B:
                    type3 = '无侧收缩'
                else:
                    pass
        except ValueError as e:
            pass
        if self.debug:
            print(f"堰流类型: {type1} {type2} {type3}")
        return type1, type2, type3

    def relative_weir_thickness(self):
        rwt = self.delta / self.H
        if self.debug:
            print(f"理论公式: delta/H")
            print(f"代入计算: {self.delta}/{self.H}")
            print(f"相对堰厚计算结果: {round(rwt, 3)}")
        return rwt


if __name__ == '__main__':
    base_culvert = BaseCulvert(h=1.0, debug=True)
    small_bridge_aperture = base_culvert.SmallBridgeAperture(base_culvert)
    hc = small_bridge_aperture.hc_by_H_(1.2, 0.9, 1)
    small_bridge_aperture.judge_weir_type(hc=hc)
    B = small_bridge_aperture.b_submerged_weir_by_H_(30, 1.2, 0.85, 0.9)
    hc_ = small_bridge_aperture.hc_by_Q(30, B, 0.85)
    small_bridge_aperture.judge_weir_type(hc=hc_)
    small_bridge_aperture.v_submerged_weir(30, 0.85, 20)
    small_bridge_aperture.H0_submerged_weir(1.765, 0.9)
