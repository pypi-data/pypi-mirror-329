class Mengquan_Constant_Flow:
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
    def calculate_C_by_Manning(n, R):
        """
        通过曼宁公式计算C系数
        :return:
        """
        C = 1 / n * R ** (1 / 6)
        return C

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


if __name__ == '__main__':
    Mengquan_Constant_Flow.calculate_l_by_trapezium_method(2.08, 4, 31.2, 0.0003, 10, 1.5, 0.02, 1, 9.8, 5, )
