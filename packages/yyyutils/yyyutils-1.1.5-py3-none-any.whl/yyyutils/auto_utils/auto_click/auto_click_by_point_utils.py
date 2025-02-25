import json
from pynput import mouse, keyboard
import time
import win32gui
import win32con
from yyyutils.auto_utils.moniter.moniter_keyboard_utils import MoniterKeyboardUtils


class AutoClickUtils:
    """
    基于坐标的鼠标点击工具类
    """

    def __init__(self, load_positions=False, load_positions_name=None, pause_key='f9', max_window=False):
        self.positions = []
        self.window_position = None
        self.get_position_stop_flag = False
        self.loop_stop_flag = False
        self.max_click_num = 30
        self.__window_handle = None
        self.clicking = True
        self.max_window = max_window
        self.pause_key_listener = MoniterKeyboardUtils(pause_key, toggle_clicking_func=self.__toggle_clicking)
        self.pause_key_listener.start()
        if load_positions and load_positions_name:
            self.load_mouse_click_positions(load_positions_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__window_handle:
            self.__remove_window_always_on_top()
        self.pause_key_listener.stop()

    def __find_window(self, window_title):
        def enum_windows_callback(hwnd, results):
            window_text = win32gui.GetWindowText(hwnd)
            if window_title.lower() in window_text.lower():
                results.append(hwnd)

        matching_windows = []
        win32gui.EnumWindows(enum_windows_callback, matching_windows)

        if matching_windows:
            self.__window_handle = matching_windows[0]
            print(f"找到窗口句柄: {self.__window_handle}")  # 打印窗口句柄
            return matching_windows[0]
        else:
            raise Exception(f"未找到包含 '{window_title}' 的窗口")

    def set_window_always_on_top(self, window_title=None, enable=True):
        """
        置顶窗口
        :return:
        """
        if not window_title:
            raise ValueError("窗口标题不能为空！")
        handle = self.__find_window(window_title)
        if handle:
            win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST,
                                  0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            if self.max_window:
                win32gui.ShowWindow(self.__window_handle, win32con.SW_MAXIMIZE)
            else:
                # 确保窗口是可见的
                win32gui.ShowWindow(self.__window_handle, win32con.SW_SHOWNORMAL)
            win32gui.SetForegroundWindow(handle)

            print(f"已置顶窗口: {win32gui.GetWindowText(handle)}")
            if not enable:
                win32gui.EnableWindow(self.__window_handle, False)
            return handle
        else:
            raise Exception("窗口句柄无效，无法置顶窗口！")

    def __remove_window_always_on_top(self):
        """
        取消置顶窗口
        :return:
        """
        if self.__window_handle:
            win32gui.SetWindowPos(self.__window_handle, win32con.HWND_NOTOPMOST,
                                  0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            print(f"已取消窗口置顶")
        else:
            raise Exception("窗口句柄无效，无法取消置顶窗口！")

    def __lock_window(self):
        """
        锁定窗口，使其显示但无法点击
        """
        if not self.__window_handle:
            raise ValueError("窗口句柄无效！")

        if self.__window_handle:
            try:
                if self.max_window:
                    win32gui.ShowWindow(self.__window_handle, win32con.SW_MAXIMIZE)
                else:
                    # 确保窗口是可见的
                    win32gui.ShowWindow(self.__window_handle, win32con.SW_SHOWNORMAL)

                # 禁用窗口
                win32gui.EnableWindow(self.__window_handle, False)

                print(f"已锁定窗口: {win32gui.GetWindowText(self.__window_handle)}")
            except Exception as e:
                print(f"锁定窗口失败: {e}")
                raise Exception("窗口句柄无效，无法锁定窗口！")
        else:
            raise Exception("窗口句柄无效，无法锁定窗口！")

    def __unlock_window(self):
        """
        解锁窗口，使其可以正常点击
        """
        if self.__window_handle:
            try:
                # 如果当前窗口被锁定，解锁窗口
                if not win32gui.IsWindowEnabled(self.__window_handle):
                    win32gui.EnableWindow(self.__window_handle, True)
                    print(f"已解锁窗口: {win32gui.GetWindowText(self.__window_handle)}")
            except Exception as e:
                print(f"解锁窗口失败: {e}")
                raise Exception("窗口句柄无效，无法解锁窗口！")
        else:
            raise Exception("窗口句柄无效，无法解锁窗口！")

    def click_xy(self, x=None, y=None, position=None, background=False):
        """if background:
            if not self.__window_handle:
                raise Exception("窗口句柄无效！")
            # 使窗口恢复

            # win32gui.ShowWindow(self.__window_handle, win32con.SW_RESTORE)
            # 转换为窗口 client 坐标
            client_rect = win32gui.GetWindowRect(self.__window_handle)
            x = (client_rect[2] - client_rect[0]) // 2
            y = (client_rect[3] - client_rect[1]) // 2
            x, y = win32gui.ClientToScreen(self.__window_handle, (x, y))
            print(f"窗口位置: {client_rect}")
            print(f"后台点击坐标: ({x}, {y})")
            lParam = win32api.MAKELONG(x, y)
            result_down = win32api.PostMessage(self.__window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                               lParam)
            result_up = win32api.PostMessage(self.__window_handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
            print(f"WM_LBUTTONDOWN 返回值: {result_down}")
            print(f"WM_LBUTTONUP 返回值: {result_up}")
        else:"""
        if position and x is None and y is None:
            print(f"点击位置: {position}")
            x, y = position
        if self.clicking:
            if self.__window_handle:
                if self.max_window:
                    win32gui.ShowWindow(self.__window_handle, win32con.SW_MAXIMIZE)
                else:
                    # 确保窗口是可见的
                    win32gui.ShowWindow(self.__window_handle, win32con.SW_SHOWNORMAL)
            m = mouse.Controller()
            m.position = (x, y)
            m.click(mouse.Button.left, 1)
        # else:
        #     # 最小化窗口
        #     if self.__window_handle:
        #         win32gui.ShowWindow(self.__window_handle, win32con.SW_MINIMIZE)

    def click_positions(self, positions, intervals=0.5, background=False):
        """
        实现批量点击屏幕坐标列表positions中的坐标点
        :param positions: 屏幕坐标列表，元素为元组(x, y)
        :param intervals: 两次点击之间的间隔时间，单位为秒，可以为单个数字或列表
        """
        if isinstance(intervals, (int, float)):
            intervals = [intervals] * (len(positions) - 1)

        for i, (x, y) in enumerate(positions):
            self.click_xy(x, y, background=background)
            if i < len(intervals):
                time.sleep(intervals[i])

    def click_positions_continuously(self, positions=None, interval=0.5, loop_interval=1.0, duration=1.0,
                                     background=False):
        """
        实现持续点击屏幕坐标列表positions中的坐标点
        :param positions: 屏幕坐标列表，元素为元组(x, y)
        :param interval: 两次点击之间的间隔时间，单位为秒，可以为单个数字或列表
        :param loop_interval: 循环间隔时间，单位为秒
        :param duration: 持续时间，单位为小时
        """
        if self.__window_handle:
            self.__unlock_window()
        if not positions:
            positions = self.positions
        duration *= 3600  # 转换为秒
        if duration <= 0:
            raise ValueError("持续时间必须大于0")
        if duration < loop_interval:
            raise ValueError("持续时间必须大于循环间隔时间")
        if interval < 0.01:
            interval = 0.01
        if loop_interval < 0.01:
            loop_interval = 0.01
        print("开始持续点击屏幕坐标列表...(或按Esc结束循环)")
        print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print(f"持续时间: {duration / 3600:.2f} 小时, 循环间隔: {loop_interval} 秒")
        # 当duration小于等于0时以及当按下Esc键时，停止循环
        with MoniterKeyboardUtils(keyboard.Key.esc, toggle_clicking_func=self.__on_press_esc2):
            while not self.loop_stop_flag:  # 保持监听直到停止
                self.click_positions(positions, interval, background=background)
                time.sleep(loop_interval)
                duration -= loop_interval
                if duration <= 0:
                    break
        print(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        if self.__window_handle:
            self.__remove_window_always_on_top()

    def __on_click(self, x, y, button, pressed):
        if pressed:
            self.positions.append((x, y))
            print(f"已记录点击位置: ({x}, {y})")
            if len(self.positions) >= self.max_click_num:  # 假设我们只记录10次点击
                self.get_position_stop_flag = True  # 停止监听
                return False  # 停止监听

    def __on_press_esc1(self):
        self.get_position_stop_flag = True  # 停止监听
        return False  # 停止监听

    def __on_press_esc2(self):
        self.loop_stop_flag = True  # 停止循环
        return False  # 停止监听

    def get_mouse_click_positions(self, save=False, save_name='positions', save_mode="overwrite"):
        """
        获取鼠标点击的位置以及窗口位置
        """
        print("请点击屏幕上的位置，记录达到最大数量后自动结束...(或按Esc结束记录)")
        self.positions = []
        # 监听鼠标点击事件
        with mouse.Listener(on_click=self.__on_click) as mouse_listener:
            # 监听键盘按键事件
            with MoniterKeyboardUtils(keyboard.Key.esc, toggle_clicking_func=self.__on_press_esc1):
                while not self.get_position_stop_flag:  # 保持监听直到停止
                    pass
        if self.__window_handle:
            self.window_position = win32gui.GetWindowRect(self.__window_handle)
            win32gui.EnableWindow(self.__window_handle, True)
        if save:
            self.save_mouse_click_positions(save_name, mode=save_mode)
        return self.positions, self.window_position

    def save_mouse_click_positions(self, name, mode="overwrite"):
        """
        保存鼠标点击位置到 JSON 文件
        :param name: 自定义键名
        :param mode: 模式，"overwrite" 为覆盖模式，"append" 为添加模式
        """
        if not self.positions:
            raise ValueError("未获取到鼠标点击位置列表！")

        data = {name: self.positions}

        if mode == "overwrite":
            # 覆盖模式，直接写入文件
            with open("positions.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif mode == "append":
            # 添加模式，先读取现有文件内容，然后合并数据
            try:
                with open("positions.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = {}

            existing_data.update(data)

            with open("positions.json", "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError("无效的模式，请使用 'overwrite' 或 'append'")

    def load_mouse_click_positions(self, name):
        """
        从 JSON 文件加载鼠标点击位置
        :param name:
        :return:
        """
        with open("positions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if name in data:
            self.positions = data[name]
            return self.positions
        else:
            raise ValueError(f"未找到名为 '{name}' 的鼠标点击位置列表！")

    """def __on_release_pause_key(self, key):
        if isinstance(key, keyboard.KeyCode):
            self.current_keys.discard(key.char)
        else:
            self.current_keys.discard(key)"""

    def __toggle_clicking(self):
        self.clicking = not self.clicking
        print("连续点击：", "开启" if self.clicking else "关闭")

    @staticmethod
    def get_json_all_keys():
        with open("positions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        keys = []
        for key in data.keys():
            keys.append(key)
        return keys

    @staticmethod
    def get_all_window_titles():
        def enum_windows_callback(hwnd, results):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text:
                results.append(window_text)

        all_titles = []
        win32gui.EnumWindows(enum_windows_callback, all_titles)
        return all_titles


"""
后台特定窗口进行点击操作
import time
import win32gui
import win32api
import win32con

class AutoClickUtils:
    def __init__(self):
        self.positions = []
        self.loop_stop_flag = False
        # self.max_click_num = 10  # 如果不再需要限制点击次数，可以移除此行

    def find_window(self, window_title):
        # 获取窗口句柄
        self.window_handle = win32gui.FindWindow(None, window_title)
        if not self.window_handle:
            raise Exception(f"未找到窗口: {window_title}")

    def click_xy_in_window(self, x, y):
        # 向指定窗口发送鼠标点击消息
        if not self.window_handle:
            raise Exception("窗口句柄无效！")

        # 构造位置消息，坐标(x, y)相对于窗口客户区
        lParam = win32api.MAKELONG(x, y)
        win32api.SendMessage(self.window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.SendMessage(self.window_handle, win32con.WM_LBUTTONUP, None, lParam)

    def click_positions_in_window(self, positions, interval=0.5):
        # 批量在指定窗口内点击坐标
        for x, y in positions:
            self.click_xy_in_window(x, y)
            time.sleep(interval)

    def click_positions_continuously(self, positions, interval=0.5, loop_interval=1.0, duration=1.0):
        # 持续对某窗口内点击
        duration *= 3600  # 转换为秒
        start_time = time.time()
        print("开始持续点击指定窗口中的坐标列表...")

        while (time.time() - start_time) < duration:
            self.click_positions_in_window(positions, interval)
            time.sleep(loop_interval)
        
        print("点击操作结束")

if __name__ == '__main__':
    c = AutoClickUtils()
    window_title = "记事本"  # 用目标窗口的标题替换“记事本”
    try:
        c.find_window(window_title)
        positions = [(100, 100), (200, 200)]  # 相对于窗口的客户区坐标
        c.click_positions_continuously(positions, duration=0.005)
    except Exception as e:
        print(str(e))
"""

# def run_click_process(auto_click_utils, positions, interval, loop_interval, duration):
#     auto_click_utils.click_positions_continuously(positions=positions, interval=interval, loop_interval=loop_interval,
#                                                   duration=duration)
"""import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, \
    QInputDialog, QTextEdit


class AutoClickApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('工具设置')
        self.layout = QVBoxLayout()

        self.window_title_label = QLabel('目标窗口的标题:')
        self.window_title_entry = QLineEdit()
        self.layout.addWidget(self.window_title_label)
        self.layout.addWidget(self.window_title_entry)

        self.show_windows_button = QPushButton('显示所有窗口名字')
        self.show_windows_button.clicked.connect(self.show_windows)
        self.layout.addWidget(self.show_windows_button)

        self.duration_label = QLabel('持续时间(小时):')
        self.duration_entry = QLineEdit()
        self.layout.addWidget(self.duration_label)
        self.layout.addWidget(self.duration_entry)

        self.loop_interval_label = QLabel('循环间隔时间(秒):')
        self.loop_interval_entry = QLineEdit()
        self.layout.addWidget(self.loop_interval_label)
        self.layout.addWidget(self.loop_interval_entry)

        self.interval_label = QLabel('两次点击之间的间隔时间(秒):')
        self.interval_entry = QLineEdit()
        self.layout.addWidget(self.interval_label)
        self.layout.addWidget(self.interval_entry)

        self.load_positions_checkbox = QCheckBox('加载已保存的点击位置(y/n):(默认不加载)')
        self.layout.addWidget(self.load_positions_checkbox)

        self.enable_checkbox = QCheckBox('点击位置时锁定窗口(y/n):(默认不锁定)')
        self.layout.addWidget(self.enable_checkbox)

        self.save_checkbox = QCheckBox('保存点击位置(y/n):(默认不保存)')
        self.layout.addWidget(self.save_checkbox)

        self.pause_key_label = QLabel('请输入暂停键(直接回车则默认为F9):')
        self.pause_key_entry = QLineEdit()
        self.layout.addWidget(self.pause_key_label)
        self.layout.addWidget(self.pause_key_entry)

        self.submit_button = QPushButton('设置并运行')
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)



        self.setLayout(self.layout)

        # 设置 tab 顺序
        self.setTabOrder(self.window_title_entry, self.duration_entry)
        self.setTabOrder(self.duration_entry, self.loop_interval_entry)
        self.setTabOrder(self.loop_interval_entry, self.interval_entry)
        self.setTabOrder(self.interval_entry, self.pause_key_entry)
        self.setTabOrder(self.pause_key_entry, self.submit_button)

        # 设置回车键跳转到下一个输入框
        self.window_title_entry.returnPressed.connect(self.duration_entry.setFocus)
        self.duration_entry.returnPressed.connect(self.loop_interval_entry.setFocus)
        self.loop_interval_entry.returnPressed.connect(self.interval_entry.setFocus)
        self.interval_entry.returnPressed.connect(self.pause_key_entry.setFocus)
        self.pause_key_entry.returnPressed.connect(self.submit_button.setFocus)

    def on_submit(self):
        window_title = self.window_title_entry.text()
        duration = float(self.duration_entry.text())
        loop_interval = float(self.loop_interval_entry.text())
        interval = float(self.interval_entry.text())
        load_positions = self.load_positions_checkbox.isChecked()
        enable = not self.enable_checkbox.isChecked()
        save = self.save_checkbox.isChecked()
        pause_key = self.pause_key_entry.text()
        if pause_key == '':
            pause_key = 'F9'

        if load_positions:
            # 假设AutoClickUtils.get_json_all_keys()是一个方法，返回所有保存的点击位置名称
            # 这里需要你根据实际情况实现
            positions = AutoClickUtils.get_json_all_keys()
            position_name, ok = QInputDialog.getItem(self, '选择保存的点击位置', '请选择保存的点击位置的名称:',
                                                     positions, 0, False)
            if ok and position_name:
                load_positions_name = position_name
            else:
                load_positions_name = None
        else:
            load_positions_name = None

        # 这里可以添加你的逻辑代码
        position = None
        QMessageBox.information(self, '提交成功', '设置已提交')
        c = AutoClickUtils(pause_key=pause_key, load_positions=load_positions, load_positions_name=load_positions_name)
        c.set_window_always_on_top(window_title=window_title, enable=enable)
        if not load_positions:
            position = c.get_mouse_click_positions(save=save, save_name=window_title, save_mode="append")[0]
        c.click_positions_continuously(positions=position, duration=duration, loop_interval=loop_interval,
                                       interval=interval)

    def show_windows(self):
        # 显示所有窗口名字
        all_titles = AutoClickUtils.get_all_window_titles()
        msg_box = QMessageBox()
        msg_box.setWindowTitle('所有窗口名字')

        text_edit = QTextEdit()
        text_edit.setPlainText('\n'.join(all_titles))
        text_edit.setReadOnly(True)
        text_edit.setFixedSize(800, 600)  # 设置文本编辑器的固定大小

        msg_box.layout().addWidget(text_edit)
        msg_box.exec_()"""

if __name__ == '__main__':
    while True:
        enable = False
        save = False
        window_title = input("请输入目标窗口的标题: ")
        duration = float(input("请输入持续时间(小时): "))
        loop_interval = float(input("请输入循环间隔时间(秒): "))
        interval = float(input("请输入两次点击之间的间隔时间(秒): "))
        load_positions = input("是否加载已保存的点击位置(y/n):(默认不加载) ")
        if load_positions.lower() == 'y':
            load_positions = True
            print(AutoClickUtils.get_json_all_keys())
            load_positions_name = input("请选择保存的点击位置的名称: ")
        else:
            load_positions_name = None
            load_positions = False
            enable = input("是否锁定窗口(y/n):(默认不锁定) ")
            if enable.lower() == 'y':
                enable = False
            else:
                enable = True
            save = input("是否保存点击位置(y/n):(默认不保存) ")
            if save.lower() == 'y':
                save = True
            else:
                save = False
        pause_key = input("请输入暂停键(直接回车则默认为F9): ")
        position = None
        if pause_key == '':
            pause_key = 'F9'

        c = AutoClickUtils(pause_key=pause_key, load_positions=load_positions, load_positions_name=load_positions_name,
                           max_window=True)
        c.set_window_always_on_top(window_title=window_title, enable=enable)
        if not load_positions:
            position = c.get_mouse_click_positions(save=save, save_name=window_title, save_mode="append")[0]
        c.click_positions_continuously(positions=position, duration=duration, loop_interval=loop_interval,
                                       interval=interval)
        choice = input("一轮点击结束，是否继续(y/n): ")
        if choice.lower() != 'y':
            break
    # app = QApplication(sys.argv)
    # ex = AutoClickApp()
    # ex.show()
    # sys.exit(app.exec_())
