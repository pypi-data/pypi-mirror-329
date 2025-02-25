import os
import shutil
import pandas
from yyyutils.data_structure_utils import StringUtils
import tkinter as tk
from tkinter import filedialog
import uuid


class OSUtils:
    """
    这个类提供一些关于文件操作的静态工具函数
    """

    @staticmethod
    def generate_random_file_name(file_name_prefix="", file_name_extension="", length=10):
        """
        这个函数用来生成随机文件名
        """

        def generate_random_string(length):
            """
            这个函数用来生成随机字符串
            """
            import random
            import string
            letters_and_numbers = string.ascii_lowercase + string.ascii_uppercase + string.digits  # 包括大小写字母和数字
            return ''.join(random.choice(letters_and_numbers) for i in range(length))

        if not file_name_extension.startswith('.'):
            file_name_extension = '.' + file_name_extension
        if not file_name_extension:
            raise ValueError("The file name extension should not be empty.")
        return file_name_prefix + generate_random_string(length) + file_name_extension

    @staticmethod
    def generate_unique_file_names(file_name_prefix="", file_name_extension="", length=10, num=1):
        """
        这个函数用来生成一组随机文件名
        """
        file_names = []
        for i in range(num):
            file_name = OSUtils.generate_random_file_name(file_name_prefix, file_name_extension, length)
            while file_name in file_names:
                file_name = OSUtils.generate_random_file_name(file_name_prefix, file_name_extension, length)
            file_names.append(file_name)
        return file_names

    @staticmethod
    def generate_unique_file_name_by_uuid(file_name_extension):
        """
        利用uuid生成唯一文件名
        :param file_name_extension:
        :return:
        """
        # 生成一个唯一的UUID
        unique_id = uuid.uuid4()

        # 去掉UUID中的短横线
        unique_id_str = str(unique_id).replace('-', '')

        # 创建唯一的文件名
        unique_file_name = f"{unique_id_str}{file_name_extension}"
        return unique_file_name

    @staticmethod
    def generate_unique_file_names_by_uuid(file_name_extension, num=1):
        """
        利用uuid生成一组唯一文件名
        :param file_name_extension:
        :param num:
        :return:
        """
        # 生成一组唯一的UUID
        unique_ids = [uuid.uuid4() for i in range(num)]

        # 去掉UUID中的短横线
        unique_id_strs = [str(unique_id).replace('-', '') for unique_id in unique_ids]

        # 创建一组唯一的文件名
        unique_file_names = [f"{unique_id_str}{file_name_extension}" for unique_id_str in unique_id_strs]
        return unique_file_names

    @staticmethod
    def chick_file_name_exist_in_single_directory(directory, file_name):
        """
        检查某个文件名（包括后缀）是否已经存在于某文件夹
        :param directory:
        :param file_name:
        :return:
        """
        if os.path.exists(os.path.join(directory, file_name)):
            return True
        else:
            return False

    @staticmethod
    def chick_file_name_exist_in_directory(directory, file_name):
        """
        检查某个文件名（包括后缀）是否已经存在于某文件夹及其子文件夹
        :param directory:
        :param file_name:
        :return:
        """
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                return True
        return False

    @staticmethod
    def get_all_files_in_directory(directory):
        """
        这个函数用来获取指定目录下所有文件（包括子目录）的绝对路径
        """
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                found_files.append(os.path.join(root, file))
                files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_single_directory(directory):
        """
        这个函数用来获取指定目录下所有文件（不包括子目录）的绝对路径
        """
        found_files = []
        files_name = []
        for file in os.listdir(directory):
            found_files.append(os.path.join(directory, file))
            files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_file_name_and_extension(file_path, need_dir=False):
        """
        这个函数用来获取文件的除去扩展名的路径，文件名和扩展名
        """
        file_name_with_extension = os.path.basename(file_path)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        file_path_without_file_name = os.path.dirname(file_path)
        res = [file_name, file_extension, file_name_with_extension]
        if need_dir:
            res.append(file_path_without_file_name)
        return res

    @staticmethod
    def rename_file(old_file_path, new_file_path, overwrite=False):
        """
        这个函数用来重命名文件
        """
        if os.path.exists(new_file_path) and not overwrite:
            raise FileExistsError("The new file already exists.")
        elif os.path.exists(new_file_path) and overwrite:
            os.remove(new_file_path)
        os.rename(old_file_path, new_file_path)
        return new_file_path

    @staticmethod
    def get_all_files_in_single_directory_by_name_extension(directory, name_extension):
        """
        这个函数用来获取指定目录下所有文件（不包括子目录）的绝对路径
        """
        if not name_extension.startswith('.'):
            name_extension = '.' + name_extension
        found_files = []
        files_name = []
        for file in os.listdir(directory):
            if file.endswith(name_extension):
                found_files.append(os.path.join(directory, file))
                files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_single_directory_by_name_or_name_prefix(directory, name):
        """
        这个函数用来获取指定目录下所有以指定名称开头的文件的绝对路径
        """
        found_files = []
        files_name = []
        for file in os.listdir(directory):
            if file.startswith(name):
                found_files.append(os.path.join(directory, file))
                files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_single_directory_by_name(directory, name):
        """
        这个函数用来获取指定目录下所有指定名称的文件的绝对路径
        """
        found_files = []
        files_name = []
        for file in os.listdir(directory):
            if file == name:
                found_files.append(os.path.join(directory, file))
                files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_single_directory_name_include_string(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的文件的绝对路径
        """
        found_files = []
        files_name = []
        for file in os.listdir(directory):
            if string in file:
                found_files.append(os.path.join(directory, file))
                files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_single_directory_name_include_string_discontinuous(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的文件的名称,可以是不连续但按顺序出现的指定字符串
        """
        found_files = []
        files_name = []
        for files in os.listdir(directory):
            for file in files:
                if StringUtils.b_is_substring_of_a(file, string):
                    found_files.append(os.path.join(directory, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_directory_by_name_extension(directory, name_extension):
        """
        这个函数用来获取指定目录下所有指定后缀的文件的绝对路径
        """
        if not name_extension.startswith('.'):
            name_extension = '.' + name_extension
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(name_extension):
                    found_files.append(os.path.join(root, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_directory_by_name_or_name_prefix(directory, name):
        """
        这个函数用来获取指定目录下所有指定名称或者以指定名称开头的文件的绝对路径
        """
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith(name):
                    found_files.append(os.path.join(root, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_directory_by_name(directory, name):
        """
        这个函数用来获取指定目录下所有指定名称的文件的绝对路径
        """
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == name:
                    found_files.append(os.path.join(root, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_directory_name_include_string(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的文件的绝对路径
        """
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if string in file:
                    found_files.append(os.path.join(root, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_files_in_directory_name_include_string_discontinuous(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的文件的名称,可以是不连续但按顺序出现的指定字符串
        """
        found_files = []
        files_name = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if StringUtils.b_is_substring_of_a(file, string):
                    found_files.append(os.path.join(root, file))
                    files_name.append(file)
        return found_files, files_name, len(found_files)

    @staticmethod
    def get_all_subdirectories(directory):
        """
        这个函数用来获取指定目录下所有子目录的绝对路径
        """
        found_subdirectories = []
        subdirectories_name = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                found_subdirectories.append(os.path.join(root, d))
                subdirectories_name.append(d)
        return found_subdirectories, subdirectories_name, len(found_subdirectories)

    @staticmethod
    def get_all_directories_in_single_directory_by_name_or_name_prefix(directory, name):
        """
        这个函数用来获取指定目录下所有以指定名称开头的目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)) and file.startswith(name):
                found_directories.append(os.path.join(directory, file))
                directories_name.append(file)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_single_directory(directory):
        """
        这个函数用来获取指定目录下所有子目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                found_directories.append(os.path.join(directory, file))
                directories_name.append(file)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_single_directory_name_include_string1(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)) and string in file:
                found_directories.append(os.path.join(directory, file))
                directories_name.append(file)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_single_directory_name_include_string2(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的目录的名称,可以是不连续但按顺序出现的指定字符串
        """
        found_directories = []
        directories_name = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)) and StringUtils.b_is_substring_of_a(file,
                                                                                                string):
                found_directories.append(os.path.join(directory, file))
                directories_name.append(file)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_directory_by_name_or_name_prefix(directory, name):
        """
        这个函数用来获取指定目录下所有以指定名称开头的目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                if d.startswith(name):
                    found_directories.append(os.path.join(root, d))
                    directories_name.append(d)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_directory_by_name(directory, name):
        """
        这个函数用来获取指定目录下所有指定名称的目录的绝对路径
        """
        found_directories = []
        directories_name = []

        for root, dirs, files in os.walk(directory):
            for d in dirs:
                if d == name:
                    found_directories.append(os.path.join(root, d))
                    directories_name.append(d)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_directory(directory):
        """
        这个函数用来获取指定目录下所有子目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                found_directories.append(os.path.join(root, d))
                directories_name.append(d)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_directory_name_include_string1(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的目录的绝对路径
        """
        found_directories = []
        directories_name = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                if string in d:
                    found_directories.append(os.path.join(root, d))
                    directories_name.append(d)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_all_directories_in_directory_name_include_string2(directory, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的目录的名称,可以是不连续但按顺序出现的指定字符串
        """
        found_directories = []
        directories_name = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                if StringUtils.b_is_substring_of_a(d, string):
                    found_directories.append(os.path.join(root, d))
                    directories_name.append(d)
        return found_directories, directories_name, len(found_directories)

    @staticmethod
    def get_size_of_directory(directory):
        """
        这个函数用来获取指定目录的大小
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return f'{total_size / (1024 * 1024):.3f} MB'

    @staticmethod
    def get_size_of_file(file_path):
        """
        这个函数用来获取指定文件的大小
        """
        return f'{os.path.getsize(file_path) / (1024 * 1024):.3f} MB'

    @staticmethod
    def print_file_or_directory_list(file_or_directory_list):
        """
        这个函数用来打印文件或目录列表,可以直接复制到文件管理器中打开
        """
        for file_or_directory in file_or_directory_list:
            print(file_or_directory)

    @staticmethod
    def change_all_files_in_directory_name_extension(directory, old_extension, new_extension):
        """
        这个函数用来修改指定目录及其子目录下所有指定后缀的文件的后缀,直接硬改，可能无法满足要求，甚至出现文件损坏
        """
        if not old_extension.startswith('.'):
            old_extension = '.' + old_extension

        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension

        for root, dirs, files in os.walk(directory):
            count = 0
            for file in files:
                if file.endswith(old_extension):
                    os.rename(os.path.join(root, file), os.path.join(root, file.replace(old_extension, new_extension)))
                    count += 1
            print(f'修改{count}个文件后缀成功')

    @staticmethod
    def change_all_files_in_single_directory_name_extension(directory, old_extension, new_extension):
        """
        这个函数用来修改指定目录下所有指定后缀的文件的后缀，直接硬改，可能无法满足要求，甚至出现文件损坏
        """
        count = 0
        for file in os.listdir(directory):
            if file.endswith(old_extension):
                os.rename(os.path.join(directory, file),
                          os.path.join(directory, file.replace(old_extension, new_extension)))
                count += 1
        print(f'修改{count}个文件后缀成功')

    @staticmethod
    def move_files_to_empty_directory(directory, files_path_list):
        """
        将文件移动到指定目录，目录必须是空目录
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 判断目录里是否存在东西，文件或者子目录
        if os.listdir(directory):
            choice = input(
                f"目录{directory}不为空，继续可能导致未知问题，请考虑使用 add_files_to_directory 函数——继续运行将会清空该目录，是否继续？(y/n)")
            if choice.lower() == 'n':
                print("文件移动已取消")
                return False
        # 清空目录
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        file_name_used_dict = {}
        for file_path in files_path_list:
            # 移动,如果出现文件名重复，则在文件名后面加上数字
            file_name, ext = os.path.splitext(file_path)
            if not ext:
                raise Exception(f"存在文件没有后缀名，路径为：{file_path}")
            new_file_name = file_name
            if file_name in file_name_used_dict.keys():
                new_file_name = file_name + '_' + str(file_name_used_dict[file_name + ext]) + ext
                file_name_used_dict[file_name + ext] += 1
            else:
                file_name_used_dict[file_name + ext] = 1
            try:
                shutil.move(file_path, os.path.join(directory, new_file_name))
            except shutil.Error as e:
                print(f'移动文件{file_path}到{directory}失败,原因:{e}')
        return True

    @staticmethod
    def copy_files_to_empty_directory(directory, files_path_list):
        """
        将文件复制到指定目录，目录必须是空目录
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.listdir(directory):
            choice = input(
                f"目录{directory}不为空，继续可能导致未知问题，请考虑使用 add_files_to_directory 函数——继续运行将会清空该目录，是否继续？(y/n)")
            if choice.lower() == 'n':
                print("文件复制已取消")
                return False
            else:
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))
        file_name_used_dict = {}
        for file_path in files_path_list:
            # 复制并且重命名
            base_name = os.path.basename(file_path)
            file_name, ext = os.path.splitext(base_name)
            if not ext:
                raise Exception(f"存在文件没有后缀名，路径为：{file_path}")
            new_file_name = base_name
            if base_name in file_name_used_dict.keys():
                new_file_name = file_name + '_' + str(file_name_used_dict[base_name]) + ext
                file_name_used_dict[base_name] += 1
            else:
                file_name_used_dict[base_name] = 1
            try:
                shutil.copy(file_path, os.path.join(directory, new_file_name))
            except shutil.Error as e:
                print(f'复制文件{file_path}到{directory}失败,原因:{e}')
        return True

    @staticmethod
    def creat_directory(directory):
        """
        创建目录
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def creat_file(file_path):
        """
        创建文件
        """
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass

    @staticmethod
    def add_file_or_directories_to_directory_without_same_name(directory, file_or_directory_name_list):
        """
        这个函数用来将文件或目录添加到指定目录，如果存在同名文件或目录，则自动重命名后添加
        :param directory:
        :param file_or_directory_name_list:
        :return:
        """
        if isinstance(file_or_directory_name_list, str):
            file_or_directory_name_list = [file_or_directory_name_list]
        if not os.path.exists(directory):
            os.makedirs(directory)
        for file_or_directory_name in file_or_directory_name_list:
            new_file_or_directory_name = OSUtils.autochange_file_or_directory_name_while_exist(directory,
                                                                                               file_or_directory_name)
            # 创建文件或目录
            if os.path.isfile(file_or_directory_name):
                OSUtils.creat_file(os.path.join(directory, new_file_or_directory_name))
            else:
                OSUtils.creat_directory(os.path.join(directory, new_file_or_directory_name))

    @staticmethod
    def add_file_or_directories_to_directory_cancel_while_exist(directory, file_or_directory_name_list):
        """
        这个函数用来将文件或目录添加到指定目录，如果存在同名文件或目录，则不添加
        :param directory:
        :param file_or_directory_name_list:
        :return:
        """
        if isinstance(file_or_directory_name_list, str):
            file_or_directory_name_list = [file_or_directory_name_list]
        if not os.path.exists(directory):
            os.makedirs(directory)
        existed_file_or_directory_name_list = os.listdir(directory)
        for file_or_directory_name in file_or_directory_name_list:
            if file_or_directory_name in existed_file_or_directory_name_list:
                continue
            # 创建文件或目录
            if os.path.isfile(file_or_directory_name):
                OSUtils.creat_file(os.path.join(directory, file_or_directory_name))
            else:
                OSUtils.creat_directory(os.path.join(directory, file_or_directory_name))

    @staticmethod
    def add_files_to_directory_without_same_name(directory, files_path_list):
        """
        将文件添加到指定目录,每个文件检查是否存在于指定目录，如果存在，通过名字后缀数字变化重命名后添加到目录
        """
        if isinstance(files_path_list, str):
            files_path_list = [files_path_list]
        if not os.path.exists(directory):
            os.makedirs(directory)

        for file_path in files_path_list:
            new_file_path = OSUtils.autochange_file_name_while_exist(directory, file_path)
            # 将文件移动到新路径
            shutil.copy(file_path, new_file_path)

    @staticmethod
    def autochange_file_or_directory_name_while_exist(directory, file_or_directory_name):
        """
        这个函数用来检查指定文件或者目录是否存在于指定目录，如果存在，通过名字后缀数字变化重命名后返回新文件名或目录名
        :param directory:
        :param file_name:
        :return:
        """
        file_and_directory_name_used_list = os.listdir(directory)
        new_file_or_directory_name = file_or_directory_name
        # 检查文件名是否重复
        if file_or_directory_name in file_and_directory_name_used_list:
            pre = 1
            base_name, ext = os.path.splitext(file_or_directory_name)
            while new_file_or_directory_name in file_and_directory_name_used_list:
                new_file_or_directory_name = f"{base_name}_{pre}{ext}"
                pre += 1
        return new_file_or_directory_name

    @staticmethod
    def autochange_file_name_while_exist(directory, file_path):
        """
        这个函数用来检查指定文件是否存在于指定目录，如果存在，通过名字后缀数字变化重命名后返回新路径
        :param directory:
        :param file_path:
        :return:
        """
        file_name_used_list = os.listdir(directory)
        file_name = os.path.basename(file_path)
        new_file_name = file_name

        # 检查文件名是否重复
        if file_name in file_name_used_list:
            pre = 1
            base_name, ext = os.path.splitext(file_name)
            if not ext:
                raise Exception(f"存在文件没有后缀名，路径为：{file_path}")
            while new_file_name in file_name_used_list:
                new_file_name = f"{base_name}_{pre}{ext}"
                pre += 1

        return os.path.join(directory, new_file_name)

    @staticmethod
    def xls_in_directory_to_xlsx(directory):
        """
        将目录及其子目录下的所有xls文件转换为xlsx文件，主义，该方法使用pandas库，不会保留xls文件中的合并单元格
        """

        if not os.path.exists(directory):
            print("目录不存在")
            return
        file_path_used = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path_used.append(os.path.join(root, file))
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.xls'):
                    file_path = os.path.join(root, file)
                    df = pandas.read_excel(file_path, sheet_name=None, engine='xlrd')
                    new_file_path = file_path.replace('.xls', '.xlsx')
                    if new_file_path in file_path_used:
                        pre = 1
                        new_file_name, ext = os.path.splitext(new_file_path)
                        while new_file_path in file_path_used:
                            new_file_path = new_file_name + '_' + str(pre) + '.xlsx'
                            pre += 1
                    file_path_used.append(new_file_path)
                    with pandas.ExcelWriter(new_file_path, engine='openpyxl') as writer:
                        for sheet_name, data in df.items():
                            data.to_excel(writer, sheet_name=sheet_name, index=False)
                    os.remove(file_path)
            print("转换结束")

    @staticmethod
    def unzip_all_files_in_directory(directory, delete_zip=True):
        """
        这个函数用来解压指定目录下及其子目录的所有zip和rar和.7z文件
        """
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.zip') or file.endswith('.rar') or file.endswith('.7z'):
                    try:
                        shutil.unpack_archive(os.path.join(root, file), root)
                        if delete_zip:
                            os.remove(os.path.join(root, file))
                    except shutil.ReadError as e:
                        print(f'解压文件{file}失败,原因:{e}')

    @staticmethod
    def zip_all_files_in_directory(directory, delete_original=False):
        """
        这个函数用来压缩指定目录下及其子目录的所有文件
        """
        for root, dirs, files in os.walk(directory):
            for file in files:
                if not file.endswith('.zip') and not file.endswith('.rar') and not file.endswith('.7z'):
                    try:
                        shutil.make_archive(os.path.join(root, file), 'zip', root, file)
                        if delete_original:
                            os.remove(os.path.join(root, file))
                    except shutil.ReadError as e:
                        print(f'压缩文件{file}失败,原因:{e}')

    @staticmethod
    def delete_single_file(file_path):
        """
        这个函数用来删除单个文件
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'文件{file_path}删除成功')
        else:
            print(f'文件{file_path}不存在')

    @staticmethod
    def get_path_from_explorer(folder=False):
        """
        这个函数用来从资源管理器中选择文件或者文件夹，返回路径
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        if folder:
            file_path = filedialog.askdirectory()
        else:
            file_path = filedialog.askopenfilename()

        if file_path:
            return file_path

        return None

    @staticmethod
    def get_all_subdirectory_in_directory(directory_path):
        """
        这个函数用来获取指定目录下所有子目录(不只是一级子目录)的绝对路径，返回(路径列表, 数量, 名称列表)
        """
        sub_directories = []
        sub_directories_name = []
        for root, dirs, files in os.walk(directory_path):
            for dir in dirs:
                sub_directories.append(os.path.join(root, dir))
                sub_directories_name.append(dir)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def get_all_subdirectory_in_single_directory(directory_path):
        """
        这个函数用来获取指定目录下所有一级子目录的绝对路径，(路径列表, 名称列表, 数量)
        """
        sub_directories = []
        sub_directories_name = []
        for file in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, file)):
                sub_directories.append(os.path.join(directory_path, file))
                sub_directories_name.append(file)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def get_all_subdirectory_in_directory_name_include_string(directory_path, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的子目录的绝对路径，返回(路径列表, 数量, 名称列表)
        """
        sub_directories = []
        sub_directories_name = []
        for root, dirs, files in os.walk(directory_path):
            for dir in dirs:
                if string in dir:
                    sub_directories.append(os.path.join(root, dir))
                    sub_directories_name.append(dir)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def get_all_subdirectory_in_single_directory_name_include_string(directory_path, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的子目录的名称，返回(路径列表, 数量, 名称列表)
        :param directory_path:
        :param string:
        :return:
        """
        sub_directories = []
        sub_directories_name = []
        for file in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, file)) and string in file:
                sub_directories.append(os.path.join(directory_path, file))
                sub_directories_name.append(file)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def get_all_subdirectory_in_directory_name_include_string_discontinuous(directory_path, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的子目录的绝对路径，可以是不连续的，返回(路径列表, 数量, 名称列表)
        :param directory_path:
        :param string:
        :return:
        """
        sub_directories = []
        sub_directories_name = []
        for root, dirs, files in os.walk(directory_path):
            for dir in dirs:
                if StringUtils.b_is_substring_of_a(dir, string):
                    sub_directories.append(os.path.join(root, dir))
                    sub_directories_name.append(dir)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def get_all_subdirectory_in_single_directory_name_include_string_discontinuous(directory_path, string):
        """
        这个函数用来获取指定目录下所有包含指定字符串的子目录的名称，可以是不连续的，返回(路径列表, 数量, 名称列表)
        :param directory_path:
        :param string:
        :return:
        """
        sub_directories = []
        sub_directories_name = []
        for file in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, file)) and StringUtils.b_is_substring_of_a(file, string):
                sub_directories.append(os.path.join(directory_path, file))
                sub_directories_name.append(file)
        return sub_directories, sub_directories_name, len(sub_directories)

    @staticmethod
    def open_file(file_path):
        """
        这个函数用来打开指定文件
        """
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f'文件{file_path}不存在')

    @staticmethod
    def extract_all_files_to_directory(directory_path, extract_directory_path, overwrite=False):
        """
        把一个文件夹里面的所有文件（包括子文件夹里面的文件）都提取到顶层文件夹里面，如果是不覆盖模式，则跳过已经存在的文件
        """
        if not os.path.exists(extract_directory_path):
            os.makedirs(extract_directory_path)
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                extract_file_path = os.path.join(extract_directory_path, file)
                if not os.path.exists(extract_file_path) or overwrite:
                    shutil.copy(file_path, extract_directory_path)


if __name__ == '__main__':
    # # OSUtils.open_file(r'D:/nonamekill\Noname-win32-x64\无名杀.exe')
    # print(OSUtils.generate_unique_file_names_by_uuid('.jpg', 2))
    # print(OSUtils.generate_unique_file_names(file_name_extension='.jpg', length=40, num=2))

    folders, _, _ = OSUtils.get_all_directories_in_single_directory(OSUtils.get_path_from_explorer(folder=True))
    print(folders)
    for folder in folders:
        OSUtils.add_file_or_directories_to_directory_cancel_while_exist(folder, ['SD1.5', 'SDXL', 'FLUX1', 'SD2'])
