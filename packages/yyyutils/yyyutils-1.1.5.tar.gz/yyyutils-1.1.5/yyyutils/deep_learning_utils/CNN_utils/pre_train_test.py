# import torch
# import copy
# import os
#
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# import pandas as pd
# import time
# import torch.nn as nn
# import matplotlib.pyplot as plt
# from matplotlib import font_manager
#
# # 设置字体为 SimHei 或其他支持中文的字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
# import keyboard
# import numpy as np
# import colorama
# from yyyutils.decorator_utils import DecoratorUtils
# from typing import Callable
#
#
# class TrainTestUtils():
#     """
#     用于训练和测试模型的工具类，可以自定义预测标签的函数和求loss的函数
#     """
#
#     def __init__(self, predict_label_func: Callable = None,
#                  loss_func: Callable = None):
#         self.predict_label_func = TrainTestUtils.__default_predict_label if predict_label_func is None else predict_label_func
#         self.loss_func = TrainTestUtils.__default_loss_func if loss_func is None else loss_func
#
#     @staticmethod
#     def __default_predict_label(output, by):
#         return torch.argmax(output, dim=1), by
#
#     @staticmethod
#     def __default_loss_func(output, target):
#         return nn.CrossEntropyLoss()(output, target)
#
#     @DecoratorUtils.validate_input
#     def train(self, model, train_loader, test_loader, epoches: int, lr: float,
#               load_model_path: str = None,
#               batch_debug: bool = False, stop_by_esc: bool = False, compare_row: bool = False):
#         """
#         :param model:
#         :param train_loader:
#         :param test_loader:
#         :param epoches:
#         :param lr:
#         :param predict_label_func: 预测标签的函数，默认使用torch.argmax(output, dim=1)
#         :param loss_func: 求出loss的函数，默认使用nn.CrossEntropyLoss()(output, target)
#         :param read_model_path:
#         :param batch_debug:
#         :param stop_by_esc:
#         :return:
#         """
#         device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#         model = model.to(device)
#         colorama.init()
#         if load_model_path is not None:
#             model.load_state_dict(torch.load(load_model_path, weights_only=True))
#
#         optimizer = torch.optim.Adam(model.parameters(), lr=lr)
#
#         best_model_wts = copy.deepcopy(model.state_dict())
#
#         best_acc = 0.0
#
#         train_loss_list = []
#         test_loss_list = []
#         train_acc_list = []
#         test_acc_list = []
#         token = False
#         since = time.time()
#         for epoch in range(epoches):
#             print('-' * 30)
#             print('Epoch {}/{}'.format(epoch + 1, epoches))
#             train_loss = 0.0
#             train_correct = 0
#             test_loss = 0.0
#             test_correct = 0
#             train_num = 0
#             test_num = 0
#             for i, (bx, by) in enumerate(train_loader):
#                 batch_since = time.time()
#                 bx = bx.to(device)
#                 by = by.to(device)
#
#                 model.train()
#                 output = model(bx)
#                 pre_label, real_label = self.predict_label_func(output, by)
#                 # print(by)
#                 # print(pre_label)
#                 loss = self.loss_func(output, by)
#
#                 optimizer.zero_grad()
#                 loss.backward()
#                 optimizer.step()
#
#                 train_loss += loss.item() * bx.size(0)
#                 # print(output)
#                 # print(pre_label)
#                 # print(real_label)
#                 if compare_row:
#                     correct_predictions = torch.all(pre_label == real_label, dim=1)  # 检查每一行是否完全相同
#                     train_correct += correct_predictions.sum().item()  # 统计符合条件的行数
#                 else:
#                     train_correct += torch.sum(pre_label == real_label).item()
#                 # print(train_correct)
#                 train_num += bx.size(0)
#                 if stop_by_esc:
#                     if keyboard.is_pressed('esc'):
#                         if epoch == 0:
#                             raise KeyboardInterrupt('第一次迭代未完成！！！')
#                         token = True
#                         print("\nEsc键被按下，退出训练并保存模型")
#                         break
#                 if batch_debug:
#                     print('\r\ttrain Batch Debug: {} [{}/{} bt]\t{:.2f}s'.format(
#                         colorama.Fore.GREEN + str(
#                             round((i + 1) / len(train_loader) * 100)) + '%' + colorama.Style.RESET_ALL,
#                         i + 1, len(train_loader), (time.time() - batch_since) * (len(train_loader) - i - 1)), end='')
#             if token:
#                 break
#             print()
#             # print()
#             for i, (bx, by) in enumerate(test_loader):
#                 batch_since = time.time()
#                 bx = bx.to(device)
#                 by = by.to(device)
#
#                 model.eval()
#                 output = model(bx)
#                 pre_label, real_label = self.predict_label_func(output, by)
#                 loss = self.loss_func(output, by)
#
#                 test_loss += loss.item() * bx.size(0)
#                 if compare_row:
#                     correct_predictions = torch.all(pre_label == real_label, dim=1)  # 检查每一行是否完全相同
#                     test_correct += correct_predictions.sum().item()  # 统计符合条件的行数
#                 else:
#                     test_correct += torch.sum(pre_label == real_label).item()
#                 test_num += bx.size(0)
#                 batch_time_used = time.time() - batch_since
#                 if batch_debug:
#                     print('\r\tval Batch Debug: {} [{}/{} bt]\t{:.2f}s'.format(
#                         colorama.Fore.GREEN + str(
#                             round((i + 1) / len(test_loader) * 100)) + '%' + colorama.Style.RESET_ALL,
#                         i + 1, len(test_loader), batch_time_used * (len(test_loader) - i - 1)), end='')
#             if not token:
#                 train_loss_list.append(train_loss / train_num)
#                 test_loss_list.append(test_loss / test_num)
#                 train_acc_list.append(float(train_correct) / train_num)
#                 test_acc_list.append(float(test_correct) / test_num)
#                 print()
#                 print('Train Loss: {:.4f} Acc: {:.4f} '.format(train_loss_list[-1], train_acc_list[-1]))
#                 print('Test Loss: {:.4f} Acc: {:.4f} '.format(test_loss_list[-1], test_acc_list[-1]))
#
#                 if test_acc_list[-1] > best_acc:
#                     best_acc = test_acc_list[-1]
#                     best_model_wts = copy.deepcopy(model.state_dict())
#
#                 time_used = time.time() - since
#                 print('All time used: {}h {}m {:.2f}s'.format(int(time_used // 3600), int((time_used % 3600) // 60),
#                                                               time_used % 60))
#         if token:
#             num = epoch
#         else:
#             num = epoch + 1
#         train_process = pd.DataFrame(
#             {'epoch': range(1, num + 1), 'train_loss': train_loss_list, 'train_acc': train_acc_list,
#              'test_loss': test_loss_list, 'test_acc': test_acc_list})
#
#         return best_model_wts, train_process
#
#     def save_best_model(self, best_model_wts, path):
#         torch.save(best_model_wts, path)
#
#     def plot_train_process(self, train_process):
#         """
#         plot train process
#         """
#         plot_name = os.path.basename(os.getcwd())
#         plt.figure(figsize=(12, 4))
#         plt.subplot(1, 2, 1)
#         plt.plot(np.array(train_process['epoch']), np.array(train_process['train_loss']), 'ro-', label='train_loss')
#         plt.plot(np.array(train_process['epoch']), np.array(train_process['test_loss']), 'bo-', label='eval_loss')
#         plt.xlabel('epoch')
#         plt.ylabel('loss')
#         plt.legend()
#         plt.title(plot_name)
#         plt.subplot(1, 2, 2)
#         plt.plot(np.array(train_process['epoch']), np.array(train_process['train_acc']), 'ro-', label='train_acc')
#         plt.plot(np.array(train_process['epoch']), np.array(train_process['test_acc']), 'bo-', label='eval_acc')
#         plt.xlabel('epoch')
#         plt.ylabel('accuracy')
#         plt.legend()
#         plt.title(plot_name)
#         plt.show()
#
#     def test(self, model, test_loader, load_model_path=None, debug=False, classes: list = None, debug_num=10,
#              row_compare=False):
#         colorama.init()
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         if load_model_path is not None:
#             model.load_state_dict(torch.load(load_model_path, weights_only=True))
#         model.to(device)
#         model.eval()
#         test_acc = 0
#         test_num = 0
#         error_num = 0
#         with torch.no_grad():
#             for i, (dx, dy) in enumerate(test_loader):
#                 dx, dy = dx.to(device), dy.to(device)
#                 output = model(dx)
#                 pred, real_label = self.predict_label_func(output, dy)
#
#                 # 处理标量和张量的情况
#                 if isinstance(pred, torch.Tensor) and pred.dim() > 1:
#                     # 张量情况
#                     if row_compare:
#                         correct_predictions = torch.all(pred == real_label, dim=1)
#                         test_acc += correct_predictions.sum().item()
#                     else:
#                         test_acc += torch.sum(pred == real_label).item()
#                     test_num += dx.size(0) * (pred.size(1) if not row_compare else 1)
#                 else:
#                     # 标量情况
#                     test_acc += torch.sum(pred == real_label).item()
#                     test_num += dx.size(0)
#
#                 if debug and i < debug_num:
#                     self._debug_output(pred, real_label, classes, error_num)
#                     if i == debug_num - 1:
#                         print(f"\n检测数量: {debug_num}，错误数量: {error_num}")
#
#             print('Test Total Accuracy: {:.2f}%'.format(100 * test_acc / test_num))
#
#     def _debug_output(self, pred, real_label, classes, error_num):
#         if isinstance(pred, torch.Tensor) and pred.dim() > 1:
#             # 处理张量情况
#             for p, r in zip(pred, real_label):
#                 if torch.all(p == r):
#                     print(f"真实值: {r.tolist()} ------- 预测值: {p.tolist()}")
#                 else:
#                     error_num += 1
#                     print(
#                         colorama.Fore.RED + f"真实值: {r.tolist()} ------- 预测值: {p.tolist()}" + colorama.Style.RESET_ALL)
#         else:
#             # 处理标量情况
#             if classes is None:
#                 if pred.item() != real_label.item():
#                     error_num += 1
#                     print(
#                         colorama.Fore.RED + f"真实值: {real_label.item()} ------- 预测值: {pred.item()}" + colorama.Style.RESET_ALL)
#                 else:
#                     print(f"真实值: {real_label.item()} ------- 预测值: {pred.item()}")
#             else:
#                 if pred.item() != real_label.item():
#                     error_num += 1
#                     print(
#                         colorama.Fore.RED + f"真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}" + colorama.Style.RESET_ALL)
#                 else:
#                     print(f"真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}")
#
#         return error_num
#
#
# if __name__ == '__main__':
#     pass

