import time
from functools import wraps
from typing import List, Tuple, Union, Set, Optional, Callable, Any, Dict, get_type_hints
import collections
import logging
import inspect
import sys
import threading
import pandas as pd
from sortedcontainers import SortedSet
from yyyutils.print_utils import PrintUtils

# pr = PrintUtils(add_line=False)
# op = PrintUtils.original_print


class DecoratorUtils:
    """
    装饰器静态工具类
    """
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)
    __logger = logging.getLogger(__name__)
    __call_times_dict = {}
    __call_count_dict = {}

    @staticmethod
    def call_rate_limit(max_calls: int, period: float):
        def decorator(func):
            func_name = func.__name__
            if func_name not in DecoratorUtils.__call_times_dict:
                DecoratorUtils.__call_times_dict[func_name] = SortedSet()

            def wrapper(*args, **kwargs):
                call_times = DecoratorUtils.__call_times_dict[func_name]
                current_time = time.time()

                # 清理过期的时间戳
                while call_times and call_times[0] <= current_time - period:
                    call_times.remove(call_times[0])

                # 判断是否超过调用限制
                if len(call_times) < max_calls:
                    # 当前时间戳与上次调用时间戳间隔小于调用间隔，则等待
                    if call_times and current_time - call_times[-1] < 0.001:
                        time.sleep(0.001 - (current_time - call_times[-1]))
                        current_time = time.time()  # 更新当前时间

                    call_times.add(current_time)
                    return func(*args, **kwargs)
                else:
                    pr.red = True
                    print(f"Call rate limit exceeded for {func.__name__}     line: {inspect.getsourcelines(func)[1]}")
                    pr.red = False
                    return None

            return wrapper

        return decorator

    @staticmethod
    def call_limit(max_calls: int):
        def decorator(func):
            func_name = func.__name__
            if func_name not in DecoratorUtils.__call_count_dict:
                DecoratorUtils.__call_count_dict[func_name] = 0

            def wrapper(*args, **kwargs):
                if DecoratorUtils.__call_count_dict[func_name] < max_calls:
                    DecoratorUtils.__call_count_dict[func_name] += 1
                    return func(*args, **kwargs)
                else:
                    pr.red = True
                    print(f"Call limit exceeded for {func.__name__}     line: {inspect.getsourcelines(func)[1]}")
                    pr.red = False
                    return None

            return wrapper

        return decorator

    @staticmethod
    def print_args(func):
        """
        输出函数调用时传入的参数
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            print("Input arguments:", args if args else '', kwargs if kwargs else '')
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def run_time(func):
        """
        计算函数运行时间
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to run.")
            return result

        return wrapper

    @staticmethod
    def validate_input(func):
        """
        检查输入参数类型,支持Union, Optional, Callable, List, Tuple, Set，以及python原生类型
        :param func:
        :return:
        """

        def is_instance_of_type(value, expected_type):
            if hasattr(expected_type, '__origin__'):
                origin = expected_type.__origin__
                args = expected_type.__args__
                if origin is Union:
                    return any(is_instance_of_type(value, arg) for arg in args)
                elif origin is Optional:
                    return value is None or is_instance_of_type(value, args[0])
                elif origin is collections.abc.Callable:
                    return callable(value)
                elif origin in {list, tuple, set, dict}:
                    # print(origin, args, value)
                    if not isinstance(value, origin):
                        return False
                    return all(is_instance_of_type(k, args[0]) and is_instance_of_type(v, args[1]) for k, v in
                               value.items()) if origin is dict else all(
                        is_instance_of_type(item, args[0]) for item in value)
                return False
            else:
                if expected_type is Any:
                    return True
                return isinstance(value, expected_type) if expected_type is not int or not isinstance(value,
                                                                                                      bool) else False

        def get_detailed_type(value):
            if isinstance(value, list):
                element_types = {type(item) for item in value}
                return f"List[{next(iter(element_types)).__name__}]" if len(
                    element_types) == 1 else f"List[{', '.join(t.__name__ for t in element_types)}]"
            elif isinstance(value, tuple):
                element_types = {type(item) for item in value}
                return f"Tuple[{next(iter(element_types)).__name__}]" if len(
                    element_types) == 1 else f"Tuple[{', '.join(t.__name__ for t in element_types)}]"
            elif isinstance(value, set):
                element_types = {type(item) for item in value}
                return f"Set[{next(iter(element_types)).__name__}]" if len(
                    element_types) == 1 else f"Set[{', '.join(t.__name__ for t in element_types)}]"
            elif isinstance(value, dict):
                key_types = {type(k) for k in value.keys()}
                value_types = {type(v) for v in value.values()}
                return f"Dict[{next(iter(key_types)).__name__}, {next(iter(value_types)).__name__}]" if len(
                    key_types) == 1 and len(
                    value_types) == 1 else f"Dict[{', '.join(k.__name__ for k in key_types)}, {', '.join(v.__name__ for v in value_types)}]"
            else:
                return type(value).__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            hints = get_type_hints(func)
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs).arguments

            for arg_name, arg_value in bound_args.items():
                if arg_name in hints and not is_instance_of_type(arg_value, hints[arg_name]):
                    actual_type = get_detailed_type(arg_value)
                    raise TypeError(f"Argument '{arg_name}' must be of type {hints[arg_name]}, got {actual_type}\n"
                                    f"ErrorFunc: {func.__name__}\n"
                                    f"ErrorLine: {inspect.getsourcelines(func)[1]}")

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def singleton(cls):
        """
        单例模式装饰器
        :param cls:
        :return:
        """
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return get_instance

    @staticmethod
    def log_calls(func):
        """
        记录函数调用和返回
        :param func:
        :return:
        """

        def __get_caller_name():
            stack = inspect.stack()
            if len(stack) > 2:
                caller = stack[2].function
                return "main" if caller == "<module>" else caller
            return "main"

        def wrapper(*args, **kwargs):
            caller = __get_caller_name()
            DecoratorUtils.__logger.info(f"{caller}: Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            DecoratorUtils.__logger.info(f"{caller}: {func.__name__} returned: {result}")
            return result

        return wrapper

    @staticmethod
    def timeout(seconds=10):
        """
        在函数执行时间超过指定时间时抛出异常
        :param seconds: 超时时间（秒），支持小数
        :return:
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                timer = threading.Timer(seconds,
                                        lambda: _raise_timeout_error(func.__name__, inspect.getsourcelines(func)[1]))
                timer.start()
                try:
                    return func(*args, **kwargs)
                finally:
                    timer.cancel()

            return wrapper

        def _raise_timeout_error(func_name, decorator_line):
            raise TimeoutError(f"Function {func_name} timed out after {seconds} seconds    line: {decorator_line}")

        return decorator

    @staticmethod
    def exception_handler(default_return=None):
        """
        捕获函数执行过程中出现的异常，并打印错误信息，并返回提示信息,默认返回None
        :param default_return:
        :return:
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    pr.red = True
                    print(f"An error occurred: {e}")
                    print(f"ErrorFunc: {func.__name__}")
                    print(f"ErrorLine: {inspect.getsourcelines(func)[1]}")
                    pr.red = False
                    return default_return

            return wrapper

        return decorator

    @staticmethod
    def print_return_value(print_=True, dataframe=False, exclude_list=None):
        exclude_list = exclude_list or []

        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not print_ or func.__name__ in exclude_list:
                    return result
                # 检查调用栈，确保只在直接调用时打印返回值
                if len(inspect.stack()) == 2:
                    print(f"{func.__name__}'s return:")
                    if dataframe and isinstance(result, list):
                        try:
                            df = pd.DataFrame(result)
                            print(f"-> {df.to_string(index=False)}")
                        except Exception as e:
                            print(result)
                    else:
                        print(f"-> {result}")
                return result

            return wrapper

        return decorator

    @staticmethod
    def print_return_value_for_class(print_=True, dataframe=False, exclude_list=None):
        exclude_list = exclude_list or []

        def decorator(cls):
            for name, method in cls.__dict__.items():
                if callable(method) and not name.startswith('__') and name not in exclude_list:
                    setattr(cls, name, DecoratorUtils.print_return_value(print_, dataframe, exclude_list)(method))
            return cls

        return decorator


if __name__ == '__main__':
    @DecoratorUtils.print_return_value()
    def test_function(a: Optional[Union[tuple, List[tuple]]]):
        time.sleep(3)
        return 1


    def A():
        pass


    for i in range(10):
        print(test_function([1, 2, 3]))
