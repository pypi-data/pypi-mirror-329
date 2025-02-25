import win32api
import win32con
import win32gui
from typing import Tuple
from pynput import mouse
from yyyutils.auto_utils.moniter.moniter_keyboard_utils import MoniterKeyboardUtils


class MouseUtils:
    def __init__(self):
        self.click_positions = []
        self.max_click_num = 10

    def __on_click(self, x, y, button, pressed):
        if pressed:
            self.click_positions.append((x, y))
            print(f"已记录点击位置: ({x}, {y})")
            if len(self.click_positions) >= self.max_click_num:  # 假设我们只记录10次点击
                self.get_position_stop_flag = True  # 停止监听
                return False  # 停止监听

    def __on_press_esc1(self):
        self.get_position_stop_flag = True  # 停止监听
        return False  # 停止监听

    def get_mouse_click_positions(self) -> list:
        """
        获取鼠标点击时位置，而不是当前鼠标位置
        :return:
        """
        with mouse.Listener(on_click=self.__on_click):
            with MoniterKeyboardUtils('esc', toggle_clicking_func=self.__on_press_esc1):
                while not self.get_position_stop_flag:  # 保持监听直到停止
                    pass

        return self.click_positions

    @staticmethod
    def get_mouse_click_position(button: str = 'left') -> Tuple[int, int]:
        """
        获取鼠标点击时位置，打印出来并且返回
        :param button: 要监听的鼠标按钮（'left'、'right' 或 'middle'）
        :return: 鼠标点击位置（x, y）
        """
        if button.lower() not in ['left', 'right', 'middle']:
            raise ValueError(f"Invalid button: {button}")
        position = None

        def on_click(x, y, btn, pressed):
            nonlocal position
            if pressed:
                if button.lower() == 'left' and btn == mouse.Button.left:
                    position = (x, y)
                    print(f"左键点击位置: ({x}, {y})")
                    return False  # 停止监听
                elif button.lower() == 'right' and btn == mouse.Button.right:
                    position = (x, y)
                    print(f"右键点击位置: ({x}, {y})")
                    return False  # 停止监听
                elif button.lower() == 'middle' and btn == mouse.Button.middle:
                    position = (x, y)
                    print(f"中键点击位置: ({x}, {y})")
                    return False  # 停止监听

        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()
        mouse_listener.join()
        return position

    @staticmethod
    def move_window(handle: int, x: int, y: int, width: int, height: int) -> None:
        """移动并调整窗口大小"""
        win32gui.MoveWindow(handle, x, y, width, height, True)

    @staticmethod
    def get_cursor_pos() -> Tuple[int, int]:
        """获取鼠标位置"""
        return win32api.GetCursorPos()

    @staticmethod
    def set_cursor_pos(x: int, y: int) -> None:
        """设置鼠标位置"""
        win32api.SetCursorPos((x, y))

    @staticmethod
    def click_mouse(button: str, x: int, y: int) -> None:
        """
        在指定位置点击鼠标按钮
        :param button: 鼠标按钮 ('left', 'right', 'middle')
        :param x: 点击位置的x坐标
        :param y: 点击位置的y坐标
        """
        button_map = {
            'left': (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
            'right': (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
            'middle': (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP)
        }
        down, up = button_map.get(button.lower(), (None, None))
        if down is None or up is None:
            raise ValueError(f"Invalid button: {button}")

        # 移动鼠标到指定位置
        win32api.SetCursorPos((x, y))

        # 执行点击操作
        win32api.mouse_event(down, x, y, 0, 0)
        win32api.mouse_event(up, x, y, 0, 0)

    @staticmethod
    def roll_middle_button(x: int, y: int, scroll_amount: int = 1, one=120) -> None:
        """
        在指定位置滚动鼠标滚轮
        :param x: 滚动位置的x坐标
        :param y: 滚动位置的y坐标
        :param scroll_amount: 滚动量，正值向下滚动，负值向上滚动，默认为120
        :param one: 滚动单位，默认为120
        """
        # 移动鼠标到指定位置
        win32api.SetCursorPos((x, y))
        scroll_amount = -scroll_amount * one

        # 执行滚轮事件
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, scroll_amount, 0)


if __name__ == '__main__':
    from yyyutils.window_utils import WindowUtils

    WindowUtils.set_window_topmost(WindowUtils.get_all_hwnds_and_titles_by_process_name('Poe')[2][0], False)
    MouseUtils.roll_middle_button(800, 300, 30)
