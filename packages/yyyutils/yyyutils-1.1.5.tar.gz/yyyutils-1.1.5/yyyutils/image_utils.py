"""
用于处理图像的工具类
"""
import cv2
import numpy as np
import os
import random
import string
import shutil
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class MatchResult:
    x: int
    y: int
    similarity: float


class ImageUtils:
    """
    用于处理图像的静态工具类
    """

    @staticmethod
    def read_image(file_path):
        """
        读取图像
        :param file_path: 图像文件路径
        :return: 图像对象
        """
        image = cv2.imread(file_path)
        return image

    @staticmethod
    def save_image(image_array, file_path):
        cv2.imwrite(file_path, image_array)

    @staticmethod
    def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        调整图像大小
        :param image: 输入图像
        :param width: 输出图像宽度
        :param height: 输出图像高度
        :param inter: 缩放插值方法
        :return: 调整后的图像
        """
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    @staticmethod
    def rotate_image(image, angle, center=None, scale=1.0):
        """
        旋转图像
        :param image: 输入图像
        :param angle: 旋转角度
        :param center: 旋转中心
        :param scale: 缩放比例
        :return: 旋转后的图像
        """
        (h, w) = image.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))
        return rotated

    @staticmethod
    def crop_image(image, x, y, w, h):
        """
        裁剪图像
        :param image: 输入图像
        :param x: 裁剪区域左上角x坐标
        :param y: 裁剪区域左上角y坐标
        :param w: 裁剪区域宽度
        :param h: 裁剪区域高度
        :return: 裁剪后的图像
        """
        cropped = image[y:y + h, x:x + w]
        return cropped

    @staticmethod
    def flip_image(image, flip_code):
        """
        翻转图像
        :param image: 输入图像
        :param flip_code: 翻转方向
        :return: 翻转后的图像
        """
        flipped = cv2.flip(image, flip_code)
        return flipped

    @staticmethod
    def add_padding(image, top, bottom, left, right, color=(0, 0, 0)):
        """
        添加边缘填充
        :param image: 输入图像
        :param top: 上边缘填充长度
        :param bottom: 下边缘填充长度
        :param left: 左边缘填充长度
        :param right: 右边缘填充长度
        :param color: 填充颜色
        :return: 填充后的图像
        """
        padded = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return padded

    @staticmethod
    def add_noise(image, mean=0, std=10):
        """
        添加噪声
        :param image: 输入图像
        :param mean: 均值
        :param std: 标准差
        :return: 加噪声后的图像
        """
        noisy = image.astype(np.int16) + np.random.normal(mean, std, image.shape)
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        return noisy

    @staticmethod
    def add_salt_pepper_noise(image, amount=0.05):
        """
        添加椒盐噪声
        :param image: 输入图像
        :param amount: 噪声比例
        :return: 加噪声后的图像
        """
        output = image.copy()
        h, w = image.shape[:2]
        num_salt = np.ceil(amount * h * w * 0.5)
        num_pepper = np.ceil(amount * h * w * 0.5)
        for i in range(num_salt):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            output[y, x] = 255
        for i in range(num_pepper):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            output[y, x] = 0
        return output

    @staticmethod
    def add_gaussian_noise(image, mean=0, var=0.01):
        """
        添加高斯噪声
        :param image: 输入图像
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        noisy = image + noise
        return noisy

    @staticmethod
    def add_speckle_noise(image, mean=0, var=0.01):
        """
        添加斑点噪声
        :param image: 输入图像
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = image.copy()
        h, w = image.shape[:2]
        noise = np.random.normal(mean, var ** 0.5, (h, w))
        noisy = image + image * noise
        return noisy

    @staticmethod
    def add_poisson_noise(image, mean=0):
        """
        添加泊松噪声
        :param image: 输入图像
        :param mean: 均值
        :return: 加噪声后的图像
        """
        noisy = np.random.poisson(image * mean) / mean
        return noisy

    @staticmethod
    def add_speckle_noise_with_mask(image, mask, mean=0, var=0.01):
        """
        添加斑点噪声
        :param image: 输入图像
        :param mask: 噪声掩码
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        noisy = image + image * noise * mask
        return noisy

    @staticmethod
    def add_gaussian_blur(image, ksize=5):
        """
        添加高斯模糊
        :param image: 输入图像
        :param ksize: 高斯核大小
        :return: 加模糊后的图像
        """
        blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
        return blurred

    @staticmethod
    def add_median_blur(image, ksize=5):
        """
        添加中值模糊
        :param image: 输入图像
        :param ksize: 中值核大小
        :return: 加模糊后的图像
        """
        blurred = cv2.medianBlur(image, ksize)
        return blurred

    @staticmethod
    def add_bilateral_blur(image, d=9, sigmaColor=75, sigmaSpace=75):
        """
        添加双边模糊
        :param image: 输入图像
        :param d: 领域大小
        :param sigmaColor: 颜色空间标准差
        :param sigmaSpace: 坐标空间标准差
        :return: 加模糊后的图像
        """
        blurred = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
        return blurred

    @staticmethod
    def add_gamma_correction(image, gamma=1.0):
        """
        添加伽马校正
        :param image: 输入图像
        :param gamma: 伽马值
        :return: 加校正后的图像
        """
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        gamma_corrected = cv2.LUT(image, table)
        return gamma_corrected

    @staticmethod
    def add_clahe(image, clipLimit=2.0, tileGridSize=(8, 8)):
        """
        添加CLAHE
        :param image: 输入图像
        :param clipLimit: 裁剪限值
        :param tileGridSize: 块大小
        :return: 加CLAHE后的图像
        """
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        cl1 = clahe.apply(image)
        return cl1

    @staticmethod
    def add_histogram_equalization(image):
        """
        添加直方图均衡化
        :param image: 输入图像
        :return: 加均衡化后的图像
        """
        equalized = cv2.equalizeHist(image)
        return equalized

    @staticmethod
    def add_adaptive_equalization(image, kernel_size=3):
        """
        添加自适应均衡化
        :param image: 输入图像
        :param kernel_size: 卷积核大小
        :return: 加均衡化后的图像
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(image)
        adapteq = cv2.adaptiveThreshold(cl1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, kernel_size, 2)
        return adapteq

    @staticmethod
    def add_image(image1, image2, alpha=0.5):
        """
        叠加图像
        :param image1: 输入图像1
        :param image2: 输入图像2
        :param alpha: 透明度
        :return: 叠加后的图像
        """
        if image1.shape != image2.shape:
            raise ValueError("Image shapes must match")
        blended = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
        return blended

    @staticmethod
    def subtract_image(image1, image2):
        """
        减去图像
        :param image1: 输入图像1
        :param image2: 输入图像2
        :return: 减去后的图像
        """
        if image1.shape != image2.shape:
            raise ValueError("Image shapes must match")
        subtracted = cv2.subtract(image1, image2)
        return subtracted

    @staticmethod
    # 二值化图像
    def binarize_image(image, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
        """
        二值化图像
        :param image: 输入图像
        :param threshold: 阈值
        :param max_value: 最大值
        :param type: 阈值类型
        :return: 二值化后的图像
        """
        ret, binary = cv2.threshold(image, threshold, max_value, type)
        return binary

    @staticmethod
    # 反二值化图像
    def inverse_binarize_image(image, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
        """
        反二值化图像
        :param image: 输入图像
        :param threshold: 阈值
        :param max_value: 最大值
        :param type: 阈值类型
        :return: 反二值化后的图像
        """
        ret, binary = cv2.threshold(image, threshold, max_value, type)
        inverse_binary = cv2.bitwise_not(binary)
        return inverse_binary

    @staticmethod
    # 图像形态学操作
    def morphology_operation(image, operation, kernel):
        """
        图像形态学操作
        :param image: 输入图像
        :param operation: 操作类型
        :param kernel: 卷积核
        :return: 操作后的图像
        """
        if operation == "erosion":
            result = cv2.erode(image, kernel)
        elif operation == "dilation":
            result = cv2.dilate(image, kernel)
        elif operation == "opening":
            result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == "closing":
            result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        elif operation == "gradient":
            result = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
        elif operation == "top_hat":
            result = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
        elif operation == "black_hat":
            result = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        else:
            raise ValueError("Invalid operation")
        return result

    @staticmethod
    # 图像梯度
    def gradient(image):
        """
        图像梯度
        :param image: 输入图像
        :return: 梯度图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

    @staticmethod
    # 图像梯度方向
    def gradient_direction(image):
        """
        图像梯度方向
        :param image: 输入图像
        :return: 梯度方向图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1)
        grad_dir = cv2.phase(grad_x, grad_y, angleInDegrees=True)
        return grad_dir

    @staticmethod
    def clear_noise(image, kernel_size=1):
        """
        清除噪声
        :param image: 输入图像
        :param kernel_size: 卷积核大小，必须为奇数
        :return: 清除噪声后的图像
        """
        # 确保卷积核大小为奇数
        if kernel_size % 2 == 0:
            kernel_size += 1

        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ImageUtils.show_image(gray, "Gray Image")

        # 高斯滤波
        blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        ImageUtils.show_image(blur, "Blur Image")

        # 二值化
        ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)
        ImageUtils.show_image(binary, "Binary Image")

        # 膨胀
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilation = cv2.dilate(binary, kernel)
        ImageUtils.show_image(dilation, "Dilation Image")

        # 腐蚀
        erosion = cv2.erode(dilation, kernel)
        ImageUtils.show_image(erosion, "Erosion Image")

        # 再次膨胀
        dilation2 = cv2.dilate(erosion, kernel)
        ImageUtils.show_image(dilation2, "Dilation2 Image")

        return dilation2

    @staticmethod
    def show_image(image_array, window_name="Image"):
        """
        最大化显示图像，可以放大缩小的那种
        :param image_array: 输入图像
        :param window_name: 窗口名称
        :return: None
        """
        cv2.namedWindow(window_name, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, image_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def locate_object(image: np.ndarray, icon_img: np.ndarray, x_start_ratio: float = 0, y_start_ratio: float = 0,
                      x_end_ratio: float = 1, y_end_ratio: float = 1, try_times: int = 3,
                      similarity_threshold: float = 0.8, multi_scale: bool = False,
                      ignore_color: bool = False, binarize: bool = False, edge_only: bool = False) -> Optional[
        MatchResult]:
        print()

        def preprocess_images(source, template, binarize, ignore_color, edge_only):
            if binarize:
                _, source = cv2.threshold(source, 127, 127, cv2.THRESH_BINARY)
                _, template = cv2.threshold(template, 127, 127, cv2.THRESH_BINARY)

            if ignore_color or edge_only:
                source = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            if edge_only:
                source = cv2.Canny(source, 100, 200)
                template = cv2.Canny(template, 100, 200)
                # if debug_img_transform:
                #     cv2.imwrite(os.path.join(temp_dir, "edge.png"), source)
                #     cv2.imwrite(os.path.join(temp_dir, "edge_template.png"), template)

            return source, template

        if not all(0 <= r <= 1 for r in [x_start_ratio, y_start_ratio, x_end_ratio, y_end_ratio]):
            raise ValueError("比例参数必须在0到1之间")

        def multi_scale_template_matching(source, template):
            best_result = None
            for scale in np.linspace(0.5, 2.0, 20):
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                if resized_template.shape[0] > source.shape[0] or resized_template.shape[1] > source.shape[1]:
                    continue
                result = cv2.matchTemplate(source, resized_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if best_result is None or max_val > best_result[0]:
                    best_result = (max_val, max_loc, resized_template.shape)
            return best_result

        for i in range(try_times):
            try:
                h, w = image.shape[:2]
                x_start, y_start = int(w * x_start_ratio), int(h * y_start_ratio)
                x_end, y_end = int(w * x_end_ratio), int(h * y_end_ratio)
                image = image[y_start:y_end, x_start:x_end]
                template = icon_img

                image, template = preprocess_images(image, template, binarize, ignore_color, edge_only)

                if multi_scale:
                    best_result = multi_scale_template_matching(image, template)
                    if best_result is None:
                        print(f'在多尺度搜索下未找到匹配，尝试 {i + 1}/{try_times}')
                        continue
                    max_val, max_loc, template_shape = best_result
                    similarity_threshold = similarity_threshold
                else:
                    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    template_shape = template.shape

                if max_val > similarity_threshold:
                    result_x, result_y = max_loc
                    result_x += x_start
                    result_y += y_start
                    return MatchResult(result_x, result_y, max_val)
                else:
                    print(f'低相似度：{max_val:.2f}，尝试 {i + 1}/{try_times}')
            except Exception as e:
                print(f"在第 {i + 1} 次尝试中发生错误: {str(e)}")

        print(f"在 {try_times} 次尝试后未找到匹配")
        return None

    @staticmethod
    def split_image_by_y(image, split_y: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        在指定的y坐标位置将图像分割成上下两部分

        Args:
            image: 要分割的图像
            split_y: 分割线的y坐标

        Returns:
            tuple: (upper_part, lower_part) 分割后的上下两部分图像
        """
        if split_y < 0 or split_y > image.shape[0]:
            raise ValueError(f"分割位置 {split_y} 超出图像范围 [0, {image.shape[0]}]")

        upper_part = image[0:split_y, :]
        lower_part = image[split_y:, :]

        return upper_part, lower_part

    @staticmethod
    def split_image_by_x(image, split_x: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        在指定的x坐标位置将图像分割成左右两部分

        Args:
            image: 要分割的图像
            split_x: 分割线的x坐标

        Returns:
            tuple: (left_part, right_part) 分割后的左右两部分图像
        """
        if split_x < 0 or split_x > image.shape[1]:
            raise ValueError(f"分割位置 {split_x} 超出图像范围 [0, {image.shape[1]}]")

        left_part = image[:, 0:split_x]
        right_part = image[:, split_x:]

        return left_part, right_part

    @staticmethod
    def locate_and_split(image, icon_img, x_start_ratio: float = 0, y_start_ratio: float = 0,
                         x_end_ratio: float = 1, y_end_ratio: float = 1, try_times: int = 3,
                         similarity_threshold: float = 0.8, multi_scale: bool = False,
                         ignore_color: bool = False, binarize: bool = False, edge_only: bool = False) -> Tuple[
        Optional[MatchResult], Optional[Tuple[np.ndarray, np.ndarray]]]:
        """
        定位目标图像并进行分割

        Returns:
            tuple: (MatchResult, (upper_part, lower_part))
                   如果未找到匹配，返回 (None, None)
        """
        # 首先调用locate_object方法找到匹配位置
        match_result = ImageUtils.locate_object(image, icon_img, x_start_ratio, y_start_ratio,
                                                x_end_ratio, y_end_ratio, try_times, similarity_threshold,
                                                multi_scale, ignore_color, binarize, edge_only)

        if match_result is None:
            return None, None

        # 调用split_image方法进行图像分割
        try:
            split_result = ImageUtils.split_image_by_y(image, match_result.y)
            return match_result, split_result
        except ValueError as e:
            print(f"分割图像时出错: {str(e)}")
            return match_result, None


if __name__ == '__main__':
    # image = ImageUtils.read_image(
    #     r"D:\QQDownloads\Data\Tencent Files\1992541488\nt_qq\nt_data\Pic\2024-11\Ori\03fe0390ef1647de044dea5a0f8bbcd5.jpg")
    # ImageUtils.show_image(image)
    # ImageUtils.clear_noise(image)
    image = cv2.imread(r'D:\PycharmProjectsPrefession\proj_git\Function\fzdxtk\temp_page_0.png')
    icon = cv2.imread(r'D:\PycharmProjectsPrefession\proj_git\Function\fzdxtk\icon.jpg')
    print(image.shape)
    match_result, split_result = ImageUtils.locate_and_split(image, icon)
    print(match_result)
    ImageUtils.save_image(match_result, 'match_result.png')
    # 显示分割结果
    if split_result is not None:
        ImageUtils.show_image(split_result[0], "upper_part")
        ImageUtils.show_image(split_result[1], "lower_part")
    else:
        print("未找到匹配")
