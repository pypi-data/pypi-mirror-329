import win32gui
import win32con
import win32api
import time
from typing import List, Tuple, Optional
import psutil
import win32process


class WindowUtils:
    """用于处理窗口相关的工具类"""

    @staticmethod
    def __enum_windows(callback, visible_only: bool = True) -> List[Tuple[int, str]]:
        """枚举窗口的通用方法"""

        def winEnumHandler(hwnd, ctx):
            if not visible_only or win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if not visible_only or title:
                    ctx.append((hwnd, title))
            return True

        windows = []
        win32gui.EnumWindows(winEnumHandler, windows)
        return windows

    @staticmethod
    def __get_all_windows(visible_only: bool = True) -> List[Tuple[int, str]]:
        """获取所有窗口的句柄和标题"""
        return WindowUtils.__enum_windows(lambda hwnd, ctx: ctx.append((hwnd, win32gui.GetWindowText(hwnd))),
                                          visible_only)

    @staticmethod
    def get_window_handle(title: str) -> int:
        """根据窗口标题获取窗口句柄，可以是窗口名字的子串"""
        for hwnd, window_title in WindowUtils.__get_all_windows():
            if title.lower() in window_title.lower():
                return hwnd
        raise ValueError(f"Can't find window with title: {title}")

    @staticmethod
    def get_window_title(handle: int) -> str:
        """根据窗口句柄获取窗口标题"""
        return win32gui.GetWindowText(handle)

    @staticmethod
    def get_window_rect(handle: int) -> Tuple[int, int, int, int]:
        """根据窗口句柄获取窗口位置信息"""
        return win32gui.GetWindowRect(handle)

    @staticmethod
    def set_window_pos(handle: int, x: int, y: int, width: int, height: int,
                       flags: int = win32con.SWP_NOZORDER) -> None:
        """设置窗口位置信息"""
        win32gui.SetWindowPos(handle, 0, x, y, width, height, flags)

    @staticmethod
    def show_window(handle: int, show: bool = True) -> int:
        """显示或隐藏窗口"""
        win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL if show else win32con.SW_HIDE)
        return handle

    @staticmethod
    def set_window_topmost(handle: int, topmost: bool = True) -> int:
        """置顶窗口"""
        win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST if topmost else win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return handle

    @staticmethod
    def disable_window(handle: int, disable: bool = True) -> None:
        """窗口禁用"""
        win32gui.EnableWindow(handle, not disable)

    @staticmethod
    def activate_window(handle: int) -> None:
        """激活窗口并将其提到前台"""
        win32gui.SetForegroundWindow(handle)

    @staticmethod
    def close_window(handle: int) -> None:
        """关闭窗口"""
        win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

    @staticmethod
    def drag_mouse(x1: int, y1: int, x2: int, y2: int, duration: float = 1.0) -> None:
        """
        在指定时间内拖动鼠标
        :param x1: 起始位置x
        :param y1: 起始位置y
        :param x2: 结束位置x
        :param y2: 结束位置y
        :param duration: 拖动总时间（秒）
        """
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y1, 0, 0)

        steps = 100
        interval = duration / steps

        start_time = time.time()
        for t in range(1, steps + 1):
            progress = t / steps
            x = int(x1 + (x2 - x1) * progress)
            y = int(y1 + (y2 - y1) * progress)
            win32api.SetCursorPos((x, y))

            elapsed = time.time() - start_time
            remaining = (t * interval) - elapsed
            if remaining > 0:
                time.sleep(remaining)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y2, 0, 0)

    @staticmethod
    def get_foreground_window() -> Tuple[int, str]:
        """获取当前前台窗口句柄和标题"""
        handle = win32gui.GetForegroundWindow()
        return handle, win32gui.GetWindowText(handle)

    @staticmethod
    def get_all_window_titles(visible_only: bool = True) -> List[str]:
        """获取所有窗口标题"""
        return [title for _, title in WindowUtils.__get_all_windows(visible_only)]

    @staticmethod
    def get_all_window_handles(visible_only: bool = True) -> List[int]:
        """获取所有窗口句柄"""
        return [hwnd for hwnd, _ in WindowUtils.__get_all_windows(visible_only)]

    @staticmethod
    def get_pids_by_name(name: str) -> List[int]:
        """根据进程名获取所有匹配的进程ID列表"""
        pids = [proc.info['pid'] for proc in psutil.process_iter(['pid', 'name']) if
                name.lower() in proc.info['name'].lower()]
        if not pids:
            raise ValueError(f"Can't find any process with name: {name}")
        return pids

    @staticmethod
    def get_hwnd_by_pid(pid: int) -> List[int]:
        """根据进程ID获取窗口句柄列表"""

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    @staticmethod
    def get_all_hwnds_and_titles_by_process_name(name: str) -> Tuple[List[int], List[str], List[int]]:
        """根据进程名获取所有匹配进程的窗口句柄、标题和有效句柄"""
        all_hwnds = []
        all_titles = []
        pids = WindowUtils.get_pids_by_name(name)
        for pid in pids:
            hwnds = WindowUtils.get_hwnd_by_pid(pid)
            all_hwnds.extend(hwnds if hwnds else [None])

        true_hwnds = [hwnd for hwnd in all_hwnds if hwnd is not None]
        all_titles = [win32gui.GetWindowText(hwnd) for hwnd in true_hwnds]

        return all_hwnds, all_titles, true_hwnds

    @staticmethod
    def is_window_minimized(hwnd: int) -> bool:
        """检查窗口是否最小化"""
        return win32gui.IsIconic(hwnd)

    @staticmethod
    def is_window_maximized(hwnd: int) -> bool:
        """检查窗口是否最大化"""
        return win32gui.IsZoomed(hwnd)

    @staticmethod
    def minimize_window(hwnd: int) -> None:
        """最小化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    @staticmethod
    def maximize_window(hwnd: int) -> None:
        """最大化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    @staticmethod
    def restore_window(hwnd: int) -> None:
        """还原窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    @staticmethod
    def restore_window_by_pid(pid: int) -> None:
        """根据进程ID恢复最小化的应用程序窗口"""

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        if hwnds:
            print(f"Restored windows for PID {pid}")


if __name__ == '__main__':
    WindowUtils.set_window_topmost(WindowUtils.get_window_handle("mytools"), False)
