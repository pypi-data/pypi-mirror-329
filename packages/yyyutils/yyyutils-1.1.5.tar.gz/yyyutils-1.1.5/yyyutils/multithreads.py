"""
TODO: 添加任务队列，避免任务过多时，阻塞主进程
"""
import threading
import time


class MyThreadPool:
    def __init__(self, max_threads, per_wait_time=1):
        if max_threads <= 0:
            raise ValueError("max_threads must be greater than 0")
        if max_threads > 32:
            max_threads = 32
        self.max_threads = max_threads
        self.threads = []
        self.per_wait_time = per_wait_time

    def add_task(self, task):
        while True:
            for t in self.threads:
                if not t.is_alive():
                    self.threads.remove(t)
            if len(self.threads) < self.max_threads:
                t = threading.Thread(target=task)
                t.start()
                self.threads.append(t)
                break
            else:
                print("Waiting for available threads...")
                time.sleep(self.per_wait_time)

    def wait_for_all(self):
        for t in self.threads:
            t.join()
