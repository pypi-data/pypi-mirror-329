import pyautogui
import time
from pynput import keyboard
from yyyutils.auto_utils.moniter.moniter_keyboard_utils import MoniterKeyboardUtils


class AutoPressUtils:
    """
    用于自动点击键盘按键的工具类
    """

    @staticmethod
    def press_key(key):
        """
        按下指定的键
        :param key:
        :return:
        """
        pyautogui.press(key)

    @staticmethod
    def press_keys_together(keys: list):
        """
        按下指定的多个键，是同时按下的效果
        :param keys:
        :return:
        """
        pyautogui.hotkey(*keys)

    @staticmethod
    def press_keys_continuously(keys: list, interval: float):
        """
        模拟连续按下指定的多个键，间隔时间为interval
        :param keys:
        :param interval:
        :return:
        """
        for key in keys:
            pyautogui.keyDown(key)
            pyautogui.sleep(interval)
            pyautogui.keyUp(key)

    @staticmethod
    def press_key_with_duration(key: str, duration: float, interval: float = 0.05):
        stop_flag = False
        start_time = time.time()
        controller = keyboard.Controller()

        def click_func():
            """
            停止按键的函数
            :return:
            """
            nonlocal stop_flag
            stop_flag = True

        with MoniterKeyboardUtils('esc', click_func):
            while not stop_flag and (time.time() - start_time) < duration:
                controller.press(key)
                controller.release(key)
                time.sleep(interval)

    @staticmethod
    def press_keys_continuously_with_duration(keys: list, duration_interval: float, interval: float = 0.05,
                                              duration: float = 10):
        """
        多次运行press_keys_continuously，直到duration时间结束
        :param keys:
        :param duration:
        :param interval:
        :return:
        """
        start_time = time.time()
        while (time.time() - start_time) < duration:
            AutoPressUtils.press_keys_continuously(keys, interval)
            time.sleep(duration_interval)


if __name__ == '__main__':
    AutoPressUtils.press_key_with_duration('a', 10)
