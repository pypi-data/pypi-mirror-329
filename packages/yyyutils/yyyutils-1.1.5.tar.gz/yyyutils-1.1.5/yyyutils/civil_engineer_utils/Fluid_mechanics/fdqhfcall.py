import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
                             QScrollArea, QCheckBox, QTextEdit)


class ResultDialog(QMainWindow):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("计算结果")
        self.setGeometry(200, 200, 600, 400)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建可滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # 创建文本显示区域
        content = QWidget()
        scroll.setWidget(content)
        v_layout = QVBoxLayout(content)

        # 创建文本编辑框
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(text)
        v_layout.addWidget(text_edit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分段求和法计算L")
        self.setGeometry(100, 100, 800, 600)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # 创建内容部件
        content = QWidget()
        self.layout = QVBoxLayout(content)

        # 创建输入框和标签
        self.inputs = {}
        self.create_input("min_h", "最小水深(m)：")
        self.create_input("max_h", "最大水深(m)：")
        self.create_input("Q", "流量(m^3/s)：")
        self.create_input("i", "底坡：")
        self.create_input("b", "棱柱形截面底宽(m)：")
        self.create_input("m", "棱柱形截面边坡系数(m/m)：")
        self.create_input("n", "粗糙度系数：")

        # 设置默认值
        self.create_input("alpha", "动力系数：", default_value='1.0')
        self.create_input("g", "重力加速度(m/s^2)：", default_value='9.8')

        self.create_input("segment_num", "分段数：", default_value='10')

        # 创建复选框
        self.reverse_check = QCheckBox("是否反向计算")
        self.layout.addWidget(self.reverse_check)

        self.draw_check = QCheckBox("是否绘制水面曲线")
        self.layout.addWidget(self.draw_check)

        # 创建计算按钮
        calc_button = QPushButton("计算")
        calc_button.clicked.connect(self.calculate)
        self.layout.addWidget(calc_button)

        # 设置滚动区域
        scroll.setWidget(content)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(scroll)

    def create_input(self, name, label_text, default_value=None):
        container = QWidget()
        layout = QHBoxLayout(container)

        label = QLabel(label_text)
        input_field = QLineEdit()

        # 如果有默认值，则设置输入框的文本
        if default_value is not None:
            input_field.setText(default_value)

        layout.addWidget(label)
        layout.addWidget(input_field)

        self.layout.addWidget(container)
        self.inputs[name] = input_field

        # 设置回车跳转
        input_field.returnPressed.connect(lambda: self.focus_next_input(name))

    def focus_next_input(self, current_name):
        input_list = list(self.inputs.keys())
        try:
            current_index = input_list.index(current_name)
            if current_index < len(input_list) - 1:
                self.inputs[input_list[current_index + 1]].setFocus()
            else:
                self.reverse_check.setFocus()
        except ValueError:
            pass

    def calculate(self):
        try:
            # 获取输入值
            values = {
                'min_h': float(self.inputs['min_h'].text()),
                'max_h': float(self.inputs['max_h'].text()),
                'Q': float(self.inputs['Q'].text()),
                'i': float(self.inputs['i'].text()),
                'b': float(self.inputs['b'].text()),
                'm': float(self.inputs['m'].text()),
                'n': float(self.inputs['n'].text()),
                'alpha': float(self.inputs['alpha'].text()),  # 动力系数
                'g': float(self.inputs['g'].text()),  # 重力加速度
                'segment_num': int(self.inputs['segment_num'].text()),
                'reverse': self.reverse_check.isChecked(),
                'draw': self.draw_check.isChecked()
            }

            # 创建输出捕获器
            import io
            import sys
            output_buffer = io.StringIO()
            sys.stdout = output_buffer

            # 调用计算函数
            from yyyutils.civil_engineer_utils.Fluid_mechanics.明渠恒定流动计算 import Mengquan_Constant_Flow
            Mengquan_Constant_Flow.calculate_l_by_trapezium_method(
                values['min_h'], values['max_h'], values['Q'],
                values['i'], values['b'], values['m'],
                values['n'], values['alpha'], values['g'],
                values['segment_num'], values['reverse'], values['draw']
            )

            # 恢复标准输出并获取输出内容
            sys.stdout = sys.__stdout__
            output_text = output_buffer.getvalue()

            # 显示结果对话框
            self.result_dialog = ResultDialog(output_text)
            self.result_dialog.show()

        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"计算过程中发生错误：{str(e)}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


import inspect


def get_file_content_as_string():
    """
    Returns the content of the current Python file as a string,
    excluding the method itself.
    """
    with open(__file__, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 获取当前方法的开始和结束行号
    start_index = lines.index("def get_file_content_as_string():\n")
    end_index = start_index + len(inspect.getsource(inspect.currentframe()).splitlines(True))

    # 将文件内容转换为字符串，排除当前方法
    content = ''.join(lines[:start_index] + lines[end_index + 1:])

    return content.strip()


if __name__ == '__main__':
    print(get_file_content_as_string())
    main()
