import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from scipy.interpolate import make_interp_spline

# 设置中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 或者 'Microsoft YaHei'
mpl.rcParams['axes.unicode_minus'] = False


class PlotUtils:
    """
    绘图工具类
    """
    def __init__(self):
        self.colors_dict = {'蓝色': 'b', '绿色': 'g', '红色': 'r', '黄色': 'y', '紫色': 'purple', '黑色': 'k',
                            '白色': 'w', '粉色': 'pink', '青色': 'c', '灰色': 'gray', '棕色': 'brown', '褐色': 'tan',
                            '青绿色': 'lime', '深绿色': 'darkgreen', '深蓝色': 'darkblue', '深红色': 'darkred',
                            '深黄色': 'darkgoldenrod', '深紫色': 'darkviolet', '深灰色': 'darkgray', '深褐色': 'sienna',
                            '亮蓝色': 'lightblue', '亮绿色': 'lightgreen', '亮红色': 'lightcoral', '亮黄色': 'yellow',
                            '亮紫色': 'plum', '亮灰色': 'lightgray', '亮褐色': 'tan', '暗蓝色': 'darkblue',
                            '暗绿色': 'darkgreen', '暗红色': 'darkred', '暗黄色': 'darkgoldenrod',
                            '暗紫色': 'darkviolet', '暗灰色': 'darkgray', '暗褐色': 'sienna'}
        self.markers_dict = {'圆点形': '.', '圆圈形': 'o', '正方形': 's', '上三角形': '^', '星形': '*', '加号形': '+',
                             'x形': 'x', '菱形': 'D', '细菱形': 'd', '下三角形': 'v', '五边形': 'p', '六边形1': 'h',
                             '六边形2': 'H', '竖线': '|', '横线': '_', '无': 'None'}
        self.line_styles_dict = {'实线': '-', '虚线': '--', '点划线': '-.', '点线': ':', '无': 'None'}
        self.points = []
        self.inter_points = []
        self.figure = {}

    def __find_color(self, color_name):
        for key, value in self.colors_dict.items():
            if color_name in key:
                return value
        else:
            raise ValueError('颜色名称错误')

    def __find_marker(self, marker_name):
        for key, value in self.markers_dict.items():
            if marker_name in key:
                return value
        else:
            raise ValueError('标记形状名称错误')

    def __find_line_style(self, line_style_name):
        for key, value in self.line_styles_dict.items():
            if line_style_name in key:
                return value
        else:
            raise ValueError('线型名称错误')

    def set_figure(self, fig_size=(10, 8), face_color='白色', edge_color='黑色', x_label='X', y_label='Y',
                   title='标题', x_lim=None, y_lim=None,
                   show_grid=True):
        """
        设置画布
        """
        self.figure['fig_size'] = fig_size
        self.figure['x_label'] = x_label
        self.figure['y_label'] = y_label
        self.figure['title'] = title
        self.figure['x_lim'] = x_lim
        self.figure['y_lim'] = y_lim
        self.figure['show_grid'] = show_grid
        self.figure['face_color'] = face_color
        self.figure['edge_color'] = edge_color

    def generate_points(self, x_list, y_list, color='蓝色', maker='圆点', point_size=10, point_alpha=1,
                        label='图例', bring_line_color=None, bring_line_style=None, bring_line_width=None,
                        bring_line_alpha=None, is_spline=False, interp_num=200, interp_color='暗蓝色',
                        interp_marker='圆点', interp_alpha=1,
                        interp_size=0, k=3):
        """
        生成散点数据
        """
        if bring_line_width == 0:
            bring_line_width = 1e-10
        if bring_line_alpha == 0:
            bring_line_alpha = 1e-10
        if is_spline:
            inter_x_list = np.array(x_list)
            inter_y_list = np.array(y_list)
            sorted_indices = np.argsort(inter_x_list)
            inter_x_list = inter_x_list[sorted_indices]
            inter_y_list = inter_y_list[sorted_indices]
            t = np.linspace(inter_x_list.min(), inter_x_list.max(), interp_num)
            # print(inter_x_list, inter_y_list)
            spl = make_interp_spline(inter_x_list, inter_y_list, k=k)
            inter_y_list = list(spl(t))
            inter_x_list = list(t)
            self.inter_points.append({'x_list': inter_x_list, 'y_list': inter_y_list, 'color': interp_color,
                                      'maker': interp_marker, 'point_size': interp_size, 'point_alpha': interp_alpha,
                                      'bring_line_color': bring_line_color, 'bring_line_style': bring_line_style,
                                      'bring_line_width': bring_line_width, 'bring_line_alpha': bring_line_alpha})
        else:
            self.inter_points.append({})
        points_data = {'x_list': x_list, 'y_list': y_list, 'color': color, 'maker': maker, 'point_size': point_size,
                       'point_alpha': point_alpha, 'label': label, 'bring_line_color': bring_line_color,
                       'bring_line_style': bring_line_style, 'bring_line_width': bring_line_width,
                       'bring_line_alpha': bring_line_alpha}
        self.points.append(points_data)

    def plot_points(self):
        """
        绘制散点图
        """
        if self.figure:
            fig_size = self.figure['fig_size']
            x_label = self.figure['x_label']
            y_label = self.figure['y_label']
            title = self.figure['title']
            x_lim = self.figure['x_lim']
            y_lim = self.figure['y_lim']
            show_grid = self.figure['show_grid']
            face_color = self.__find_color(self.figure['face_color'])
            edge_color = self.__find_color(self.figure['edge_color'])

        else:
            fig_size = (10, 8)
            face_color = 'white'
            edge_color = 'black'
            x_label = 'X'
            y_label = 'Y'
            title = '标题'
            x_lim = None
            y_lim = None
            show_grid = True
        plt.figure(figsize=fig_size, facecolor=face_color, edgecolor=edge_color)
        label_list = []
        for point in self.points:
            plt.scatter(point['x_list'], point['y_list'], color=self.__find_color(point['color']),
                        marker=self.__find_marker(point['maker']), s=point['point_size'], alpha=point['point_alpha'])
            label_list.append(point['label'])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if x_lim is not None:
            plt.xlim(x_lim)
        if y_lim is not None:
            plt.ylim(y_lim)
        plt.grid(show_grid)
        plt.legend(label_list)
        plt.show()

    def plot_lines(self, line_style=None, line_alpha=None, line_width=None, line_color=None):
        """
        绘制折线图，以下几个参数的优先级为：指定参数 > 点携带参数 > 默认参数
        line_color: 线条颜色。默认情况下，如果每条线的点携带了颜色，则使用该颜色，否则使用点的颜色，如果指定了line_color，则全部线条都使用该颜色
        line_style: 线条样式。默认情况下，如果每条线的点携带了样式，则使用该样式，否则实线，如果指定了line_style，则全部线条都使用该样式
        line_width: 线条宽度。默认情况下，如果每条线的点携带了宽度，则使用该宽度，否则使用1，如果指定了line_width，则全部线条都使用该宽度
        line_alpha: 线条透明度。默认情况下，如果每条线的点携带了透明度，则使用该透明度，否则使用1，如果指定了line_alpha，则全部线条都使用该透明度
        """
        if self.figure:
            fig_size = self.figure['fig_size']
            x_label = self.figure['x_label']
            y_label = self.figure['y_label']
            title = self.figure['title']
            face_color = self.__find_color(self.figure['face_color'])
            edge_color = self.__find_color(self.figure['edge_color'])
            x_lim = self.figure['x_lim']
            y_lim = self.figure['y_lim']
            show_grid = self.figure['show_grid']
        else:
            fig_size = (10, 8)
            x_label = 'X'
            y_label = 'Y'
            title = '标题'
            face_color = 'white'
            edge_color = 'black'
            x_lim = None
            y_lim = None
            show_grid = True
        plt.figure(figsize=fig_size, facecolor=face_color, edgecolor=edge_color)
        label_list = []

        for point in self.points:
            if line_color:
                lc = self.__find_color(line_color)
            elif point['bring_line_color']:
                lc = self.__find_color(point['bring_line_color'])
            else:
                lc = self.__find_color(point['color'])
            if line_style:
                ls = self.__find_line_style(line_style)
            elif point['bring_line_style']:
                ls = self.__find_line_style(point['bring_line_style'])
            else:
                ls = self.__find_line_style('实线')
            if line_width is not None:
                lw = line_width
            elif point['bring_line_width']:
                lw = point['bring_line_width']
            else:
                lw = 1
            if line_alpha is not None:
                la = line_alpha
            elif point['bring_line_alpha']:
                la = point['bring_line_alpha']
            else:
                la = 1
            plt.plot(point['x_list'], point['y_list'], markerfacecolor=self.__find_color(point['color']),
                     markeredgecolor=self.__find_color(point['color']),
                     color=lc,
                     marker=self.__find_marker(point['maker']), linestyle=ls,
                     markersize=point['point_size'],
                     alpha=la, linewidth=lw)
            label_list.append(point['label'])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if x_lim is not None:
            plt.xlim(x_lim)
        if y_lim is not None:
            plt.ylim(y_lim)
        plt.grid(show_grid)
        plt.legend(label_list)
        plt.show()

    def plot_curves(self, line_style=None, line_alpha=None, line_width=None, line_color=None, all_points_size=None):
        """
        绘制曲线图，用平滑曲线连接点，相比于plot_lines，增加了all_points_size参数，用于设置所有点的大小，包括内插点，其他参数的优先级规则同plot_lines（函数参数>点携带参数>默认参数（跟随非内插点））
        """
        if self.figure:
            fig_size = self.figure['fig_size']
            x_label = self.figure['x_label']
            y_label = self.figure['y_label']
            title = self.figure['title']
            face_color = self.__find_color(self.figure['face_color'])
            edge_color = self.__find_color(self.figure['edge_color'])
            x_lim = self.figure['x_lim']
            y_lim = self.figure['y_lim']
            show_grid = self.figure['show_grid']
        else:
            fig_size = (10, 8)
            x_label = 'X'
            y_label = 'Y'
            title = '标题'
            face_color = 'white'
            edge_color = 'black'
            x_lim = None
            y_lim = None
            show_grid = True
        plt.figure(figsize=fig_size, facecolor=face_color, edgecolor=edge_color)
        label_list = []
        count = 0
        for point in self.inter_points:
            if not point:
                count += 1
                continue
            if line_color:
                lc = self.__find_color(line_color)
            elif point['bring_line_color']:
                lc = self.__find_color(point['bring_line_color'])
            else:
                lc = self.__find_color(self.points[count]['color'])
            if line_style:
                ls = self.__find_line_style(line_style)
            elif point['bring_line_style']:
                ls = self.__find_line_style(point['bring_line_style'])
            else:
                ls = self.__find_line_style('实线')
            if line_width is not None:
                lw = line_width
            elif point['bring_line_width']:
                lw = point['bring_line_width']
            else:
                lw = 1
            if line_alpha is not None:
                la = line_alpha
            elif point['bring_line_alpha']:
                la = point['bring_line_alpha']
            else:
                la = 1
            if all_points_size is not None:
                ms = all_points_size
            else:
                ms = point['point_size']
            # if all_points_alpha:
            #     ma = all_points_alpha
            # else:
            #     ma = point['point_alpha']
            plt.plot(point['x_list'], point['y_list'], markerfacecolor=self.__find_color(point['color']),
                     markeredgecolor=self.__find_color(point['color']),
                     color=lc,
                     marker=self.__find_marker(point['maker']), linestyle=ls,
                     markersize=ms,
                     alpha=la, linewidth=lw)
            count += 1
        for point in self.points:
            plt.scatter(point['x_list'], point['y_list'], color=self.__find_color(point['color']),
                        marker=self.__find_marker(point['maker']), s=point['point_size'], alpha=point['point_alpha'])
            label_list.append(point['label'])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if x_lim is not None:
            plt.xlim(x_lim)
        if y_lim is not None:
            plt.ylim(y_lim)
        plt.grid(show_grid)
        plt.legend(label_list)
        plt.show()


if __name__ == '__main__':
    # 实例化画图工具类
    plot_utils = PlotUtils()
    plot_utils.set_figure(title='test', show_grid=False)
    plot_utils.generate_points(x_list=[1, 2, 3, 4, 5], y_list=[2, 3, 4, 5, 60], color='蓝色', maker='圆',
                               point_size=10, bring_line_color='绿色', bring_line_style='虚线',
                               is_spline=True, interp_size=3)
    plot_utils.generate_points(x_list=[1, 3, 2, 4, 5], y_list=[8, 19, 21, -23, 25], color='红色', maker='星',
                               point_size=20, label='图例2', is_spline=True, interp_color='绿色', interp_size=0)
    # print(plot_utils.inter_points)
    # plot_utils.plot_points()
    plot_utils.plot_curves(line_style='实线', all_points_size=0)
    # 绘制散点图
