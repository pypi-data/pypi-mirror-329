from dataclasses import dataclass
import inspect
import builtins
import sys
import re
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=False)  # 将 autoreset 设置为 False，以便手动控制颜色


# 定义 PrintConfig 类来存储配置
@dataclass
class PrintConfig:
    add_line: bool = True
    add_file: bool = False
    add_class: bool = False
    add_func: bool = False
    add_time: bool = False
    flush: bool = False
    use_tee: bool = False
    terminals: tuple = ()
    structured_print: bool = False
    max_str_len: int = 100
    max_level: int = None
    max_items: int = None
    print_range: tuple = None
    struct_torch: bool = False
    struct_numpy: bool = False
    struct_pandas: bool = False


class Tee(object):
    """
    将输出同时输出到多个终端
    """

    def __init__(self, *terminals):
        self.terminals = terminals

    def __remove_ansi_escape_sequences(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mGKF]')  # 正则表达式匹配ANSI序列
        return ansi_escape.sub('', text)

    def write(self, obj):
        self.terminals = list(self.terminals)
        for f in self.terminals:
            if isinstance(obj, str):
                obj = self.__remove_ansi_escape_sequences(obj)
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.terminals:
            f.flush()


class PrintUtils:
    """
    自定义print函数，可以添加文件名、类名、函数名、行号、时间，以及手动控制文字颜色
    """
    original_print = print

    def __init__(self, config: PrintConfig):
        self.config = config
        self.add_line = config.add_line
        self.add_file = config.add_file
        self.add_class = config.add_class
        self.add_func = config.add_func
        self.add_time = config.add_time
        self.flush = config.flush
        self.struct_torch = config.struct_torch
        self.struct_numpy = config.struct_numpy
        self.struct_pandas = config.struct_pandas
        self.__enable = True
        self.__current_color = ''
        self.__skip_file_write = False

        # 结构化打印的参数
        self.structured_print = config.structured_print
        self.max_str_len = config.max_str_len
        self.max_level = config.max_level
        self.max_items = config.max_items
        self.print_range = config.print_range
        assert self.max_str_len > 0, "max_str_len必须大于0"
        assert self.max_level is None or self.max_level > 0, "max_level必须大于0"
        assert self.max_items is None or self.max_items > 0, "max_items必须大于0"

        self.tee = None
        if self.config.use_tee and self.config.terminals:
            self.tee = Tee(*self.config.terminals)

        self.__replace_print()

    def __custom_print(self, *args, **kwargs):
        if not self.__enable:
            return PrintUtils.original_print(*args, **kwargs)
        if self.structured_print and len(args) != 1:
            PrintUtils.original_print("结构化打印只支持单个参数")
            PrintUtils.original_print("将使用普通打印")
        # 如果启用了结构化打印且只有一个参数，使用结构化打印
        if self.structured_print and len(args) == 1:
            self.print_structure(args[0], max_str_len=self.max_str_len, max_level=self.max_level,
                                 max_items=self.max_items, print_range=self.print_range,
                                 struct_torch=self.struct_torch, struct_numpy=self.struct_numpy,
                                 struct_pandas=self.struct_pandas)
            return

        string = ""
        frame = self.__get_frame()

        if frame:
            if self.add_file:
                file_name = frame.f_code.co_filename
                string += f"F--{file_name}, "
            if self.add_class:
                class_name = frame.f_locals.get('self', None).__class__.__name__
                if class_name:
                    string += f"C--{class_name}, "
            if self.add_func:
                func_name = frame.f_code.co_name
                string += f"Fu--{func_name}, "
            if self.add_line:
                line_number = frame.f_lineno
                string += f"L--{line_number}, "
        if self.add_time:
            import time
            now_time = time.strftime("%H:%M:%S", time.localtime())
            string += f"T--{now_time}, "
        string = string[:-2] + "：" if string else ""

        sep = kwargs.pop('sep', ' ')
        end = kwargs.pop('end', '\n')

        output = self.__current_color + string + sep.join(map(str, args)) + Style.RESET_ALL

        PrintUtils.original_print(output, end=end, flush=self.flush, **kwargs)

        if self.tee and not self.__skip_file_write:
            self.tee.write(output + end)

        self.__skip_file_write = False

    def set_structured_print(self, enable=True, max_str_len=100, max_level=None, max_items=None):
        """设置结构化打印的参数"""
        self.structured_print = enable
        self.max_str_len = max_str_len
        self.max_level = max_level
        self.max_items = max_items

    def __get_frame(self):
        """安全地获取调用栈信息"""
        try:
            frame = inspect.currentframe()
            while frame:
                if frame.f_code.co_filename != __file__:
                    return frame
                frame = frame.f_back
        except Exception:
            pass
        return None

    def set_color(self, color):
        """设置文字颜色"""
        if color.lower() == 'red':
            self.__current_color = Fore.RED
        elif color.lower() == 'green':
            self.__current_color = Fore.GREEN
        elif color.lower() == 'blue':
            self.__current_color = Fore.BLUE
        elif color.lower() == 'yellow':
            self.__current_color = Fore.YELLOW
        else:
            self.__current_color = ''

    def reset_color(self):
        """重置文字颜色"""
        self.__current_color = ''

    def disable(self):
        self.__enable = False
        self.__restore_print()

    def enable(self):
        self.__enable = True
        self.__replace_print()

    def toggle_tee(self, *terminals):
        """切换Tee的启用状态"""
        if self.tee:
            self.tee = None
            self.__skip_file_write = True  # 设置标志
            print("Tee已禁用，当前使用普通打印。")
        elif terminals:
            self.tee = Tee(*terminals)
            self.__skip_file_write = True  # 设置标志
            print("Tee已启用。")
        else:
            print("请提供输出终端以启用Tee。")

    def __replace_print(self):
        builtins.print = self.__custom_print

    def __restore_print(self):
        builtins.print = PrintUtils.original_print

    def __del__(self):
        """析构函数，确保在对象被销毁时恢复原始的print函数"""
        self.__restore_print()

    def print_structure(self, obj, level=0, prefix='', max_str_len=100, max_level=None, max_items=None,
                        struct_torch=False, struct_numpy=False, struct_pandas=False, print_range=None):
        """
        打印任意Python对象的嵌套结构,以树状格式展示

        参数:
            obj: 要分析的对象
            level (int): 当前缩进级别
            prefix (str): 当前行的前缀字符串
            max_str_len (int): 字符串最大显示长度
            max_level (int): 最大递归深度,None表示无限制
            max_items (int): 最外层数据结构打印的最大项数,None表示无限制
            struct_torch (bool): 是否处理PyTorch张量
            struct_numpy (bool): 是否处理NumPy数组
            struct_pandas (bool): 是否处理Pandas对象
            print_range (tuple): 控制最外层打印范围的元组 (start, end)，从0开始计数
        """
        # 超过最大层级则返回
        if max_level is not None and level >= max_level:
            PrintUtils.original_print(f"{'  ' * level}└─ [达到最大递归深度]")
            return

        indent = '  ' * level

        # 处理None
        if obj is None:
            PrintUtils.original_print(f"{indent}└─ None")
            return

        # 处理基本数据类型
        if isinstance(obj, (int, float, bool, complex)):
            PrintUtils.original_print(f"{indent}└─ {type(obj).__name__}: {obj}")
            return

        # 处理字符串
        if isinstance(obj, str):
            obj_str = obj if len(obj) <= max_str_len else obj[:max_str_len - 3] + "..."
            PrintUtils.original_print(f"{indent}└─ str: '{obj_str}' (length={len(obj)})")
            return

        # 处理字节和字节数组
        if isinstance(obj, (bytes, bytearray)):
            obj_str = str(obj)
            if len(obj_str) > max_str_len:
                obj_str = obj_str[:max_str_len - 3] + "..."
            PrintUtils.original_print(f"{indent}└─ {type(obj).__name__}: {obj_str} (length={len(obj)})")
            return

        # 处理张量类型(PyTorch)
        if struct_torch:
            import torch
            if isinstance(obj, torch.Tensor):
                PrintUtils.original_print(
                    f"{indent}└─ Tensor: shape={obj.shape}, dtype={obj.dtype}, device={obj.device}")
                return

        if struct_numpy:
            import numpy as np
            if isinstance(obj, np.ndarray):
                PrintUtils.original_print(f"{indent}└─ ndarray: shape={obj.shape}, dtype={obj.dtype}")
                return

        if struct_pandas:
            import pandas as pd
            if isinstance(obj, pd.DataFrame):
                PrintUtils.original_print(f"{indent}└─ DataFrame: shape={obj.shape}, columns={list(obj.columns)}")
                return
            if isinstance(obj, pd.Series):
                PrintUtils.original_print(f"{indent}└─ Series: length={len(obj)}, name={obj.name}, dtype={obj.dtype}")
                return

        # 处理列表和元组
        if isinstance(obj, (list, tuple)):
            container_type = type(obj).__name__
            PrintUtils.original_print(f"{indent}└─ {container_type}: length={len(obj)}")
            items = obj
            if level == 0 and print_range is not None:
                start, end = print_range
                items = obj[start:end]
            elif max_items is not None and level == 0:
                items = obj[:max_items]

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                branch = '└─' if is_last else '├─'
                PrintUtils.original_print(
                    f"{indent}  {branch} [{i + (print_range[0] if level == 0 and print_range else 0)}]")
                self.print_structure(item, level + 2, max_str_len=max_str_len, max_level=max_level,
                                     max_items=max_items, struct_torch=struct_torch,
                                     struct_numpy=struct_numpy, struct_pandas=struct_pandas)
            if max_items is not None and level == 0 and len(obj) > max_items and print_range is None:
                PrintUtils.original_print(f"{indent}  └─ ... ({len(obj) - max_items} more items)")

        # 处理字典
        elif isinstance(obj, dict):
            PrintUtils.original_print(f"{indent}└─ dict: length={len(obj)}")
            items = list(obj.items())
            if level == 0 and print_range is not None:
                start, end = print_range
                items = items[start:end]
            elif max_items is not None and level == 0:
                items = items[:max_items]

            for i, (key, value) in enumerate(items):
                is_last = i == len(items) - 1
                branch = '└─' if is_last else '├─'
                PrintUtils.original_print(f"{indent}  {branch} {repr(key)}:")
                self.print_structure(value, level + 2, max_str_len=max_str_len, max_level=max_level,
                                     max_items=max_items, struct_torch=struct_torch,
                                     struct_numpy=struct_numpy, struct_pandas=struct_pandas)
            if max_items is not None and level == 0 and len(obj) > max_items and print_range is None:
                PrintUtils.original_print(f"{indent}  └─ ... ({len(obj) - max_items} more items)")

        # 处理集合
        elif isinstance(obj, (set, frozenset)):
            PrintUtils.original_print(f"{indent}└─ {type(obj).__name__}: length={len(obj)}")
            items = list(obj)
            if level == 0 and print_range is not None:
                start, end = print_range
                items = items[start:end]
            elif max_items is not None and level == 0:
                items = items[:max_items]

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                branch = '└─' if is_last else '├─'
                PrintUtils.original_print(f"{indent}  {branch} {repr(item)}")
            if max_items is not None and level == 0 and len(obj) > max_items and print_range is None:
                PrintUtils.original_print(f"{indent}  └─ ... ({len(obj) - max_items} more items)")

        # 处理可迭代对象
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            PrintUtils.original_print(f"{indent}└─ Iterable({type(obj).__name__})")
            try:
                items = list(obj)
                if level == 0 and print_range is not None:
                    start, end = print_range
                    items = items[start:end]
                elif max_items is not None and level == 0:
                    items = items[:max_items]

                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    branch = '└─' if is_last else '├─'
                    PrintUtils.original_print(
                        f"{indent}  {branch} [{i + (print_range[0] if level == 0 and print_range else 0)}]")
                    self.print_structure(item, level + 2, max_str_len=max_str_len, max_level=max_level,
                                         max_items=max_items, struct_torch=struct_torch,
                                         struct_numpy=struct_numpy, struct_pandas=struct_pandas)
                if max_items is not None and level == 0 and len(obj) > max_items and print_range is None:
                    PrintUtils.original_print(f"{indent}  └─ ... ({len(obj) - max_items} more items)")
            except:
                PrintUtils.original_print(f"{indent}  └─ [无法迭代完成]")

        # 处理对象属性
        elif hasattr(obj, '__dict__'):
            PrintUtils.original_print(f"{indent}└─ Object({type(obj).__name__})")
            attrs = vars(obj)
            items = list(attrs.items())
            if level == 0 and print_range is not None:
                start, end = print_range
                items = items[start:end]
            elif max_items is not None and level == 0:
                items = items[:max_items]

            for i, (key, value) in enumerate(items):
                is_last = i == len(items) - 1
                branch = '└─' if is_last else '├─'
                PrintUtils.original_print(f"{indent}  {branch} .{key}:")
                self.print_structure(value, level + 2, max_str_len=max_str_len, max_level=max_level,
                                     max_items=max_items, struct_torch=struct_torch,
                                     struct_numpy=struct_numpy, struct_pandas=struct_pandas)
            if max_items is not None and level == 0 and len(attrs) > max_items and print_range is None:
                PrintUtils.original_print(f"{indent}  └─ ... ({len(attrs) - max_items} more items)")

        # 处理其他所有类型
        else:
            obj_str = str(obj)
            if len(obj_str) > max_str_len:
                obj_str = obj_str[:max_str_len - 3] + "..."
            PrintUtils.original_print(f"{indent}└─ {type(obj).__name__}: {obj_str}")


class TestClass:
    def test(self):
        print("红色")


# 示例使用
if __name__ == '__main__':
    # file = open('output.txt', 'w', encoding='utf-8')
    # pr = PrintUtils(add_line=True, add_class=True, add_func=True, add_time=True, use_tee=True, terminals=(file,))
    # op = PrintUtils.original_print
    # print(12435344523465432)
    # file.close()
    print_config = PrintConfig(structured_print=True, max_items=1)
    pr = PrintUtils(print_config)
    data = {
        'list': [1, 2, 3],
        'dict': {'a': 1, 'b': [4, 5]},
        'set': {1, 2, 3}
    }
    print(data)
    # pr.set_structured_print(enable=False)
    #
    # print(data)
    # from collections import deque
    #
    # n, m = map(int, input().split())
    # queue = deque()
    # for i in range(1, n + 1):
    #     queue.append(i)
    # pr.set_structured_print(True)
    # print(queue)
