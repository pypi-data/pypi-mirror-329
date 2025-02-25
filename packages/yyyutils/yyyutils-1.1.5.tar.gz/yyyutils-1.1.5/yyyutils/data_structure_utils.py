import re
from collections import deque


class ListUtils:
    """
    列表相关的工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def extract_all_elements(lst):
        """
        用于提取列表或者多重列表中的所有元素，返回一个列表
        """
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(ListUtils.extract_all_elements(item))
            elif isinstance(item, tuple):
                result.extend(ListUtils.extract_all_elements(list(item)))
            else:
                result.append(item)
        return result

    @staticmethod
    def extend_lists(*lsts):
        """
        用于将多个列表拼接成一个列表
        """
        result = []
        for lst in lsts:
            result.extend(lst)
        return result

    @staticmethod
    def get_duplicates(lst):
        """
        用于获取列表中重复的元素，返回一个列表
        """
        duplicates = []
        for item in lst:
            if lst.count(item) > 1 and item not in duplicates:
                duplicates.append(item)
        return duplicates

    @staticmethod
    def get_unique_elements(lst):
        """
        用于获取列表中唯一的元素，返回一个列表
        """
        unique_elements = []
        duplicates = ListUtils.get_duplicates(lst)
        for item in lst:
            if item not in duplicates:
                unique_elements.append(item)
        return unique_elements

    @staticmethod
    def quchong(lst):
        """
        去除重复项，重复元素留下一个就行
        :param lst:
        :return:
        """
        new_lst = []
        for item in lst:
            if item not in new_lst:
                new_lst.append(item)
        return new_lst

    @staticmethod
    def split_list_by_none(lst):
        """
        用于将列表中包含None的元素分割成多个子列表，返回一个列表
        """
        result = []
        sublist = []

        for item in lst:
            if item is None:
                if sublist:
                    result.append(sublist)
                    sublist = []
            else:
                sublist.append(item)

        if sublist:
            result.append(sublist)

        return result

    @staticmethod
    def split_list_by_value(lst, value):
        """
        用于将列表中包含特定值的元素分割成多个子列表，返回一个列表
        """
        result = []
        sublist = []

        for item in lst:
            if item == value:
                if sublist:
                    result.append(sublist)
                    sublist = []
            else:
                sublist.append(item)

        if sublist:
            result.append(sublist)

        return result


class DictUtils:
    """
    字典相关的工具类，类属性current_floor用于dict_data_extractor函数中在各层之间传递递归的层级，类属性value_list用于记录dict_data_extractor函数中提取的值
    """
    __current_floor = 1
    __value_list = []

    def __init__(self):
        pass

    @staticmethod
    def dict_value_comparer_with_same_keys(dict1: dict, dict2: dict) -> list:
        """
        比较两个有相同键的字典，返回不同的值 的 键的列表
        """
        if len(dict1) != len(dict2):
            raise ValueError("The two dicts have different lengths, cannot compare")
        diff_value_keys = []
        for key, value in dict1.items():
            if dict2[key] != value:
                diff_value_keys.append(key)
        return diff_value_keys

    @staticmethod
    def dict_key_comparer(dict1: dict, dict2: dict) -> tuple:
        """
        比较两个字典，分别返回两个字典独有的键的列表
        """
        if len(dict1) != len(dict2):
            print("The two dicts have different lengths")
        else:
            print("The two dicts have same lengths")
        additional_keys_in_dict1, additional_keys_in_dict2 = [], []
        for key in dict1.keys():
            if key not in dict2.keys():
                additional_keys_in_dict1.append(key)
        for key in dict2.keys():
            if key not in dict1.keys():
                additional_keys_in_dict2.append(key)
        if not additional_keys_in_dict1 and not additional_keys_in_dict2:
            print("The two dicts have same keys")
        else:
            print("The two dicts have different keys")
            return additional_keys_in_dict1, additional_keys_in_dict2

    @staticmethod
    def __incrementing_generator():
        n = 1
        while True:
            yield n
            n += 1

    @staticmethod
    def __dict_data_extractor(dict_data: dict, key_name: str, max_depth: int):
        """
        递归的提取多重字典中的特定键对应的值，并返回一个列表, 其中每个元素是一个元组，包含值和层级
        max_depth: 最大递归层级
        """
        current_floor = DictUtils.__current_floor
        if current_floor > max_depth:
            print(f"Max depth reached: {max_depth}")
            return

        if isinstance(dict_data, dict):
            for key, value in dict_data.items():
                if key == key_name:
                    DictUtils.__value_list.append((value, current_floor))
                DictUtils.__current_floor += 1
                DictUtils.__dict_data_extractor(value, key_name, max_depth)
                DictUtils.__current_floor -= 1
        elif isinstance(dict_data, (list, tuple)):
            for item in dict_data:
                DictUtils.__current_floor += 1
                DictUtils.__dict_data_extractor(item, key_name, max_depth)
                DictUtils.__current_floor -= 1

    @staticmethod
    def dict_data_extractor(dict_data: dict, key_names: list, max_depth: int = 10, need_depth: int = None):
        """
        封装了__dict_data_extractor函数,并且在执行完__dict_data_extractor函数后，重置类属性current_floor和value_list
        """
        key_names = list(key_names)
        result = {}
        for key_name in key_names:
            DictUtils.__current_floor = 1
            DictUtils.__value_list = []
            DictUtils.__dict_data_extractor(dict_data, key_name, max_depth)
            result[key_name] = DictUtils.__value_list
        if need_depth is not None:
            result = {key: [t[0] for t in value if t[-1] == need_depth] for key, value in result.items()}
        return result

    @staticmethod
    def dict_data_extractor_loop(dict_data, key_names, max_depth=10, need_depth=None):
        result = {key: [] for key in key_names}  # 存储每个键名的结果
        stack = deque([(dict_data, 1)])  # 使用队列存储待处理的项和层级

        while stack:
            current_data, current_floor = stack.popleft()
            # 如果超出最大深度或当前数据不是字典或列表，则继续
            if current_floor > max_depth or not isinstance(current_data, (dict, list)):
                if current_floor > max_depth:
                    print(f"Max depth reached: {max_depth}")
                continue

            if isinstance(current_data, dict):
                for key, value in current_data.items():
                    # 如果找到目标键，记录其值和层级
                    if key in key_names:
                        result[key].append((value, current_floor))
                    # 将值和层级压入栈中继续处理
                    stack.append((value, current_floor + 1))
            elif isinstance(current_data, (list, tuple)):
                for item in current_data:
                    stack.append((item, current_floor + 1))
        if need_depth is not None:
            result = {key: [t[0] for t in value if t[-1] == need_depth] for key, value in result.items()}
        return result


class StringUtils:
    """
    字符串相关的工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def transform_to_original_str(text):
        """
        将unicode字符串转换为原始字符串
        """
        return repr(text)[1:-1]

    @staticmethod
    def b_is_substring_of_a(a, b):
        """
        检查B是不是A的子串，可以是不连续的但是顺序必须一致
        """
        it = iter(a)
        return all(item in it for item in b)

    @staticmethod
    def remove_all_marks(text):
        text = re.sub(r'[^\w\s]', '', text)
        return text

    @staticmethod
    def remove_all_spaces(text):
        text = re.sub(r'\s+', '', text)
        return text

    @staticmethod
    def replace_char_in_text(text, char, replace_char=''):
        """
        替换文本中的特定字符
        """
        return text.replace(char, replace_char)

    @staticmethod
    def split_text_by_separator_to_list(text, separator):
        """
        根据分隔符分割文本，返回列表
        """
        return text.split(separator)

    @staticmethod
    def split_text_by_separator_to_tuple(text, separator):
        """
        根据分隔符分割文本，返回元组
        """
        return tuple(text.split(separator))

    @staticmethod
    def transform_input_to_t_list(input_str, separator1, separator2):
        """
        将输入字符串转换为嵌套列表，其中子列表的元素用separator2分割，子列表用separator1分割
        :return:
        """
        temp_list = StringUtils.split_text_by_separator_to_list(input_str, separator1)
        result_list = []
        for item in temp_list:
            result_list.append(StringUtils.split_text_by_separator_to_tuple(item, separator2))
        return result_list


if __name__ == '__main__':
    deep_dict = {'a': {'a': 'a', 'b': 'a', 'o': [{'o': 's'}, {'o': 'ss'}]},
                 'b': {'c': [{'b': 'bbb'}], 'b': {'b': {'b': 'd'}, 'c': {'b': 'ddd'}}}, 'o': 'p',
                 'e': {'e': {'f': {'e': {'o': 'ooo'}}}}}
    print(DictUtils.dict_data_extractor(deep_dict, ['o']))
    print(DictUtils.dict_data_extractor(deep_dict, ['c']))
    print(DictUtils.dict_data_extractor(deep_dict, ['e']))
    print(DictUtils.dict_data_extractor(deep_dict, ['b', 'e'], need_depth=2))
    print(DictUtils.dict_data_extractor_loop(deep_dict, ['b', 'e']))
    # a = [None, 1, 3, None, 5, None, 7, None, 9, None, None]
    # print(ListUtils.split_list_by_none(a))
