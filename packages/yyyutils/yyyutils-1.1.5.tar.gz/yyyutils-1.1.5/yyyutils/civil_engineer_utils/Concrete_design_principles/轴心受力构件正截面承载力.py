from yyyutils.math_utils.math_utils import MathUtils
import re

math_utils = MathUtils()


class 通用工具类:
    """
    所有单位均用国际单位
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
    def 正方形截面边长b(A):
        """
        计算正方形截面边长b
        :param A:
        :return:
        """
        res = math_utils.sqrt(A)
        通用工具类.debug_print(description='计算正方形截面边长b', formula='sqrt(A)', params={'A': A},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 矩形截面面积A(b, h):
        """
        计算矩形截面面积A
        :param b:
        :param h:
        :return:
        """
        res = b * h
        通用工具类.debug_print(description='计算矩形截面面积A', formula='b * h', params={'b': b, 'h': h},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 圆面积A(d):
        """
        计算圆面积A
        :param d:
        :return:
        """
        res = math_utils.PI * d ** 2 / 4
        通用工具类.debug_print(description='计算圆面积A', formula='PI * d^2/4', params={'d': d},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 配筋率ρ(As, Ac):
        """
        计算轴心受拉构件的配筋率
        :param As:
        :param Ac:
        :return:
        """
        res = As / Ac
        通用工具类.debug_print(description='计算轴心受拉构件的配筋率ρ', formula='As / Ac', params={'As': As, 'Ac': Ac},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 弹模比αE(Es, Ec):
        """
        计算轴心受拉构件的弹模比
        :param Es:
        :param Ec:
        :return:
        """
        res = Es / Es
        通用工具类.debug_print(description='计算轴心受拉构件的弹模比αE', formula='Es / Ec', params={'Es': Es, 'Ec': Ec},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 标准长细比λ(l0, i):
        """
        计算轴心受拉构件的标准长细比
        :param l0:
        :param i:
        :return:
        """
        res = l0 / i
        通用工具类.debug_print(description='计算轴心受拉构件的标准长细比λ', formula='l0 / i', params={'l0': l0, 'i': i},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 矩形截面长细比λb(l0, b):
        """
        计算矩形截面长细比λb
        :param l0:
        :param b:
        :return:
        """
        res = l0 / b
        通用工具类.debug_print(description='计算矩形截面长细比λb', formula='l0 / b', params={'l0': l0, 'b': b},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 圆形截面长细比λd(l0, d):
        """
        计算圆形截面长细比λd
        :param l0:
        :param d:
        :return:
        """
        res = l0 / d
        通用工具类.debug_print(description='计算圆形截面长细比λd', formula='l0 / d', params={'l0': l0, 'd': d},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def 计算长度l0(l):
        """
        计算长度l0
        :param l:
        :return:
        """
        input_ = input(
            "请从如下列表中选择构件两端受到的约束类型(输入数字序号，不用分隔)：\n1. 铰支\t2. 固定\t3. 自由\n")
        input_ = list(input_)
        cofficient = None
        if input_ == ['1', '1']:
            cofficient = 1.0
        elif input_ == ['2', '2']:
            cofficient = 0.5
        elif input_ == ['1', '2'] or input_ == ['2', '1']:
            cofficient = 0.7
        elif input_ == ['2', '2']:
            cofficient = 2
        else:
            print("输入有误，请重新输入！")
        l0 = l * cofficient
        通用工具类.debug_print(description='计算长度l0', formula='l * cofficient',
                               params={'l': l, 'cofficient': cofficient},
                               result=l0) if 通用工具类.debug else None
        return l0

    @staticmethod
    def 正截面设计承载力(γ0, N, ):
        """
        计算轴心受压构件的设计受压承载力
        :param N:
        :param γ0:
        :return:
        """
        res = N * γ0
        通用工具类.debug_print(description='计算轴心受压构件的设计受压承载力', formula='N * γ0',
                               params={'N': N, 'γ0': γ0},
                               result=res) if 通用工具类.debug else None
        return res

    @staticmethod
    def dcor(d, c):
        dcor = d - 2 * c
        通用工具类.debug_print(description='计算dcor', formula='d-2*c', params={'d': d, 'c': c},
                               result=dcor) if 通用工具类.debug else None
        return dcor


class 轴心受拉工具类(通用工具类):
    """
    所有单位均用国际单位
    """
    debug = True

    @staticmethod
    def 最小配筋率ρmin(ft, fy):
        """
        计算轴心受拉构件的最小配筋率ρmin
        :param ft:
        :param fy:
        :return:
        """
        res = max(0.002, 0.45 * ft / fy)
        通用工具类.debug_print(description='计算轴心受拉构件的最小配筋率ρmin', formula='max(0.002, 0.45 * ft / fy)',
                               params={'ft': ft, 'fy': fy},
                               result=res) if 轴心受拉工具类.debug else None
        return res

    @staticmethod
    def 开裂荷载Ncr(ft, Ac, αE, ρ):
        """
        计算轴心受拉构件的开裂荷载
        :param ft:
        :param Ac:
        :param αE:
        :param ρ:
        :return:
        """
        res = ft * Ac * (1 - 2 * αE * ρ)
        通用工具类.debug_print(description='计算轴心受拉构件的开裂荷载Ncr', formula='ft * Ac * (1 - 2 * αE * ρ)',
                               params={'ft': ft, 'Ac': Ac, 'αE': αE, 'ρ': ρ},
                               result=res) if 轴心受拉工具类.debug else None
        return res

    @staticmethod
    def 开裂受拉钢筋应力σs(ft, αE):
        """
        计算轴心受拉构件的开裂受拉钢筋应力
        :param ft:
        :param αE:
        :return:
        """
        res = 2 * αE * ft
        通用工具类.debug_print(description='计算轴心受拉构件的开裂受拉钢筋应力σs', formula='2 * αE * ft',
                               params={'ft': ft, 'αE': αE},
                               result=res) if 轴心受拉工具类.debug else None

        return res

    @staticmethod
    def 正截面承载力Nu(fy, As):
        """
        计算轴心受拉构件的正截面承载力
        :param fy:
        :param As:
        :return:
        """
        res = fy * As
        通用工具类.debug_print(description='计算轴心受拉构件的正截面承载力Nu', formula='fy * As',
                               params={'fy': fy, 'As': As},
                               result=res) if 轴心受拉工具类.debug else None
        return res


class 轴心受压普通箍筋柱工具类(通用工具类):
    """
    所有单位均用国际单位
    """
    debug = True

    @staticmethod
    def 正截面受压承载力Nu(φ, fc, A, fy_, As_, ρ):
        """
        计算轴心受压构件的正截面受压承载力
        :param φ:
        :param fc:
        :param A:
        :param fy_:
        :param As_:
        :param ρ:
        :return:
        """
        if ρ > 0.03:
            A -= As_
        res = 0.9 * φ * (fc * A + fy_ * As_)
        通用工具类.debug_print(description='计算轴心受压构件的正截面受压承载力Nu',
                               formula='0.9 * φ * (fc * A + fy_ * As_)',
                               params={'φ': φ, 'fc': fc, 'A': A, 'fy_': fy_, 'As_': As_, 'ρ': ρ},
                               result=res) if 轴心受压普通箍筋柱工具类.debug else None

        return res

    @staticmethod
    def 截面面积A(φ, Nu, fc, fy_, ρ):
        """
        根据正截面受压承载力Nu计算截面面积A
        :param φ:
        :param Nu:
        :param fc:
        :param fy_:
        :param ρ:
        :return:
        """
        A = Nu / (0.9 * φ * (fc + fy_ * ρ))
        通用工具类.debug_print(description='计算截面面积A', formula='Nu / (0.9 * φ * (fc + fy_ * ρ))',
                               params={'Nu': Nu, 'φ': φ, 'fc': fc, 'fy_': fy_, 'ρ': ρ},
                               result=A) if 轴心受压普通箍筋柱工具类.debug else None

        return A

    @staticmethod
    def 受压钢筋面积As_(φ, A, fc, fy_, N):
        """
        依据设计强度和假设求得的截面面积计算受压钢筋面积As_
        :param φ:
        :param A:
        :param fc:
        :param fy_:
        :param N:
        :return:
        """
        res = (N - 0.9 * φ * fc * A) / (0.9 * φ * fy_)
        通用工具类.debug_print(description='计算受压钢筋面积As_', formula='(N - 0.9 * φ * fc * A) / (0.9 * φ * fy_)',
                               params={'N': N, 'φ': φ, 'fc': fc, 'A': A, 'fy_': fy_},
                               result=res) if 轴心受压普通箍筋柱工具类.debug else None

        return res

    @staticmethod
    def 内插求稳定系数φ(λ1, λ2, φ1, φ2, λ):
        φ = math_utils.linear_interpolate(λ1, λ2, φ1, φ2, λ)
        通用工具类.debug_print(description='计算稳定系数φ', formula='linear_interpolate(λ1, λ2, φ1, φ2, λ)',
                               params={'λ1': λ1, 'λ2': λ2, 'φ1': φ1, 'φ2': φ2, 'λ': λ},
                               result=φ) if 轴心受压普通箍筋柱工具类.debug else None

        return φ


class 轴心受压螺旋箍筋柱工具类:
    """
    所有单位均为国际单位
    """
    debug = True

    @staticmethod
    def 相当纵筋面积Ass0(dcor, Ass1, s):
        """
        计算相当纵筋面积Ass0
        :param dcor:
        :param Ass1:
        :param s:
        :return:
        """
        res = math_utils.PI * Ass1 * dcor / s
        通用工具类.debug_print(description='计算相当纵筋面积Ass0', formula='PI * Ass1 * dcor / s',
                               params={'dcor': dcor, 'Ass1': Ass1, 's': s},
                               result=res) if 轴心受压螺旋箍筋柱工具类.debug else None

        return res

    @staticmethod
    def 判断是否考虑螺旋箍筋影响(Ass0=None, As_=None, s=None, dcor=None, λd=None, Nu_=None, Nu=None):
        """
        判断是否考虑螺旋箍筋影响，传一个参数考虑一种情况
        :param Ass0:
        :param As_:
        :param s:
        :param dcor:
        :param λd:
        :param Nu_:
        :param Nu:
        :return:
        """
        res = True
        # 判断如果全是None，则报错
        if Ass0 is None and As_ is None and s is None and dcor is None and λd is None and Nu_ is None and Nu is None:
            raise ValueError("请至少输入一个参数！")
        if Ass0 is not None and As_ is not None:
            if Ass0 < 0.25 * As_:
                print("相当纵筋面积Ass0小于0.25*As，不考虑螺旋箍筋影响！")
                res = False
        if s is not None:
            if dcor is not None and s > dcor / 5:
                print("s大于dcor/5，不考虑螺旋箍筋影响！")
                res = False
            if s > 0.08:
                print("s大于0.08m，不考虑螺旋箍筋影响！")
            if s < 0.04:
                print("s小于0.04m，不考虑螺旋箍筋影响！")
        if λd is not None:
            if λd > 12:
                print("λd大于12，不考虑螺旋箍筋影响！")
                res = False
        if Nu_ is not None and Nu is not None:
            if Nu_ > 1.5 * Nu:
                print("轴心受压承载力Nu_大于1.5*Nu，不考虑螺旋箍筋影响！")
                res = False
        通用工具类.debug_print(description='判断是否考虑螺旋箍筋影响', formula=None,
                               params={'Ass0': Ass0, 'As_': As_, 's': s, 'dcor': dcor, 'λd': λd, 'Nu_': Nu_, 'Nu': Nu},
                               result=res) if 轴心受压螺旋箍筋柱工具类.debug else None
        return res

    @staticmethod
    def 正截面受压承载力Nu_(α, fc, fy_, fy, Acor, As_, Ass0):
        """
        计算轴心受压构件的正截面受压承载力
        :param α: 间接钢筋的折减系数，<C50时取1.0，C80取0.85
        :param fc:
        :param fy_:
        :param fy:
        :param Acor:
        :param As_:
        :param Ass0:
        :return:
        """
        res = 0.9 * (fc * Acor + fy_ * As_ + 2 * α * fy * Ass0)
        通用工具类.debug_print(description='计算轴心受压构件的正截面受压承载力Nu_',
                               formula='0.9 * (fc * Acor + fy_ * As_ + 2 * α * fy * Ass0)',
                               params={'α': α, 'fc': fc, 'fy_': fy_, 'fy': fy, 'Acor': Acor, 'As_': As_, 'Ass0': Ass0},
                               result=res) if 轴心受压螺旋箍筋柱工具类.debug else None
        return res


if __name__ == '__main__':
    fc = 11.9e6
    fy_ = 300e6
    l = 3
    A = 通用工具类.圆面积A(0.4)
    As_ = 1206e-6
    s = 0.05
    c = 0.035
    dcor = 通用工具类.dcor(0.4, c)
    Ass1 = 通用工具类.圆面积A(0.01)
    Ass0 = 轴心受压螺旋箍筋柱工具类.相当纵筋面积Ass0(dcor, Ass1, s)
    Acor = 通用工具类.圆面积A(dcor)
    l0 = 通用工具类.计算长度l0(l)
    λd = 通用工具类.圆形截面长细比λd(l0, 0.4)  # 圆形截面长细比λd=3.75
    φ = 1
    α = 1
    rou = 通用工具类.配筋率ρ(As_, A)
    轴心受压螺旋箍筋柱工具类.判断是否考虑螺旋箍筋影响(s=s, dcor=dcor, As_=As_, Ass0=Ass0, λd=λd)
    Nu_ = 轴心受压螺旋箍筋柱工具类.正截面受压承载力Nu_(α, fc, fy_, fy_, Acor, As_, Ass0)
    Nu = 轴心受压普通箍筋柱工具类.正截面受压承载力Nu(φ, fc, A, fy_, As_, rou)
    轴心受压螺旋箍筋柱工具类.判断是否考虑螺旋箍筋影响(Nu_=Nu_, Nu=Nu)
