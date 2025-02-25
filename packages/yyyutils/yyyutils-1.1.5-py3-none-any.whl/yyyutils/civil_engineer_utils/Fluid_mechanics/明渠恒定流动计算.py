import sympy as sp


class Mengquan_Constant_Flow:
    @staticmethod
    def define_symbol(name):
        """
        定义符号变量
        :return:
        """
        # 在类属性里面加上定义的符号变量
        # setattr(Mengquan_Constant_Flow, name, sp.symbols(name))
        return sp.symbols(name)

    @staticmethod
    def _calculate_C(n, R):
        """
        计算谢才公式C系数, 不要有符号变量
        :param n:
        :param R:水力半径
        :return:
        """
        if n < 0.02 and R < 0.5:
            print("采用曼宁公式计算C系数")
            C = 1 / n * R ** (1 / 6)
        else:
            print("采用巴甫洛夫斯基公式计算C系数")
            y = 2.5 * n ** 0.5 - 0.13 - 0.75 * R ** 0.5 * (n ** 0.5 - 0.1)
            C = 1 / n * R ** y
        return C

    @staticmethod
    def calculate_C_by_Manning(n, R):
        """
        通过曼宁公式计算C系数
        :return:
        """
        C = 1 / n * R ** (1 / 6)
        return C

    @staticmethod
    def calculate_C_by_Bublak(n, R):
        """
        通过巴甫洛夫斯基公式计算C系数
        :return:
        """
        y = 2.5 * n ** 0.5 - 0.13 - 0.75 * R ** 0.5 * (n ** 0.5 - 0.1)
        C = 1 / n * R ** y
        return C

    @staticmethod
    def calculate_R(A, chi):
        """
        计算水力半径
        :param A:
        :param chi:
        :return:
        """
        return A / chi

    @staticmethod
    def calculate_trapezium_data(b, h, m):
        """
        计算梯形截面明渠的各项数据
        :return:
        """
        B = b + 2 * m * h
        A = (b + m * h) * h
        chi = b + 2 * h * (1 + m ** 2) ** 0.5
        R = A / chi
        return B, A, chi, R

    @staticmethod
    def calculate_critical_depth_and_slope(alpha=None, Q=None, g=None, chic=None, hc: sp.Symbol = None,
                                           Ac: sp.Symbol = None,
                                           Bc: sp.Symbol = None, Cc: sp.Symbol = None):
        """
        计算临界水深和临界坡度
        :param Bc: 使用临界水深表示的水面
        :param alpha:
        :param Q:
        :param g:
        :param n:粗糙系数
        :param chic:湿周
        :param hc: 临界水深
        :param ic: 临界坡度
        :param Ac: 使用临界水深表示的截面面积
        :param Bc: 使用临界水深表示的水面宽度
        :param Cc: 使用临界水深表示的谢才系数
        :return:
        """
        hc_value = None
        ic_value = None
        try:
            # 列方程计算hc
            eq1 = Ac ** 3 / Bc - alpha * Q ** 2 / g
            # 解方程计算hc
            hc_values = sp.solve(eq1, hc)

            for i in hc_values:
                if i.is_real and i > 0:
                    hc_value = i
                    break
        except Exception as e:
            print(e)
            hc_value = None
        try:
            # 将hc的值代入到各个表达式中
            chic_value = float(chic.subs(hc, hc_value))
            Bc_value = float(Bc.subs(hc, hc_value))
            Cc_value = float(Cc.subs(hc, hc_value))

            # 使用数值直接计算ic
            ic_value = float(g * chic_value / (alpha * Cc_value ** 2 * Bc_value))
        except Exception as e:
            print(e)
            ic_value = None
        finally:
            return hc_value, ic_value

    @staticmethod
    def calculate_hc(Ac, Bc, alpha, Q, g, hc):
        hc_value = None
        try:
            # 列方程计算hc
            eq1 = Ac ** 3 / Bc - alpha * Q ** 2 / g
            # 解方程计算hc
            hc_values = sp.solve(eq1, hc)

            for i in hc_values:
                if i.is_real and i > 0:
                    hc_value = i
                    break
        except Exception as e:
            print(e)
            hc_value = None
        finally:
            return hc_value

    @staticmethod
    def calculate_vc(Q, A):
        return Q / A

    @staticmethod
    def calculate_Fr(alpha, Q, B0, g, A0):
        Frc = (alpha * Q ** 2 * B0 / g / A0 ** 3) ** 0.5
        return Frc

    @staticmethod
    def calculate_i(Q, A0, C0, R0):
        i = (Q / A0 / C0) ** 2 / R0
        return i

    @staticmethod
    def calculate_q(h, alpha, v, g):
        return h + alpha * v ** 2 / 2 / g

    @staticmethod
    def calculate_h0(h0: sp.Symbol, Q, A0: sp.Symbol, C0: sp.Symbol, R0: sp.Symbol, i: float):
        """
        计算正常状态下水深h0
        :param h0: 水深符号变量
        :param Q: 流量
        :param A0: 过水断面面积符号表达式
        :param C0: 谢才系数符号表达式
        :param R0: 水力半径符号表达式
        :param i: 底坡
        :return: 水深h0的数值解
        """
        import threading
        import queue

        # 建立方程
        eq1 = (i - Q ** 2 / A0 ** 2 / C0 ** 2 / R0)

        def solve_equation(result_queue):
            try:
                print("尝试解析解方程")
                # 尝试解析解
                solution = sp.solve(eq1, h0)

                # 筛选出物理有意义的解(水深为正实数)
                valid_solutions = [sol.evalf() for sol in solution if sol.is_real and sol > 0]

                if valid_solutions:
                    result_queue.put(float(valid_solutions[0]))
                else:
                    result_queue.put(None)
            except:
                result_queue.put(None)

        # 使用队列存储结果
        result_queue = queue.Queue()
        solver_thread = threading.Thread(target=solve_equation, args=(result_queue,))
        solver_thread.daemon = True
        solver_thread.start()

        try:
            # 等待10秒
            result = result_queue.get(timeout=1)
            if result is not None:
                return result
        except queue.Empty:
            pass  # 超时处理
        except Exception as e:
            pass  # 其他异常处理

        # 如果解析解失败或超时，使用数值解法
        try:
            print("解析解法失败，使用初始猜测值进行数值求解（h0_guess=0.1）")
            # 给定一个合理的初始猜测值
            h0_guess = 0.1
            # 使用nsolve数值求解
            numeric_solution = sp.nsolve(eq1, h0, h0_guess)

            # 验证解的有效性
            if numeric_solution.is_real and float(numeric_solution) > 0:
                return float(numeric_solution)
            else:
                raise ValueError("数值解法未找到物理有意义的解")

        except Exception as e:
            raise ValueError(f"方程求解失败: {str(e)}")

    @staticmethod
    def calculate_h_through_analysis(h: sp.Symbol, Q, A: sp.Symbol, C: sp.Symbol, R: sp.Symbol, i):
        """
        解析解求解h
        :return:
        """
        eq1 = (i - Q ** 2 / A ** 2 / C ** 2 / R)
        solution = sp.solve(eq1, h)
        for sol in solution:
            if sol.is_real and sol > 0:
                return float(sol)
        return None

    @staticmethod
    def calculate_h_through_numerical_method(h: sp.Symbol, Q, A: sp.Symbol, C: sp.Symbol, R: sp.Symbol, i,
                                             h0_guess=0.1):
        """
        数值解法求解h
        :return:
        """
        try:
            # 给定一个合理的初始猜测值
            # h0_guess = 0.1
            # 使用nsolve数值求解
            numeric_solution = sp.nsolve(i - Q ** 2 / A ** 2 / C ** 2 / R, h, h0_guess)

            # 验证解的有效性
            if numeric_solution.is_real and float(numeric_solution) > 0:
                return float(numeric_solution)
            else:
                raise ValueError("数值解法未找到物理有意义的解")

        except Exception as e:
            raise ValueError(f"方程求解失败: {str(e)}")

    @staticmethod
    def calculate_Q(A, C, R, i):
        return A * C * (R * i) ** 0.5

    @staticmethod
    def calculate_h0_optimal_condition(m, b):
        """
        传入的是数值就返回数值，传入的是符号变量就返回符号变量表达式，计算最优水力条件的h
        :param m:
        :param b:
        :return:
        """
        return b / (2 * ((1 + m ** 2) ** 0.5 - m))

    @staticmethod
    def calculate_h__(h_, hc):
        return h_ / 2 * ((1 + 8 * (hc / h_) ** 3) ** 0.5 - 1)

    @staticmethod
    def calculate_delta_h(h_, h__):
        return (h__ - h_) ** 3 / 4 / h_ / h__

    @staticmethod
    def calculate_l_by_trapezium_method(min_h, max_h, Q, i, b, m, n, alpha, g, segment_num, reverse=False, draw=False):
        """
        分段求和法求解l
        :param max_h:
        :param min_h:
        :param Q:
        :param i:
        :param g:
        :param segment_num: 分段数
        :param b:
        :param m:
        :param n:
        :param alpha:
        :param reverse: 是否反向计算，即水深从大到小计算
        :return:
        """
        # 在4到2.08之间找从大到小取出10个水深
        if min_h >= max_h:
            raise ValueError("最小水深必须小于最大水深")
        import numpy as np

        h_list = list(np.linspace(min_h, max_h, segment_num + 1) if not reverse else np.linspace(max_h, min_h,
                                                                                                 segment_num + 1))
        print("h_list:", h_list)
        sections = []
        for h in h_list:
            B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(b, h, m)
            C = Mengquan_Constant_Flow.calculate_C_by_Manning(n, R)
            sections.append((alpha, h, A, R, C))

        def single_l(alpha1, h1, A1, R1, C1, alpha2, h2, A2, R2, C2, Q, i, g, max_h, min_h):
            if h1 > max_h or h1 < min_h or h2 > max_h or h2 < min_h:
                raise ValueError("水深超出计算范围")
            v1 = Q / A1
            v2 = Q / A2
            hv1 = alpha1 * v1 ** 2 / 2 / g
            hv2 = alpha2 * v2 ** 2 / 2 / g
            e1 = h1 + hv1
            e2 = h2 + hv2
            average_v = (v1 + v2) / 2
            average_C = (C1 + C2) / 2
            average_R = (R1 + R2) / 2
            average_J = average_v ** 2 / average_C ** 2 / average_R
            delta_e = e2 - e1
            delta_l = delta_e / (i - average_J)
            print(f"delta_l({h1:0<.2f}m ——> {h2:0<.2f}m)：", f"{delta_l:.2f}m")
            return delta_l

        def draw_water_surface_curve(x_list, y_list, curve_names=None, title="", x_label="", y_label=""):
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots

            # 创建图形
            fig = go.Figure()

            # 处理单条曲线的情况
            if not isinstance(y_list[0], (list, tuple)):
                y_list = [y_list]

            # 处理图例名称
            if curve_names is None:
                curve_names = [""] * len(y_list)
            elif not isinstance(curve_names, (list, tuple)):
                curve_names = [curve_names]

            # 确保curve_names长度与曲线数量相同
            if len(curve_names) < len(y_list):
                curve_names.extend([""] * (len(y_list) - len(curve_names)))

            # 添加每条曲线
            for i, y_data in enumerate(y_list):
                fig.add_trace(
                    go.Scatter(
                        x=x_list,
                        y=y_data,
                        mode='lines+markers',  # 线条+标记点
                        line=dict(width=2, shape='spline'),  # 线条宽度
                        marker=dict(size=5),  # 标记点大小
                        name=curve_names[i],  # 使用传入的曲线名称
                        hovertemplate='x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>'  # 保留两位小数
                    )
                )

            # 更新布局
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                hovermode='closest',  # 悬停模式
                width=800,  # 图形宽度
                height=500,  # 图形高度
                showlegend=True,  # 显示图例
                legend=dict(
                    yanchor="top",  # 图例垂直位置
                    y=0.99,  # 图例y坐标
                    xanchor="right",  # 图例水平位置
                    x=0.99,  # 图例x坐标
                    bgcolor='rgba(255, 255, 255, 0.5)',  # 设置图例背景透明度
                    bordercolor='rgba(0, 0, 0, 0.3)',  # 设置图例边框透明度
                )
            )

            # 显示图形
            fig.show()

        l = 0
        delta_l_list = []
        for j in range(segment_num):
            delta_l = single_l(*sections[j], *sections[j + 1], Q, i, g, max_h, min_h)
            l += delta_l
            delta_l_list.append(delta_l)
        if draw:
            l_list = [0]
            for delta_l in delta_l_list:
                l_list.append(l_list[-1] + delta_l)
            if len(l_list) == len(h_list):
                draw_water_surface_curve(l_list, h_list, "水面高度", "水面曲线", "l(m)", "h(m)")

        print(f"  all_l({min_h:0<.2f}m ——> {max_h:0<.2f}m)：", f"{l:.2f}m") if not reverse else print(
            f"  all_l({max_h:0<.2f}m ——> {min_h:0<.2f}m)：",
            f"{l:0<.2f}m")
        return l

    @staticmethod
    def calculate_l_by_trapezium_method_pre(max_h, min_h, Q, i, g, *section_data):
        """
        分段求和法求解l
        :param max_h:
        :param min_h:
        :param Q:
        :param i:
        :param g:
        :param section_data: 每个截面的参数，动力系数alpha，水深h，截面面积A，水力半径R，谢才系数C，以元组形式传入
        :return:
        """
        if not isinstance(section_data[0], tuple):
            raise ValueError("section_data参数必须为元组")

        # 检查section_data里面的每一个元组是否有5个元素
        for data in section_data:
            if len(data) != 5:
                raise ValueError("section_data参数的每一个元素必须为5个元素的元组")

        sections_num = len(section_data)

        def single_l(alpha1, h1, A1, R1, C1, alpha2, h2, A2, R2, C2, Q, i, g, max_h, min_h):
            if h1 > max_h or h1 < min_h or h2 > max_h or h2 < min_h:
                raise ValueError("水深超出计算范围")
            v1 = Q / A1
            v2 = Q / A2
            hv1 = alpha1 * v1 ** 2 / 2 / g
            hv2 = alpha2 * v2 ** 2 / 2 / g
            e1 = h1 + hv1
            e2 = h2 + hv2
            average_v = (v1 + v2) / 2
            average_C = (C1 + C2) / 2
            average_R = (R1 + R2) / 2
            average_J = average_v ** 2 / average_C ** 2 / average_R
            delta_e = e2 - e1
            delta_l = delta_e / (i - average_J)
            print("single_delta_l:", delta_l)
            return delta_l

        l = 0
        for j in range(sections_num - 1):
            l += single_l(*section_data[j], *section_data[j + 1], Q, i, g, max_h, min_h)
        return l


