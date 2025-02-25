"""
TODO:
- MyProcessPoolSameTask类，把进程调用的绑定方法改为静态方法，避免序列化问题
- MyProcessPoolSameTask类和MyProcessPoolDifferentTask类，把是否需要阻塞主进程和是否需要返回结果的参数放在类初始化时指定
- 主线程创建任务的class，可以执行不同的任务
"""
import multiprocessing
import time


class MyProcessPoolSameTask:
    """
    进程池，用于执行相同的任务，每个任务都一样，不需要返回结果
    """

    def __init__(self, max_processes=3, per_wait_time=1):
        if max_processes <= 0:
            raise ValueError("max_processes must be greater than 0")
        if max_processes > 16:
            max_processes = 16
        self.max_processes = max_processes
        self.processes = []
        self.per_wait_time = per_wait_time
        self.task_queue = []
        self.inform_queue = multiprocessing.Queue()
        self.original_task = True
        self.need_return = None
        self.is_join_main = None

    def _auto_add_task(self, num_of_task, task, args=()):
        """
        在添加任务的进程中，自动添加任务到任务队列并更新主进程的任务队列,每个任务都一样
        :param num_of_task:
        :param task:
        :param args:
        :return:
        """
        for i in range(num_of_task):
            self.task_queue.append((task, args))
        self.inform_queue.put(self.task_queue)

    @staticmethod
    def _new_task(task, args=(), result_queue=None):
        """
        私有函数，用于重构任务函数，使用队列通信返回结果
        :param task:
        :param args:
        :param result_queue:
        :return:
        """
        result = task(*args)
        result_queue.put(result)

    def add_task_process(self, num_of_task, task, args=(), need_return=False):
        """
        单独用于添加任务的进程，参数need_return用于控制任务是否需要返回结果
        :param num_of_task:用于指定需要添加的任务数量
        :param task:添加的任务函数
        :param args:给添加任务的函数的参数
        :param need_return:依据need_return的值，决定是否重构任务函数（使用队列通信返回结果）
        :return:
        """
        if need_return:
            self.need_return = True
            self.original_task = False
        original_task = task
        # 判断任务函数是否有返回值，如果有，则重构任务函数，使用队列通信
        if need_return:
            task = MyProcessPoolSameTask._new_task
            args = (original_task, args)
        temp_process = multiprocessing.Process(target=self._auto_add_task, args=(num_of_task, task, args))
        temp_process.start()
        temp_process.join()

    def _start(self, result_queue_to_main):
        """
        私有函数，在用于启动进程池的进程中，启动所有子进程，如果需要返回结果，则将结果放入result_queue_to_main通知给主进程
        :param result_queue_to_main:
        :return:
        """
        result_queue = multiprocessing.Queue()
        num = len(self.task_queue)
        for i in range(num):
            while True:
                for p in self.processes[:]:
                    if not p.is_alive():
                        p.terminate()
                        self.processes.remove(p)
                if len(self.processes) < self.max_processes:
                    task = self.task_queue[i]
                    # print(task)
                    if not self.original_task:
                        args = (*task[1], result_queue)
                        # print(args)
                    else:
                        args = task[1]
                    p = multiprocessing.Process(target=task[0], args=args)
                    p.start()
                    self.processes.append(p)
                    break
                else:
                    time.sleep(self.per_wait_time)
        # 所有子进程都结束后，获取结果
        for p in self.processes:
            p.join()
        if not self.original_task:
            while not result_queue.empty():
                result_queue_to_main.put(result_queue.get())

    def start_process(self, is_join_main=True):
        """
        单独用于启动进程池的进程，参数is_join_main用于控制是否阻塞主进程，只有阻塞主进程才能获取结果
        :param is_join_main: 控制是否阻塞主进程以等待所有任务完成
        :return:
        """

        if not is_join_main and self.need_return:
            raise ValueError("need_return must be False when is_join_main is False")
        result_queue = multiprocessing.Queue()
        if not self.task_queue:
            self.task_queue = self.inform_queue.get()
        # print(self.task_queue)
        start_task_process = multiprocessing.Process(target=self._start, args=(result_queue,))
        start_task_process.start()
        if is_join_main:
            start_task_process.join()
            # 只有当所有子进程都结束后，才会获取结果，故如果不阻塞主进程则无法获取结果
            result_list = []
            while not result_queue.empty():
                result_list.append(result_queue.get())
            return result_list


class MyProcessPoolDifferentTask:
    """
    进程池，用于执行不同的任务，每个任务都不一样，需要返回结果
    """
    def __init__(self, max_processes=3, per_wait_time=1,per_task_time=0, need_return=False):
        if max_processes <= 0:
            raise ValueError("max_processes must be greater than 0")
        if max_processes > 16:
            max_processes = 16
        self.max_processes = max_processes
        self.processes = []
        self.per_wait_time = per_wait_time
        self.per_task_time = per_task_time
        self.task_queue = []
        self.need_return = need_return
        self.result_queue = multiprocessing.Queue()

    @staticmethod
    def _new_task(task, args=(), result_queue=None):
        """
        私有函数，用于重构任务函数，使用队列通信返回结果
        :param task:
        :param args:
        :param result_queue:
        :return:
        """
        result = task(*args)
        result_queue.put(result)

    def add_task(self, task, args: tuple = ()):
        """
        主进程中逐个添加任务，每个任务可以不一样，待实现
        :param task:
        :param args:
        :return:
        """
        original_task = task
        if self.need_return:
            task = self._new_task
            args = (original_task, args)
        self.task_queue.append((task, args))

    @staticmethod
    def _start(instance, result_queue_to_main=None):
        if instance.need_return:
            result_queue = multiprocessing.Queue()
        num = len(instance.task_queue)
        for i in range(num):
            while True:
                for p in instance.processes[:]:
                    if not p.is_alive():
                        p.terminate()
                        instance.processes.remove(p)
                if len(instance.processes) < instance.max_processes:
                    task = instance.task_queue[i]
                    # print(task)
                    if instance.need_return:
                        args = (*task[1], result_queue)
                        print(args)
                    else:
                        args = task[1]
                    if instance.per_task_time > 0 and i > 0:
                        time.sleep(instance.per_task_time)
                    p = multiprocessing.Process(target=task[0], args=args)
                    p.start()
                    instance.processes.append(p)
                    break
                else:
                    time.sleep(instance.per_wait_time)
        # 所有子进程都结束后，获取结果
        for p in instance.processes:
            p.join()
        if instance.need_return:
            while not result_queue.empty():
                result_queue_to_main.put(result_queue.get())

    def start_process(self, is_join_main=True):
        # print(self.task_queue)
        if not is_join_main and self.need_return:
            raise ValueError("need_return must be False when is_join_main is False")
        if self.need_return:
            args = (self, self.result_queue,)
        else:
            args = (self,)

        start_task_process = multiprocessing.Process(target=MyProcessPoolDifferentTask._start, args=args)
        start_task_process.start()
        if is_join_main:
            start_task_process.join()
            # 只有当所有子进程都结束后，才会获取结果，故如果不阻塞主进程则无法获取结果
            result_list = []
            while not self.result_queue.empty():
                result_list.append(self.result_queue.get())
            return result_list


def task1(x, mm):
    print(multiprocessing.current_process().name, x, mm)


if __name__ == '__main__':
    m = MyProcessPoolDifferentTask(max_processes=3, per_wait_time=1,per_task_time=0)
    mm = input()
    for i in range(10):
        m.add_task(task1, (i, mm))
    m.start_process(is_join_main=True)