import torch
import copy
import os
import pandas as pd
import time
import torch.nn as nn
import matplotlib.pyplot as plt
import keyboard
import numpy as np
import colorama
from yyyutils.decorator_utils import DecoratorUtils
from typing import Callable, List, Optional

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 设置字体为 SimHei 或其他支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题


class TrainTestUtils:
    """用于训练和测试模型的工具类，可以自定义预测标签的函数和求loss的函数"""

    def __init__(self, predict_label_func: Optional[Callable] = None,
                 loss_func: Optional[Callable] = None):
        self.predict_label_func = predict_label_func or self.__default_predict_label
        self.loss_func = loss_func or self.__default_loss_func

    @staticmethod
    def __default_predict_label(output: torch.Tensor, by: torch.Tensor) -> tuple:
        return torch.argmax(output, dim=1), by

    @staticmethod
    def __default_loss_func(output: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return nn.CrossEntropyLoss()(output, target)

    @DecoratorUtils.validate_input
    def train(self, model: nn.Module, train_loader: torch.utils.data.DataLoader,
              test_loader: torch.utils.data.DataLoader, epoches: int, lr: float,
              load_model_path: Optional[str] = None, batch_debug: bool = False,
              stop_by_esc: bool = False, compare_row: bool = False) -> tuple:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        colorama.init()

        if load_model_path:
            model.load_state_dict(torch.load(load_model_path, map_location=device))

        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        train_loss_list, test_loss_list, train_acc_list, test_acc_list = [], [], [], []

        since = time.time()
        for epoch in range(epoches):
            print('-' * 30)
            print(f'Epoch {epoch + 1}/{epoches}')

            train_loss, train_correct, test_loss, test_correct = 0.0, 0, 0.0, 0
            train_num, test_num = 0, 0

            # Training phase
            model.train()
            for i, (bx, by) in enumerate(train_loader):
                batch_since = time.time()
                bx, by = bx.to(device), by.to(device)

                output = model(bx)
                pre_label, real_label = self.predict_label_func(output, by)
                loss = self.loss_func(output, by)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                train_loss += loss.item() * bx.size(0)
                train_correct += self._calculate_correct(pre_label, real_label, compare_row)
                train_num += bx.size(0)

                if stop_by_esc and keyboard.is_pressed('esc'):
                    if epoch == 0:
                        raise KeyboardInterrupt('第一次迭代未完成！！！')
                    print("\nEsc键被按下，退出训练并保存模型")
                    return best_model_wts, self._create_train_process(epoch, train_loss_list, train_acc_list,
                                                                      test_loss_list, test_acc_list)

                if batch_debug:
                    self._print_batch_progress('train', i, len(train_loader), time.time() - batch_since)

            print()  # 换行

            # Validation phase
            model.eval()
            with torch.no_grad():
                for i, (bx, by) in enumerate(test_loader):
                    batch_since = time.time()
                    bx, by = bx.to(device), by.to(device)

                    output = model(bx)
                    pre_label, real_label = self.predict_label_func(output, by)
                    loss = self.loss_func(output, by)

                    test_loss += loss.item() * bx.size(0)
                    test_correct += self._calculate_correct(pre_label, real_label, compare_row)
                    test_num += bx.size(0)

                    if batch_debug:
                        self._print_batch_progress('val', i, len(test_loader), time.time() - batch_since)

            # Calculate and store metrics
            train_loss_list.append(train_loss / train_num)
            test_loss_list.append(test_loss / test_num)
            train_acc_list.append(float(train_correct) / train_num)
            test_acc_list.append(float(test_correct) / test_num)

            print()
            print(f'Train Loss: {train_loss_list[-1]:.4f} Acc: {train_acc_list[-1]:.4f}')
            print(f'Test Loss: {test_loss_list[-1]:.4f} Acc: {test_acc_list[-1]:.4f}')

            if test_acc_list[-1] > best_acc:
                best_acc = test_acc_list[-1]
                best_model_wts = copy.deepcopy(model.state_dict())

            time_used = time.time() - since
            print(f'All time used: {int(time_used // 3600)}h {int((time_used % 3600) // 60)}m {time_used % 60:.2f}s')

        return best_model_wts, self._create_train_process(epoches, train_loss_list, train_acc_list, test_loss_list,
                                                          test_acc_list)

    def _calculate_correct(self, pre_label: torch.Tensor, real_label: torch.Tensor, compare_row: bool) -> int:
        if compare_row:
            return torch.all(pre_label == real_label, dim=1).sum().item()
        return torch.sum(pre_label == real_label).item()

    def _print_batch_progress(self, phase: str, current: int, total: int, time_left: float):
        progress = colorama.Fore.GREEN + f"{round((current + 1) / total * 100)}%" + colorama.Style.RESET_ALL
        print(
            f'\r\t{phase} Batch Debug: {progress} [{current + 1}/{total} bt]\t{time_left * (total - current - 1):.2f}s',
            end='')

    def _create_train_process(self, num_epochs: int, train_loss: List[float], train_acc: List[float],
                              test_loss: List[float], test_acc: List[float]) -> pd.DataFrame:
        return pd.DataFrame({
            'epoch': range(1, num_epochs + 1),
            'train_loss': train_loss,
            'train_acc': train_acc,
            'test_loss': test_loss,
            'test_acc': test_acc
        })

    def save_best_model(self, best_model_wts: dict, path: str):
        torch.save(best_model_wts, path)

    def plot_train_process(self, train_process: pd.DataFrame):
        """绘制训练过程"""
        plot_name = os.path.basename(os.getcwd())
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.plot(train_process['epoch'], train_process['train_loss'], 'ro-', label='train_loss')
        ax1.plot(train_process['epoch'], train_process['test_loss'], 'bo-', label='eval_loss')
        ax1.set_xlabel('epoch')
        ax1.set_ylabel('loss')
        ax1.legend()
        ax1.set_title(plot_name)

        ax2.plot(train_process['epoch'], train_process['train_acc'], 'ro-', label='train_acc')
        ax2.plot(train_process['epoch'], train_process['test_acc'], 'bo-', label='eval_acc')
        ax2.set_xlabel('epoch')
        ax2.set_ylabel('accuracy')
        ax2.legend()
        ax2.set_title(plot_name)

        plt.show()

    def test(self, model: nn.Module, test_loader: torch.utils.data.DataLoader,
             load_model_path: Optional[str] = None, debug: bool = False,
             classes: Optional[List[str]] = None, debug_num: int = 10,
             row_compare: bool = False):
        colorama.init()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if load_model_path:
            model.load_state_dict(torch.load(load_model_path, map_location=device))

        model.to(device)
        model.eval()

        test_acc, test_num, error_num = 0, 0, 0

        with torch.no_grad():
            for i, (dx, dy) in enumerate(test_loader):
                dx, dy = dx.to(device), dy.to(device)
                output = model(dx)
                pred, real_label = self.predict_label_func(output, dy)

                if isinstance(pred, torch.Tensor) and pred.dim() > 1:
                    test_acc += self._calculate_correct(pred, real_label, row_compare)
                    test_num += dx.size(0) * (pred.size(1) if not row_compare else 1)
                else:
                    test_acc += torch.sum(pred == real_label).item()
                    test_num += dx.size(0)

                if debug and i < debug_num:
                    error_num = self._debug_output(pred, real_label, classes, error_num)
                    if i == debug_num - 1:
                        print(f"\n检测数量: {debug_num}，错误数量: {error_num}")

            print(f'Test Total Accuracy: {100 * test_acc / test_num:.2f}%')

    def _debug_output(self, pred: torch.Tensor, real_label: torch.Tensor,
                      classes: Optional[List[str]], error_num: int) -> int:
        if isinstance(pred, torch.Tensor) and pred.dim() > 1:
            for p, r in zip(pred, real_label):
                if torch.all(p == r):
                    print(f"真实值: {r.tolist()} ------- 预测值: {p.tolist()}")
                else:
                    error_num += 1
                    print(
                        colorama.Fore.RED + f"真实值: {r.tolist()} ------- 预测值: {p.tolist()}" + colorama.Style.RESET_ALL)
        else:
            if classes is None:
                if pred.item() != real_label.item():
                    error_num += 1
                    print(
                        colorama.Fore.RED + f"真实值: {real_label.item()} ------- 预测值: {pred.item()}" + colorama.Style.RESET_ALL)
                else:
                    print(f"真实值: {real_label.item()} ------- 预测值: {pred.item()}")
            else:
                if pred.item() != real_label.item():
                    error_num += 1
                    print(
                        colorama.Fore.RED + f"真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}" + colorama.Style.RESET_ALL)
                else:
                    print(f"真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}")

        return error_num


if __name__ == '__main__':
    pass