# import sympy as sp


# from typing import Union, Optional, Tuple, Dict, Any
# import numpy as np
# from dataclasses import dataclass
# import logging
#
# # 配置日志
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# @dataclass
# class TrapeziumSection:
#     """梯形断面参数数据类"""
#     B: float  # 水面宽度
#     A: float  # 过水断面面积
#     chi: float  # 湿周
#     R: float  # 水力半径
#
#
# @dataclass
# class CriticalParameters:
#     """临界状态参数数据类"""
#     hc: float  # 临界水深
#     vc: float  # 临界流速
#     ic: float  # 临界坡度
#     Fr: float  # 弗劳德数
#
#
# class MengquanConstantFlow:
#     """
#     明渠恒定流水力计算类
#
#     属性:
#         g: 重力加速度, 默认9.81 m/s²
#         alpha: 动能修正系数, 默认1.0
#
#     方法:
#         define_symbol: 定义符号变量
#         calculate_C: 计算谢才系数
#         calculate_trapezium_data: 计算梯形断面参数
#         calculate_critical_parameters: 计算临界状态参数
#         等...
#     """
#
#     def __init__(self, g: float = 9.81, alpha: float = 1.0):
#         """
#         初始化明渠恒定流计算器
#
#         Args:
#             g: 重力加速度(m/s²)
#             alpha: 动能修正系数
#         """
#         self.g = g
#         self.alpha = alpha
#
#     @staticmethod
#     def define_symbol(name: str) -> sp.Symbol:
#         """
#         定义符号变量
#
#         Args:
#             name: 变量名称
#
#         Returns:
#             sp.Symbol: sympy符号变量
#         """
#         return sp.symbols(name)
#
#     @staticmethod
#     def calculate_C(n: float, R: float) -> float:
#         """
#         智能计算谢才系数C
#
#         Args:
#             n: 糙率
#             R: 水力半径(m)
#
#         Returns:
#             float: 谢才系数C
#
#         Raises:
#             ValueError: 当参数无效时
#         """
#         if n <= 0 or R <= 0:
#             raise ValueError("糙率n和水力半径R必须为正数")
#
#         if n < 0.02 and R < 0.5:
#             logger.info("使用曼宁公式计算谢才系数")
#             C = MengquanConstantFlow.calculate_C_by_Manning(n, R)
#         else:
#             logger.info("使用巴甫洛夫斯基公式计算谢才系数")
#             C = MengquanConstantFlow.calculate_C_by_Bublak(n, R)
#         return float(C)
#
#     @staticmethod
#     def calculate_C_by_Manning(n: float, R: float) -> float:
#         """通过曼宁公式计算C系数"""
#         return float(1 / n * R ** (1 / 6))
#
#     @staticmethod
#     def calculate_C_by_Bublak(n: float, R: float) -> float:
#         """通过巴甫洛夫斯基公式计算C系数"""
#         y = 2.5 * n ** 0.5 - 0.13 - 0.75 * R ** 0.5 * (n ** 0.5 - 0.1)
#         return float(1 / n * R ** y)
#
#     @staticmethod
#     def calculate_R(A: float, chi: float) -> float:
#         """
#         计算水力半径
#
#         Args:
#             A: 过水断面面积(m²)
#             chi: 湿周(m)
#
#         Returns:
#             float: 水力半径(m)
#
#         Raises:
#             ValueError: 当参数无效时
#         """
#         if A <= 0 or chi <= 0:
#             raise ValueError("面积和湿周必须为正数")
#         return float(A / chi)
#
#     @staticmethod
#     def calculate_trapezium_data(b: float, h: float, m: float) -> TrapeziumSection:
#         """
#         计算梯形截面明渠的各项数据
#
#         Args:
#             b: 底宽(m)
#             h: 水深(m)
#             m: 边坡系数
#
#         Returns:
#             TrapeziumSection: 包含断面特征参数的数据类对象
#
#         Raises:
#             ValueError: 当参数无效时
#         """
#         if b <= 0 or h <= 0:
#             raise ValueError("底宽和水深必须为正数")
#
#         B = b + 2 * m * h
#         A = (b + m * h) * h
#         chi = b + 2 * h * (1 + m ** 2) ** 0.5
#         R = A / chi
#
#         return TrapeziumSection(B, A, chi, R)
#
#     def calculate_critical_parameters(self, Q: float, b: float, m: float, n: float) -> CriticalParameters:
#         """
#         计算临界状态参数
#
#         Args:
#             Q: 流量(m³/s)
#             b: 底宽(m)
#             m: 边坡系数
#             n: 糙率
#
#         Returns:
#             CriticalParameters: 包含临界状态参数的数据类对象
#
#         Raises:
#             ValueError: 当参数无效或计算失败时
#         """
#         if Q <= 0 or b <= 0 or n <= 0:
#             raise ValueError("流量、底宽和糙率必须为正数")
#
#         try:
#             hc = self.define_symbol('hc')
#
#             # 临界状态下的几何参数表达式
#             Ac = (b + m * hc) * hc
#             Bc = b + 2 * m * hc
#             chic = b + 2 * hc * (1 + m ** 2) ** 0.5
#             Rc = Ac / chic
#             Cc = self.calculate_C(n, float(Rc))
#
#             # 计算临界水深
#             hc_value = self.calculate_hc(Ac, Bc, self.alpha, Q, self.g, hc)
#
#             if hc_value is None:
#                 raise ValueError("临界水深计算失败")
#
#             # 计算其他临界参数
#             Ac_value = float(Ac.subs(hc, hc_value))
#             vc = self.calculate_vc(Q, Ac_value)
#             ic = self.calculate_i(Q, Ac_value, Cc, float(Rc.subs(hc, hc_value)))
#             Fr = self.calculate_Fr(self.alpha, Q, float(Bc.subs(hc, hc_value)),
#                                    self.g, Ac_value)
#
#             return CriticalParameters(hc_value, vc, ic, Fr)
#
#         except Exception as e:
#             logger.error(f"临界参数计算失败: {str(e)}")
#             raise
#
#     def calculate_hc(self, Ac, Bc, alpha: float, Q: float, g: float, hc: sp.Symbol) -> Optional[float]:
#         """
#         计算临界水深
#
#         Args:
#             Ac: 临界水深表达式
#             Bc: 临界水面宽度表达式
#             alpha: 动能修正系数
#             Q: 流量(m³/s)
#             g: 重力加速度(m/s²)
#             hc: 临界水深符号变量
#
#         Returns:
#             Optional[float]: 临界水深值，计算失败时返回None
#         """
#         try:
#             eq1 = Ac ** 3 / Bc - alpha * Q ** 2 / g
#             hc_values = sp.solve(eq1, hc)
#
#             for value in hc_values:
#                 if value.is_real and value > 0:
#                     return float(value)
#             return None
#
#         except Exception as e:
#             logger.error(f"临界水深计算失败: {str(e)}")
#             return None
#
#     @staticmethod
#     def calculate_vc(Q: float, A: float) -> float:
#         """计算流速"""
#         if A <= 0:
#             raise ValueError("断面面积必须为正数")
#         return Q / A
#
#     @staticmethod
#     def calculate_Fr(alpha: float, Q: float, B: float, g: float, A: float) -> float:
#         """计算弗劳德数"""
#         if A <= 0 or B <= 0:
#             raise ValueError("断面面积和水面宽度必须为正数")
#         return float((alpha * Q ** 2 * B / g / A ** 3) ** 0.5)
#
#     @staticmethod
#     def calculate_i(Q: float, A: float, C: float, R: float) -> float:
#         """计算水力坡度"""
#         if A <= 0 or C <= 0 or R <= 0:
#             raise ValueError("参数必须为正数")
#         return float((Q / A / C) ** 2 / R)
#
#     @staticmethod
#     def calculate_Q(A: float, C: float, R: float, i: float) -> float:
#         """计算流量"""
#         if A <= 0 or C <= 0 or R <= 0 or i <= 0:
#             raise ValueError("参数必须为正数")
#         return float(A * C * (R * i) ** 0.5)
#
#     @staticmethod
#     def calculate_optimal_depth(m: Union[float, sp.Symbol],
#                                 b: Union[float, sp.Symbol]) -> Union[float, sp.Symbol]:
#         """
#         计算最佳水深
#
#         Args:
#             m: 边坡系数
#             b: 底宽
#
#         Returns:
#             Union[float, sp.Symbol]: 最佳水深，根据输入类型返回对应类型
#         """
#         return b / (2 * ((1 + m ** 2) ** 0.5 - m))
#
#     @staticmethod
#     def calculate_conjugate_depths(h1: float, hc: float) -> Tuple[float, float]:
#         """
#         计算共轭水深和水跃高度
#
#         Args:
#             h1: 初始水深(m)
#             hc: 临界水深(m)
#
#         Returns:
#             Tuple[float, float]: (共轭水深h2, 水跃高度delta_h)
#
#         Raises:
#             ValueError: 当参数无效时
#         """
#         if h1 <= 0 or hc <= 0:
#             raise ValueError("水深必须为正数")
#
#         h2 = h1 / 2 * ((1 + 8 * (hc / h1) ** 3) ** 0.5 - 1)
#         delta_h = (h2 - h1) ** 3 / (4 * h1 * h2)
#         return h2, delta_h
#
#     def to_dict(self) -> Dict[str, Any]:
#         """将对象转换为字典形式"""
#         return {
#             'g': self.g,
#             'alpha': self.alpha
#         }
#
#     def __str__(self) -> str:
#         """返回对象的字符串表示"""
#         return f"MengquanConstantFlow(g={self.g}, alpha={self.alpha})"
#
#
# if __name__ == '__main__':
#     # 创建计算实例
#     mcf = MengquanConstantFlow()
#
#     try:
#         # 计算梯形断面参数
#         section = mcf.calculate_trapezium_data(b=2.0, h=1.5, m=1.0)
#         print(f"断面参数: {section}")
#
#         # 计算临界状态参数
#         critical = mcf.calculate_critical_parameters(Q=5.0, b=2.0, m=1.0, n=0.015)
#         print(f"临界状态参数: {critical}")
#
#         # 计算共轭水深
#         h2, delta_h = mcf.calculate_conjugate_depths(h1=1.0, hc=0.8)
#         print(f"共轭水深: {h2:.3f}m, 水跃高度: {delta_h:.3f}m")
#
#     except ValueError as e:
#         print(f"计算错误: {str(e)}")
#     except Exception as e:
#         print(f"未知错误: {str(e)}")
if __name__ == '__main__':
    # hc = Mengquan_Constant_Flow.define_symbol('hc')
    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(2, hc, 0)
    # B0, A0, C0, R0 = Mengquan_Constant_Flow.calculate_trapezium_data(4, 2, 0)
    # print(B)
    # print(A)
    # print(chi)
    # print(R)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.017, R)
    # C0 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.017, R0)
    # print(C)
    # # hc, ic = Mengquan_Constant_Flow.calculate_critical_depth_and_slope(1, 8.2, 9.8, chi, hc, A, B, C)
    # hc = Mengquan_Constant_Flow.calculate_hc(A, B, 1, 8.2, 9.8, hc)
    # print(hc)
    # print(hc, ic)
    # A = A.subs('hc', hc)
    # vc = Mengquan_Constant_Flow.calculate_vc(8, A)
    # print(vc)
    # v0 = Mengquan_Constant_Flow.calculate_vc(8, 8)
    # print(v0)
    # Frc = Mengquan_Constant_Flow.calculate_Fr(1.1, 8, 4, 9.8, 8)
    #
    # print(Frc)
    # i = Mengquan_Constant_Flow.calculate_i(8, 8, C0, R0)
    # print(i)
    # print(Mengquan_Constant_Flow.calculate_h__(1, 1.197))
    # print(Mengquan_Constant_Flow.calculate_delta_h(0.298, 1.581))
    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(1, 0.202, 0)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.014, R)
    # print(Mengquan_Constant_Flow.calculate_i(0.284, A, C, R))

    # h0 = Mengquan_Constant_Flow.define_symbol('h0')
    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(1, h0, 0)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.014, R)
    # print(A)
    # print(C)
    # print(R)
    # print(Mengquan_Constant_Flow.calculate_h_through_numerical_method(h0, 0.284, A, C, R, 0.0004))
    # # 0.5007083526268088
    #
    # h0 = Mengquan_Constant_Flow.define_symbol('h0')
    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(10, h0, 1.5)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R)
    # print(Mengquan_Constant_Flow.calculate_h_through_numerical_method(h0, 31.2, A, C, R, 0.0003))
    # print(Mengquan_Constant_Flow.calculate_hc(A, B, 1, 31.2, 9.8, h0))

    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(2, 0.68, 0)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R)
    # section1 = (1, 0.68, A, R, C)
    # B2, A2, chi2, R2 = Mengquan_Constant_Flow.calculate_trapezium_data(2, 0.42, 0)
    # C2 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R2)
    # section2 = (1, 0.42, A2, R2, C2)
    # B3, A3, chi3, R3 = Mengquan_Constant_Flow.calculate_trapezium_data(2, 0.3, 0)
    # C3 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R3)
    # section3 = (1, 0.3, A3, R3, C3)
    # B4, A4, chi4, R4 = Mengquan_Constant_Flow.calculate_trapezium_data(2, 0.25, 0)
    # C4 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R4)
    # section4 = (1, 0.25, A4, R4, C4)
    # B5, A5, chi5, R5 = Mengquan_Constant_Flow.calculate_trapezium_data(2, 0.24, 0)
    # C5 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R5)
    # section5 = (1, 0.24, A5, R5, C5)
    # print(Mengquan_Constant_Flow.calculate_l_by_trapezium_method_pre(0.68, 0.21, 3.5, 0.3, 9.8,
    #                                                              section1, section2, section3, section4, section5))

    Mengquan_Constant_Flow.calculate_l_by_trapezium_method(2.08, 4, 31.2, 0.0003, 10, 1.5, 0.02, 1, 9.8, 5, )
    # print(Mengquan_Constant_Flow.calculate_l_by_trapezium_method(0.68, 0.2405, 3.5, 0.3, 2, 0, 0.02, 1, 9.8, 1000))
    #
    # B, A, chi, R = Mengquan_Constant_Flow.calculate_trapezium_data(10, 4, 1.5)
    # C = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R)
    # section1 = (1, 4, A, R, C)
    # B2, A2, chi2, R2 = Mengquan_Constant_Flow.calculate_trapezium_data(10, 3.5, 1.5)
    # C2 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R2)
    # section2 = (1, 3.5, A2, R2, C2)
    # B3, A3, chi3, R3 = Mengquan_Constant_Flow.calculate_trapezium_data(10, 3, 1.5)
    # C3 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R3)
    # section3 = (1, 3, A3, R3, C3)
    # B4, A4, chi4, R4 = Mengquan_Constant_Flow.calculate_trapezium_data(10, 2.49, 1.5)
    # C4 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R4)
    # section4 = (1, 2.5, A4, R4, C4)
    # B5, A5, chi5, R5 = Mengquan_Constant_Flow.calculate_trapezium_data(10, 2.08, 1.5)
    # C5 = Mengquan_Constant_Flow.calculate_C_by_Manning(0.02, R5)
    # section5 = (1, 2.08, A5, R5, C5)
    # print(Mengquan_Constant_Flow.calculate_l_by_trapezium_method_pre(4, 2.08, 31.2, 0.0003, 9.8,
    #                                                              section5, section4, section3, section2, section1))
