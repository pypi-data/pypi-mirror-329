from pynput.keyboard import Key, KeyCode, Listener, Controller
from typing import Callable, List, Union
from yyyutils.decorator_utils import DecoratorUtils


class MoniterKeyboardUtils:
    """
    创建一个监听键盘的线程，在实例存在期间监听指定键盘组合，并执行指定的回调函数。
    """
    default_control_keys = {
        'key.ctrl_l', 'key.ctrl_r', 'key.alt_l', 'key.alt_r', 'key.cmd_l', 'key.cmd_r', 'key.win_l', 'key.win_r',
        'key.ctrl', 'key.alt', 'key.cmd', 'key.win'
    }

    ctrl_chars = {
        '\x01': 'a', '\x02': 'b', '\x03': 'c', '\x04': 'd', '\x05': 'e',
        '\x06': 'f', '\x07': 'g', '\x08': 'h', '\x09': 'i', '\x0a': 'j',
        '\x0b': 'k', '\x0c': 'l', '\x0d': 'm', '\x0e': 'n', '\x0f': 'o',
        '\x10': 'p', '\x11': 'q', '\x12': 'r', '\x13': 's', '\x14': 't',
        '\x15': 'u', '\x16': 'v', '\x17': 'w', '\x18': 'x', '\x19': 'y',
        '\x1a': 'z', '<48>': '0', '<49>': '1', '<50>': '2', '<51>': '3',
        '<52>': '4', '<53>': '5', '<54>': '6', '<55>': '7', '<56>': '8',
        '<57>': '9', '<186>': ';', '<187>': '=', '<188>': ',', '<189>': '-',
        '<190>': '.', '<191>': '/', '<192>': '`', '<222>': "'",
        '': '[', '': ']', '': '\\'
    }

    @DecoratorUtils.validate_input
    def __init__(self, keys: Union[str, List[str], Key], toggle_clicking_func: Callable = None,
                 toggle_release_func: Callable = None):
        self.common_keys, self.control_keys = self._parse_keys(keys if isinstance(keys, list) else [keys])
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.__toggle_clicking_func = toggle_clicking_func
        self.__toggle_release_func = toggle_release_func
        self.__pressed_control_keys = set()
        self.__pressed_common_keys = set()
        self.keyboard_controller = Controller()
        self.__pressed = False

    def _parse_keys(self, keys: List[str]):
        parsed_control_keys = set()
        parsed_common_keys = set()
        for key in keys:
            if isinstance(key, Key):
                key = str(key).lower()
            else:
                key = key.lower()
            try:
                parsed_key = str(getattr(Key, key)).lower()
            except AttributeError:
                parsed_key = key

            if parsed_key in self.default_control_keys:
                parsed_control_keys.add(parsed_key.split('_')[0])
            else:
                parsed_common_keys.add(parsed_key)
        return parsed_common_keys, parsed_control_keys

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __on_press(self, key):
        str_key = self._get_str_key(key)

        if str_key in self.ctrl_chars:
            if 'key.ctrl' in self.control_keys and self.ctrl_chars[str_key] in self.common_keys:
                self.__pressed_control_keys.add('key.ctrl')
                self.__pressed_common_keys.add(self.ctrl_chars[str_key])
        elif str_key in self.default_control_keys:
            str_key = str_key.split('_')[0]
            if str_key in self.control_keys:
                self.__pressed_control_keys.add(str_key)
        elif str_key in self.common_keys:
            self.__pressed_common_keys.add(str_key)

        if self.__pressed_common_keys == self.common_keys and self.__pressed_control_keys == self.control_keys:
            if self.__toggle_clicking_func:
                self.__toggle_clicking_func()
            self.__pressed = True

    from pynput.keyboard import Key, KeyCode, Listener, Controller
    from typing import Callable, List, Union

    class MoniterKeyboardUtils:
        """
        创建一个监听键盘的线程，在实例存在期间监听指定键盘组合，并执行指定的回调函数。
        """
        default_control_keys = {
            'key.ctrl_l', 'key.ctrl_r', 'key.alt_l', 'key.alt_r', 'key.cmd_l', 'key.cmd_r', 'key.win_l', 'key.win_r',
            'key.ctrl', 'key.alt', 'key.cmd', 'key.win'
        }

        ctrl_chars = {
            '\x01': 'a', '\x02': 'b', '\x03': 'c', '\x04': 'd', '\x05': 'e',
            '\x06': 'f', '\x07': 'g', '\x08': 'h', '\x09': 'i', '\x0a': 'j',
            '\x0b': 'k', '\x0c': 'l', '\x0d': 'm', '\x0e': 'n', '\x0f': 'o',
            '\x10': 'p', '\x11': 'q', '\x12': 'r', '\x13': 's', '\x14': 't',
            '\x15': 'u', '\x16': 'v', '\x17': 'w', '\x18': 'x', '\x19': 'y',
            '\x1a': 'z', '<48>': '0', '<49>': '1', '<50>': '2', '<51>': '3',
            '<52>': '4', '<53>': '5', '<54>': '6', '<55>': '7', '<56>': '8',
            '<57>': '9', '<186>': ';', '<187>': '=', '<188>': ',', '<189>': '-',
            '<190>': '.', '<191>': '/', '<192>': '`', '<222>': "'",
            '': '[', '': ']', '': '\\'
        }

        def __init__(self, keys: Union[str, List[str], Key], toggle_clicking_func: Callable = None,
                     toggle_release_func: Callable = None):
            self.common_keys, self.control_keys = self._parse_keys(keys if isinstance(keys, list) else [keys])
            self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
            self.__toggle_clicking_func = toggle_clicking_func
            self.__toggle_release_func = toggle_release_func
            self.__pressed_control_keys = set()
            self.__pressed_common_keys = set()
            self.keyboard_controller = Controller()
            self.__pressed = False

        def _parse_keys(self, keys: List[str]):
            parsed_control_keys = set()
            parsed_common_keys = set()
            for key in keys:
                if isinstance(key, Key):
                    key = str(key).lower()
                else:
                    key = key.lower()
                try:
                    parsed_key = str(getattr(Key, key)).lower()
                except AttributeError:
                    parsed_key = key

                if parsed_key in self.default_control_keys:
                    parsed_control_keys.add(parsed_key.split('_')[0])
                else:
                    parsed_common_keys.add(parsed_key)
            return parsed_common_keys, parsed_control_keys

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop()

        def __on_press(self, key):
            str_key = self._get_str_key(key)

            if str_key in self.ctrl_chars:
                if 'key.ctrl' in self.control_keys and self.ctrl_chars[str_key] in self.common_keys:
                    self.__pressed_control_keys.add('key.ctrl')
                    self.__pressed_common_keys.add(self.ctrl_chars[str_key])
            elif str_key in self.default_control_keys:
                str_key = str_key.split('_')[0]
                if str_key in self.control_keys:
                    self.__pressed_control_keys.add(str_key)
            elif str_key in self.common_keys:
                self.__pressed_common_keys.add(str_key)

            if self.__pressed_common_keys == self.common_keys and self.__pressed_control_keys == self.control_keys:
                if self.__toggle_clicking_func:
                    self.__toggle_clicking_func()
                self.__pressed = True

        def __on_release(self, key):
            str_key = self._get_str_key(key)

            if str_key in self.ctrl_chars:
                self.__pressed_common_keys.discard(self.ctrl_chars[str_key])
            if str_key in self.default_control_keys:
                str_key = str_key.split('_')[0]
                self.__pressed_control_keys.discard(str_key)
            else:
                self.__pressed_common_keys.discard(str_key)

            if self.__pressed and not self.__pressed_common_keys and not self.__pressed_control_keys:
                if self.__toggle_release_func:
                    self.__toggle_release_func()
                self.__pressed = False

        @staticmethod
        def _get_str_key(key):
            if isinstance(key, Key):
                return str(key).lower()
            elif isinstance(key, KeyCode):
                return key.char.lower() if key.char else str(key)
            return str(key).lower()

        def start(self):
            self.listener.start()

        def stop(self):
            self.listener.stop()

    def on_press():
        print("Keys pressed!")

    def on_release():
        print("Keys released!")

    # 监听组合键
    if __name__ == '__main__':
        with MoniterKeyboardUtils(['ctrl', 'a'], 'on_press', 'on_release'):
            while True:
                pass

    def __on_release(self, key):
        str_key = self._get_str_key(key)

        if str_key in self.ctrl_chars:
            self.__pressed_common_keys.discard(self.ctrl_chars[str_key])
        if str_key in self.default_control_keys:
            str_key = str_key.split('_')[0]
            self.__pressed_control_keys.discard(str_key)
        else:
            self.__pressed_common_keys.discard(str_key)

        if self.__pressed and not self.__pressed_common_keys and not self.__pressed_control_keys:
            if self.__toggle_release_func:
                self.__toggle_release_func()
            self.__pressed = False

    @staticmethod
    def _get_str_key(key):
        if isinstance(key, Key):
            return str(key).lower()
        elif isinstance(key, KeyCode):
            return key.char.lower() if key.char else str(key)
        return str(key).lower()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()


def on_press():
    print("Keys pressed!")


def on_release():
    print("Keys released!")


# 监听组合键
if __name__ == '__main__':
    with MoniterKeyboardUtils(['ctrl', 'a'], 'on_press', 'on_release'):
        while True:
            pass
