import os
import re
import random
import numpy as np
from PIL import Image
from shutil import copy


class DataHandler:
    """
    处理总数据集（分好类的数据集）
    """

    @staticmethod
    def _mkdir(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @staticmethod
    def _gain_partitions_dir_name(data_dir):
        return [class_dir for class_dir in os.listdir(data_dir)]

    @staticmethod
    def create_train_test_dir(data_dir: str, split_rate: float, copy_flag: bool = False) -> None:
        """
        将总数据集划分为训练集和测试集，并复制到data/train和data/test目录下。
        :param data_dir:总数据集路径
        :param split_rate:分给测试集的比例，0-1之间
        :param copy_flag:是否需要重头划分并复制数据集，默认为False（不划分），此时会检查data目录是否存在，如果存在则不进行重新划分，如果不存在则进行划分并复制
        :return:
        """
        if os.path.exists(r'./data') and not copy_flag:
            return
        DataHandler._mkdir(r'./data/train')
        DataHandler._mkdir(r'./data/test')
        # print(DataHandler._gain_partitions_dir_name(data_dir))
        # return
        for class_dir in DataHandler._gain_partitions_dir_name(data_dir):
            DataHandler._mkdir(r'./data/train/' + class_dir)
            DataHandler._mkdir(r'./data/test/' + class_dir)
        for class_dir in DataHandler._gain_partitions_dir_name(data_dir):
            class_dir_path = os.path.join(data_dir, class_dir)
            files = os.listdir(class_dir_path)
            files_num = len(files)
            test_files = random.sample(files, int(files_num * split_rate))
            for index, file in enumerate(files):
                file_path = os.path.join(class_dir_path, file)
                if file in test_files:
                    new_file_path = os.path.join(r'./data/test/' + class_dir, file)
                else:
                    new_file_path = os.path.join(r'./data/train/' + class_dir, file)
                copy(file_path, new_file_path)
                print('\r[{}] processing [{}/{}]'.format(class_dir, index + 1, files_num), end="")
            print()
            print('*****************[{}] finished!*****************'.format(class_dir))
        print('\n****************All partitions finished!****************')

    @staticmethod
    def mean_std_normalize_images(data_dir: str, save_path: str = './mean_std.txt', read_by_txt: bool = True,
                                  debug_channel: bool = False):
        if read_by_txt and os.path.exists('./mean_std.txt'):
            with open('./mean_std.txt', 'r') as file:
                data = file.read()

            # 使用正则表达式找到均值和标准差列表的部分
            mean_match = re.search(r'mean: \[(.*?)\]', data)
            std_match = re.search(r'std: \[(.*?)\]', data)

            if mean_match and std_match:
                # 从正则表达式匹配中提取均值和标准差列表的部分
                mean_str = mean_match.group(1)
                std_str = std_match.group(1)

                # 将字符串转换为浮点数列表
                mean = [float(num) for num in mean_str.split(',')]
                std = [float(num) for num in std_str.split(',')]
                print('读取mean_std.txt文件成功！')
                print('mean:', mean)
                print('std:', std)
                # 返回均值和标准差列表
                return mean, std
            else:
                pass
        print('****************开始计算mean和std******************')
        total_pixels = 0
        sum_normalized_pixels = np.zeros(3)
        sum_squared_diff = np.zeros(3)

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG', 'bmp', 'BMP')):
                    file_path = os.path.join(root, file)
                    try:
                        img = Image.open(file_path)
                        img_array = np.array(img)
                        if img_array.ndim == 3 and img_array.shape[2] in [3, 4]:  # 只处理3或4通道的图像
                            if img_array.shape[2] == 4:
                                img_array = img_array[:, :, :3]  # 去掉透明通道
                            # print(f'正在处理图像{file_path}')
                            normalized_img_array = img_array / 255.0
                            total_pixels += normalized_img_array.size // 3
                            sum_normalized_pixels += np.sum(normalized_img_array, axis=(0, 1))
                    except Exception as e:
                        if debug_channel:
                            print(f'捕捉到图像{file_path}异常: {e}')
        mean = sum_normalized_pixels / total_pixels

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG', 'bmp', 'BMP')):
                    file_path = os.path.join(root, file)
                    try:
                        img = Image.open(file_path)
                        img_array = np.array(img)
                        if img_array.ndim == 3 and img_array.shape[2] in [3, 4]:
                            if img_array.shape[2] == 4:
                                img_array = img_array[:, :, :3]  # 去掉透明通道
                            normalized_img_array = (img_array / 255.0) - mean
                            sum_squared_diff += np.sum(np.square(normalized_img_array), axis=(0, 1))
                    except Exception as e:
                        if debug_channel:
                            print(f'捕捉到图像{file_path}异常: {e}')

        std = np.sqrt(sum_squared_diff / total_pixels)
        print('mean:', list(mean))
        print('std:', list(std))
        # 把mean和std保存到文件中
        with open('./mean_std.txt', 'w') as f:
            f.write(f'mean: {list(mean)}\n')
            f.write(f'std: {list(std)}\n')
        print('****************计算mean和std完成！******************')
        return list(mean), list(std)
