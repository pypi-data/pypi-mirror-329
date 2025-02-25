from pynput.mouse import Button, Controller, Listener
from typing import Callable, Dict


class MonitorMouseUtils:
    """
    创建一个监听鼠标的线程，在实例存在期间监听指定鼠标动作，并执行指定的回调函数。
    可以分别处理左键、中键和右键的点击事件。
    只有在按下并释放鼠标按钮时才触发点击事件。
    如果任何回调函数返回 False，则停止监听。
    """

    def __init__(self,
                 on_move: Callable = None,
                 on_left_click: Callable = None,
                 on_right_click: Callable = None,
                 on_middle_click: Callable = None,
                 on_scroll: Callable = None):
        self.on_move = on_move
        self.on_click_funcs = {
            Button.left: on_left_click,
            Button.right: on_right_click,
            Button.middle: on_middle_click
        }
        self.on_scroll = on_scroll
        self.listener = None
        self.mouse_controller = Controller()
        self.pressed_button = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __on_move(self, x, y):
        if self.on_move:
            if self.on_move.__code__.co_argcount == 0:
                result = self.on_move()
            else:
                result = self.on_move(x, y)
            if result is False:
                return False

    def __on_click(self, x, y, button, pressed):
        if pressed:
            self.pressed_button = button
        elif not pressed and self.pressed_button == button:
            if button in self.on_click_funcs and self.on_click_funcs[button]:
                func = self.on_click_funcs[button]
                argcount = func.__code__.co_argcount
                if argcount == 0:
                    result = func()
                elif argcount == 2:
                    result = func(x, y)
                else:
                    result = None
                self.pressed_button = None
                if result is False:
                    return False

    def __on_scroll(self, x, y, dx, dy):
        if self.on_scroll:
            if self.on_scroll.__code__.co_argcount == 0:
                result = self.on_scroll()
            elif self.on_scroll.__code__.co_argcount == 2:
                result = self.on_scroll(dx, dy)
            else:
                result = self.on_scroll(x, y, dx, dy)
            if result is False:
                return False

    def start(self):
        self.listener = Listener(
            on_move=self.__on_move,
            on_click=self.__on_click,
            on_scroll=self.__on_scroll
        )
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()


# 示例用法
def on_move():
    print("鼠标移动了")


def on_left_click():
    print("鼠标左键点击")
    return False  # 左键点击后停止监听


def on_right_click():
    print("鼠标右键点击")


def on_middle_click():
    print("鼠标中键点击")


def on_scroll():
    print("鼠标滚动")


if __name__ == '__main__':
    with MonitorMouseUtils(
            on_move=on_move,
            on_left_click=on_left_click,
            on_right_click=on_right_click,
            on_middle_click=on_middle_click,
            on_scroll=on_scroll
    ):
        print("鼠标监控已启动，左键点击（按下并释放）将停止监听...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("监控已停止")
