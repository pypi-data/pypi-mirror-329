import os
import time
import cv2 as cv
import pywinauto.mouse
from PIL import ImageGrab
from loguru import logger
import shutil
import keyboard
from yyyutils.window_utils import WindowUtils
from dataclasses import dataclass
from typing import Optional, List, Tuple
import numpy as np
import win32gui


@dataclass
class MatchResult:
    x: int
    y: int
    similarity: float


class AutoClickByImageUtils:
    def __init__(self, window_name: Optional[str] = None, icon_dir: str = r"..\image", temp_dir: str = r"..\temp",
                 fail_img_dir: str = r"..\fail_img", debug_img_transform: bool = False, save_fail_screen: bool = False):
        self.window_name = window_name or "Desktop"
        self.handle = win32gui.GetDesktopWindow() if self.window_name == "Desktop" else WindowUtils.get_window_handle(
            self.window_name)
        self.temp_dir = temp_dir
        self.icon_dir = icon_dir
        self.fail_img_dir = fail_img_dir
        self.debug_img_transform = debug_img_transform
        self.save_fail_screen = save_fail_screen
        self.app_screen_path = os.path.join(self.temp_dir, "app.png")
        self.work_screen_path = os.path.join(self.temp_dir, "work_screen.png")

        self.create_directories()
        self.image_cache = {}
        self.clear_fail_img()

        if self.window_name != "Desktop":
            WindowUtils.show_window(self.handle)
            WindowUtils.set_window_topmost(self.handle)

        self.original_position = WindowUtils.get_window_rect(self.handle)

    def create_directories(self):
        for dir_path in [self.temp_dir, self.fail_img_dir]:
            os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self.icon_dir):
            raise FileNotFoundError(f"icon目录 {self.icon_dir} 不存在")

    def get_app_screenshot(self) -> Tuple[int, int, int, int]:
        try:
            img_ready = ImageGrab.grab(self.original_position if self.window_name != "Desktop" else None)
            img_ready.save(self.app_screen_path)
            return self.original_position
        except Exception as e:
            logger.error(f"获取应用截图失败: {str(e)}")
            raise

    def get_workscreen_screenshot(self):
        try:
            screen_shot = ImageGrab.grab()
            if screen_shot:
                screen_shot.save(self.work_screen_path)
            return screen_shot
        except Exception as e:
            logger.error(f"获取工作屏幕截图失败: {str(e)}")
            return None

    @staticmethod
    def click_icon(xy: Tuple[int, int], xy_offset: Tuple[int, int] = (0, 0)):
        try:
            x, y = xy[0] + xy_offset[0], xy[1] + xy_offset[1]
            pywinauto.mouse.click(button='left', coords=(x, y))
            logger.info(f"成功点击坐标：({x}, {y})")
        except Exception as e:
            logger.error(f"点击坐标 {xy} 失败：{str(e)}")

    def _locate_icon(self, img_name: str, x_start_ratio: float = 0, y_start_ratio: float = 0,
                     x_end_ratio: float = 1, y_end_ratio: float = 1, try_times: int = 3,
                     similarity_threshold: float = 0.8, multi_scale: bool = False,
                     ignore_color: bool = False, binarize: bool = False, edge_only: bool = False) -> Optional[
        MatchResult]:
        obj_path = os.path.join(self.icon_dir, img_name)

        if not all(0 <= r <= 1 for r in [x_start_ratio, y_start_ratio, x_end_ratio, y_end_ratio]):
            raise ValueError("比例参数必须在0到1之间")

        for i in range(try_times):
            try:
                x_init, y_init = self.get_app_screenshot()[:2]
                source = cv.imread(self.app_screen_path)
                if source is None:
                    raise FileNotFoundError(f"无法读取截图：{self.app_screen_path}")

                h, w = source.shape[:2]
                x_start, y_start = int(w * x_start_ratio), int(h * y_start_ratio)
                x_end, y_end = int(w * x_end_ratio), int(h * y_end_ratio)
                source = source[y_start:y_end, x_start:x_end]

                template = self.image_cache.get(img_name)
                if template is None:
                    template = cv.imread(obj_path)
                    if template is None:
                        raise FileNotFoundError(f"无法读取目标图像：{obj_path}")
                    self.image_cache[img_name] = template

                source, template = self.preprocess_images(source, template, binarize, ignore_color, edge_only)

                if multi_scale:
                    best_result = self.multi_scale_template_matching(source, template)
                    if best_result is None:
                        logger.info(f'图标{img_name}--在多尺度搜索下未找到匹配，尝试 {i + 1}/{try_times}')
                        if self.save_fail_screen:
                            self.save_fail_img(source, img_name, i)
                        continue
                    max_val, max_loc, template_shape = best_result
                    similarity_threshold = 0.75
                else:
                    result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                    template_shape = template.shape

                if max_val > similarity_threshold:
                    result_x = x_init + x_start + max_loc[0] + template_shape[1] // 2
                    result_y = y_init + y_start + max_loc[1] + template_shape[0] // 2
                    return MatchResult(result_x, result_y, max_val)
                else:
                    logger.info(f'图标{img_name}--低相似度：{max_val:.2f}，尝试 {i + 1}/{try_times}')
                    if self.save_fail_screen:
                        self.save_fail_img(source, img_name, i, max_val)
            except Exception as e:
                logger.error(f"图标{img_name}--在第 {i + 1} 次尝试中发生错误: {str(e)}")

        logger.warning(f"图标{img_name}--在 {try_times} 次尝试后未找到匹配")
        return None

    def preprocess_images(self, source, template, binarize, ignore_color, edge_only):
        if binarize:
            _, source = cv.threshold(source, 127, 127, cv.THRESH_BINARY)
            _, template = cv.threshold(template, 127, 127, cv.THRESH_BINARY)
            if self.debug_img_transform:
                cv.imwrite(os.path.join(self.temp_dir, "binarize.png"), source)
                cv.imwrite(os.path.join(self.temp_dir, "binarize_template.png"), template)

        if ignore_color or edge_only:
            source = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
            template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
            if self.debug_img_transform:
                cv.imwrite(os.path.join(self.temp_dir, "gray.png"), source)
                cv.imwrite(os.path.join(self.temp_dir, "gray_template.png"), template)

        if edge_only:
            source = cv.Canny(source, 100, 200)
            template = cv.Canny(template, 100, 200)
            if self.debug_img_transform:
                cv.imwrite(os.path.join(self.temp_dir, "edge.png"), source)
                cv.imwrite(os.path.join(self.temp_dir, "edge_template.png"), template)

        return source, template

    def multi_scale_template_matching(self, source, template):
        best_result = None
        for scale in np.linspace(0.5, 2.0, 20):
            resized_template = cv.resize(template, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA)
            if resized_template.shape[0] > source.shape[0] or resized_template.shape[1] > source.shape[1]:
                continue
            result = cv.matchTemplate(source, resized_template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if best_result is None or max_val > best_result[0]:
                best_result = (max_val, max_loc, resized_template.shape)
        return best_result

    def save_fail_img(self, source, img_name, attempt, similarity=None):
        filename = f'icon{img_name.split(".")[0]}_{attempt + 1}'
        if similarity:
            filename += f'_{int(similarity * 100)}%'
        filename += '.png'
        path = os.path.join(self.fail_img_dir, filename)
        cv.imwrite(path, source)

    def clear_fail_img(self):
        try:
            shutil.rmtree(self.fail_img_dir)
            os.makedirs(self.fail_img_dir)
            logger.info("已清空失败图片目录")
        except Exception as e:
            logger.error(f"清空失败图片目录失败：{str(e)}")

    def check_icon(self, img_name: str, x_start_ratio: float = 0, y_start_ratio: float = 0,
                   x_end_ratio: float = 1, y_end_ratio: float = 1, multi_scale: bool = False,
                   ignore_color: bool = False, binarize: bool = False, edge_only: bool = False,
                   similarity_threshold: float = 0.8) -> Tuple[bool, int, int]:
        try:
            res = self._locate_icon(img_name, x_start_ratio, y_start_ratio, x_end_ratio, y_end_ratio,
                                    similarity_threshold=similarity_threshold, multi_scale=multi_scale,
                                    ignore_color=ignore_color, binarize=binarize, edge_only=edge_only)
            return (True, res.x, res.y) if res else (False, -1, -1)
        except Exception as e:
            logger.error(f"检查图标 {img_name} 失败：{str(e)}")
            return False, -1, -1

    def _move_files(self, origin_folder: str, target_folder: str, suffix_list: List[str] = []) -> int:
        try:
            data_list = [file for file in os.listdir(origin_folder)
                         if not suffix_list or any(file.endswith(suffix) for suffix in suffix_list)]

            if not data_list:
                logger.info("没有找到符合条件的文件")
                return 0

            cur_time = time.strftime("%Y-%m-%d_%H-%M-%S")
            target_folder_new = os.path.join(target_folder, cur_time)
            os.makedirs(target_folder_new, exist_ok=True)

            moved_count = 0
            for file_name in data_list:
                source_file = os.path.join(origin_folder, file_name)
                target_file = os.path.join(target_folder_new, file_name)
                shutil.move(source_file, target_file)
                logger.info(f"已移动文件: {file_name}")
                moved_count += 1

            logger.info(f"成功移动 {moved_count} 个文件到 {target_folder_new}")
            return moved_count
        except Exception as e:
            logger.error(f"移动文件时发生错误: {str(e)}")
            raise

    def running_program(self, origin_folder: str, target_folder: str, suffix_list: List[str] = [], cycle_num: int = -1):
        exit_flag = False

        def on_key_event(event):
            nonlocal exit_flag
            if event.name.upper() == 'Q':
                logger.info('退出程序')
                exit_flag = True

        keyboard.on_press(on_key_event)
        logger.info('开始运行程序')
        cycle_count = 0
        while not exit_flag:
            try:
                if self.is_test_over():
                    self._move_files(origin_folder, target_folder, suffix_list)
                    logger.info(f"完成第 {cycle_count} 个周期")
                    if cycle_num != -1 and cycle_count >= cycle_num:
                        logger.info(f"已完成 {cycle_count} 个周期，程序结束")
                        return
                    cycle_count += 1
            except Exception as e:
                logger.error(f"运行过程中发生错误: {str(e)}")
            time.sleep(1)

    def clear_icon_dir(self):
        try:
            shutil.rmtree(self.icon_dir)
            os.makedirs(self.icon_dir)
            logger.info("已清空图标目录")
        except Exception as e:
            logger.error(f"清空图标目录失败：{str(e)}")

    def save_click_icon(self, folder_path: str = None, size: Tuple[int, int] = (100, 100),
                        clear_icon_dir: bool = False, use_screenshot: bool = False):
        """
        保存以鼠标点击的位置为中心的图标，按下esc键退出保存
        :param folder_path: 保存图标的文件夹路径
        :param size: 图标大小，以鼠标点击的位置为中心，传入宽高
        :param clear_icon_dir: 是否清空图标目录
        :param use_screenshot: 是否使用截图进行点击
        :return:
        """
        finish_flag = False
        grab_flag = False
        icon_dir = folder_path or self.icon_dir
        if not os.path.exists(icon_dir):
            os.makedirs(icon_dir)

        def func():
            nonlocal finish_flag
            finish_flag = True

        def grab_func():
            nonlocal grab_flag
            grab_flag = True

        if clear_icon_dir:
            try:
                shutil.rmtree(icon_dir)
                os.makedirs(icon_dir)
                logger.info("已清空图标目录")
            except Exception as e:
                logger.error(f"清空图标目录失败：{str(e)}")

        from yyyutils.auto_utils.moniter.moniter_keyboard_utils import MoniterKeyboardUtils
        from yyyutils.auto_utils.mouse_utils import MouseUtils
        from yyyutils.window_utils import WindowUtils

        screenshot = None

        def show_image(screenshot):
            from PIL import ImageTk
            import tkinter as tk

            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry(f"{screenshot.width}x{screenshot.height}+0+0")
            root.attributes('-topmost', True)

            img = ImageTk.PhotoImage(screenshot)
            panel = tk.Label(root, image=img)
            panel.pack(side="bottom", fill="both", expand="yes")

            def close_window(event):
                root.destroy()

            root.bind('<Escape>', close_window)
            root.mainloop()

        import threading
        if use_screenshot:
            logger.info("按下s键获取屏幕截图")
            with MoniterKeyboardUtils('s', toggle_clicking_func=grab_func):
                while True:
                    if grab_flag:
                        screenshot = ImageGrab.grab()
                        threading.Thread(target=show_image, args=(screenshot,)).start()
                        break

        logger.info(f"开始保存鼠标中键点击的位置为中心的图标到{icon_dir}")
        with MoniterKeyboardUtils('esc', func) as moniter:
            count = 0
            while True:
                try:
                    count += 1
                    x, y = MouseUtils.get_mouse_click_position(button='middle')
                    if finish_flag:
                        break
                    img = ImageGrab.grab(bbox=(x - size[0] // 2, y - size[1] // 2, x + size[0] // 2, y + size[1] // 2))
                    img.save(os.path.join(icon_dir, f"icon{count}.png"))
                    logger.info(f"已保存鼠标点击的位置为中心的图标 {count}")
                except Exception as e:
                    logger.error(f"保存鼠标点击的位置为中心的图标 {count} 失败：{str(e)}")
        logger.info("保存图标结束")


class AutoClickGenerator:
    def __init__(self, window_name: Optional[str] = None, image_dir: str = "../image", temp_dir: str = "../temp"):
        self.auto_click_utils = AutoClickByImageUtils(window_name, image_dir, temp_dir)
        time.sleep(1)
        self.icon_list = []
        self.click_res = False

    def add_icon(self, icon_name: str, multi_scale: bool = False, ignore_color: bool = False, binarize: bool = False,
                 edge_only: bool = False, similarity_threshold: float = 0.8):
        try:
            res, x, y = self.auto_click_utils.check_icon(icon_name, multi_scale=multi_scale, ignore_color=ignore_color,
                                                         binarize=binarize, edge_only=edge_only,
                                                         similarity_threshold=similarity_threshold)
            if res:
                self.icon_list.append((icon_name, x, y))
                logger.info(f"添加图标 {icon_name} 成功")
            else:
                logger.warning(f"添加图标 {icon_name} 失败")
        except Exception as e:
            logger.error(f"添加图标 {icon_name} 失败：{str(e)}")
        return self

    def add_icons(self, icon_name_list: List[str]):
        for icon_name in icon_name_list:
            self.add_icon(icon_name)
        return self

    def click_by_order(self, interval: float = 1, xy_offset: Tuple[int, int] = (0, 0), multi_scale: bool = False,
                       ignore_color: bool = False, binarize: bool = False,
                       edge_only: bool = False, similarity_threshold: float = 0.8):
        xy_list = []
        for icon_name in os.listdir(self.auto_click_utils.icon_dir):
            try:
                res, x, y = self.auto_click_utils.check_icon(icon_name, multi_scale=multi_scale,
                                                             ignore_color=ignore_color, binarize=binarize,
                                                             edge_only=edge_only,
                                                             similarity_threshold=similarity_threshold)
                if res:
                    xy_list.append((x, y))
                    AutoClickByImageUtils.click_icon((x + xy_offset[0], y + xy_offset[1]))
                    logger.info(f"点击图标 {icon_name} 成功")
                    time.sleep(interval)
                else:
                    logger.warning(f"点击图标 {icon_name} 失败")
            except Exception as e:
                logger.error(f"点击图标 {icon_name} 失败：{str(e)}")
        return self, xy_list

    def click(self, interval: float = 1, xy_offset: Tuple[int, int] = (0, 0)):
        self.click_res = False
        for icon_name, x, y in self.icon_list:
            try:
                AutoClickByImageUtils.click_icon((x + xy_offset[0], y + xy_offset[1]))
                logger.info(f"点击图标 {icon_name} 成功")
                time.sleep(interval)
                self.click_res = True
            except Exception as e:
                logger.error(f"点击图标 {icon_name} 失败：{str(e)}")
        self.icon_list.clear()
        return self
