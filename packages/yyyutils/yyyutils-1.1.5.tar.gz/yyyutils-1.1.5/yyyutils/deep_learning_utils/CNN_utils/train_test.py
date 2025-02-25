import torch
import copy
import os
import pandas as pd
import time
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
import logging
from tqdm import tqdm
from dataclasses import dataclass, asdict
from typing import Callable, Optional
from torch.optim.lr_scheduler import ReduceLROnPlateau
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from torchsummary import summary
from colorama import Fore, Style
import json
from datetime import datetime


@dataclass
class TrainConfig:
    """
    训练配置类

    Attributes:
        epochs (int): 训练轮数
        lr (float): 学习率
        lr_factor (float): 学习率调整因子
        lr_patience (int): 学习率调整耐心值
        load_model_path (Optional[str]): 加载预训练模型的路径，默认为None
        batch_debug (bool): 是否进行批次调试，默认为False
        stop_by_esc (bool): 是否允许通过ESC键停止训练，默认为False
        compare_row (bool): 是否按行比较预测结果，默认为False
        early_stopping_patience (int): 早停的耐心值，默认为10
        gradient_clip_value (Optional[float]): 梯度裁剪值，默认为None
        sort_log_by_val_acc (bool): 是否根据验证集准确率对日志进行降序排序，默认为True，可能会影响性能
        clear_log_file (bool): 是否清空日志文件，默认为False
    """
    epochs: int = 100
    lr: float = 0.001
    lr_factor: float = 0.5
    lr_patience: int = None
    load_model_path: Optional[str] = None
    batch_debug: bool = False
    stop_by_esc: bool = False
    compare_row: bool = False
    early_stopping_patience: int = None
    gradient_clip_value: Optional[float] = None
    sort_log_by_val_acc: bool = True
    clear_log_file: bool = False


@dataclass
class TestConfig:
    """
    测试配置类

    Attributes:
        load_model_path (Optional[str]): 加载模型的路径，默认为None
        debug (bool): 是否进行调试，默认为False
        classes (Optional[list]): 类别列表，默认为None
        debug_num (int): 调试时的样本数量，默认为10
        row_compare (bool): 是否按行比较预测结果，默认为False
        sort_log_by_test_acc (bool): 是否根据测试集准确率对日志进行降序排序，默认为True，可能会影响性能
        clear_log_file (bool): 是否清空日志文件，默认为False
    """
    load_model_path: Optional[str] = None
    debug: bool = False
    classes: Optional[list] = None
    debug_num: int = 10
    row_compare: bool = False
    sort_log_by_test_acc: bool = True
    clear_log_file: bool = False


class TrainTestUtils:
    """
    训练和测试工具类

    Attributes:
        predict_label_func (Callable): 预测标签的函数
        loss_func (Callable): 损失函数
        logger (logging.Logger): 日志记录器
    """

    def __init__(self, predict_and_real_label_to_colculate_acc_func: Callable = None,
                 loss_func: Callable = None, acc_func: Callable = None,
                 change_output_target_to_loss_func: callable = None):
        """
        初始化TrainTestUtils类

        Args:
            predict_and_real_label_to_colculate_acc_func (Callable, optional): 预测标签的函数，默认为None，参数为模型输出和标签
            loss_func (Callable, optional): 损失函数，默认为None，参数为模型输出和标签
            change_output_target_to_loss_func (callable, optional): 将模型输出和标签在输入损失函数之前进行转换的函数，默认为None，参数为模型输出和标签
        """
        self.predict_label_func = self.__default_predict_label if predict_and_real_label_to_colculate_acc_func is None else predict_and_real_label_to_colculate_acc_func
        self.loss_func = self.__default_loss_func if loss_func is None else loss_func
        self.acc_func = acc_func
        self.change_output_target_to_loss_func = self.__default_change_output_target_to_loss_func if change_output_target_to_loss_func is None else change_output_target_to_loss_func
        self.logger = self._setup_logger()

    @staticmethod
    def __default_predict_label(output, by):
        """
        默认的预测标签函数
        """
        return torch.argmax(output, dim=1), by

    @staticmethod
    def __default_loss_func(output, target):
        """
        默认的损失函数
        """
        return nn.CrossEntropyLoss()(output, target)

    @staticmethod
    def __default_acc_func(pre_label, real_label, row_compare=False):
        """
        默认的准确率函数
        """
        return torch.all(pre_label == real_label, dim=1).sum().item() if row_compare else torch.sum(
            pre_label == real_label).item()

    @staticmethod
    def __default_change_output_target_to_loss_func(output, target):
        """
        默认的将模型输出和标签在输入损失函数之前进行转换的函数
        """
        return output, target

    def _setup_logger(self):
        """
        设置日志记录器
        """
        logger = logging.getLogger('train_test_utils')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f'{Fore.WHITE}%(asctime)s - %(name)s - {Fore.GREEN}%(message)s{Style.RESET_ALL}')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def save_config_and_results(self, config, results, filename='experiment_log.jsonl', sort=True):
        """
        保存配置和结果到 JSON 文件

        Args:
            config: 配置对象 (TrainConfig 或 TestConfig)
            results (dict): 训练或测试的结果
            filename (str): 保存的文件名
            sort (bool): 是否对记录进行排序
        """
        config_dict = asdict(config)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "config": config_dict,
            "results": results
        }

        # 尝试读取已有的内容
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                # 如果文件不为空，则读取内容
                file_content = f.read()
                if file_content:
                    # 解析已有的 JSON 数据
                    log_entries = json.loads(file_content)
                    log_entries.append(log_entry)  # 添加新记录

                    # 根据文件名决定排序规则
                    if sort:
                        if filename == 'train_log.jsonl':
                            log_entries.sort(key=lambda x: x['results']['final_val_acc'], reverse=True)
                        elif filename == 'test_log.jsonl':
                            log_entries.sort(key=lambda x: x['results']['test_accuracy'], reverse=True)

                else:
                    # 文件为空，初始写入数组
                    log_entries = [log_entry]

        else:
            # 文件不存在，创建并写入一个新的数组
            log_entries = [log_entry]

        # 将处理后的记录写入文件
        with open(filename, 'w') as f:
            json.dump(log_entries, f)

        self.logger.info(f"配置和结果已保存到 {filename}")

    def load_experiment_log(self, train=True, test=False, print_log=True):
        """
        从 JSON 文件加载实验日志

        Args:
            filename (str): 日志文件名

        Returns:
            list: 包含所有实验记录的列表
        """
        experiments = []
        if train:
            filename = 'train_log.jsonl'
        if test:
            filename = 'test_log.jsonl'

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                file_content = f.read().strip()
                if file_content:
                    # 去掉可能存在的多余换行符，并直接解析文件内容
                    experiments = json.loads(file_content)

        self.logger.info(f"从 {filename} 加载了 {len(experiments)} 条实验记录")
        if print_log:
            for exp in experiments:
                print(f"实验结束时间: {exp['timestamp']}")
                print(f"配置: {exp['config']}")
                print(f"结果: {exp['results']}")
                print("---")
        return experiments

    def train(self, model, train_loader, val_loader, config: TrainConfig = TrainConfig()):
        """
        训练模型
        """
        if config.clear_log_file:
            try:
                os.remove('train_log.jsonl')
            except FileNotFoundError:
                pass
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)

        if config.load_model_path is not None:
            try:
                model.load_state_dict(torch.load(config.load_model_path, map_location=device, weights_only=True))
            except FileNotFoundError:
                self.logger.error(f"模型文件未找到: {config.load_model_path}")
                return None, None

        optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
        if config.lr_patience:
            scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=config.lr_factor, patience=config.lr_patience)

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        train_loss_list, val_loss_list, train_acc_list, val_acc_list = [], [], [], []

        early_stopping_counter = 0

        for epoch in range(config.epochs):
            self.logger.info(f'Epoch {epoch + 1}/{config.epochs}')

            train_loss, train_correct, train_num = self._train_epoch(model, train_loader, optimizer, device, config)
            val_loss, val_correct, val_num = self._val_epoch(model, val_loader, device, config)

            train_loss_list.append(train_loss / train_num)
            val_loss_list.append(val_loss / val_num)
            train_acc_list.append(float(train_correct) / train_num)
            val_acc_list.append(float(val_correct) / val_num)

            self.logger.info(f'Train Loss: {train_loss_list[-1]:.4f} Acc: {train_acc_list[-1]:.4f}')
            self.logger.info(f'Val Loss: {val_loss_list[-1]:.4f} Acc: {val_acc_list[-1]:.4f}')
            if config.lr_patience:
                scheduler.step(val_acc_list[-1])
            current_lr = optimizer.param_groups[0]['lr']
            self.logger.info(f'Current Learning Rate: {current_lr:.6f}')

            if val_acc_list[-1] > best_acc:
                best_acc = val_acc_list[-1]
                best_model_wts = copy.deepcopy(model.state_dict())
                early_stopping_counter = 0
            else:
                early_stopping_counter += 1

            if config.early_stopping_patience is not None and early_stopping_counter >= config.early_stopping_patience:
                self.logger.info(f"Early stopping triggered after {epoch + 1} epochs")
                break

        train_process = pd.DataFrame({
            'epoch': range(1, len(train_loss_list) + 1),
            'train_loss': train_loss_list,
            'train_acc': train_acc_list,
            'val_loss': val_loss_list,
            'val_acc': val_acc_list
        })

        results = {
            "best_accuracy": best_acc,
            "epochs_trained": len(train_loss_list),
            "final_train_loss": train_loss_list[-1],
            "final_train_acc": train_acc_list[-1],
            "final_val_loss": val_loss_list[-1],
            "final_val_acc": val_acc_list[-1]
        }
        self.save_config_and_results(config, results, filename='train_log.jsonl', sort=config.sort_log_by_val_acc)

        return best_model_wts, train_process

    def _train_epoch(self, model, train_loader, optimizer, device, config):
        """
        训练一个epoch
        """
        model.train()
        train_loss, train_correct, train_num = 0.0, 0, 0

        for bx, by in tqdm(train_loader, desc="Training", ):
            bx, by = bx.to(device), by.to(device)

            optimizer.zero_grad()
            output = model(bx)
            pre_label, real_label = self.predict_label_func(output, by)
            loss = self.loss_func(*self.change_output_target_to_loss_func(output, by))

            loss.backward()

            if config.gradient_clip_value is not None:
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.gradient_clip_value)

            optimizer.step()

            train_loss += loss.item() * bx.size(0)
            train_correct += self.acc_func(pre_label,
                                           real_label) if self.acc_func is not None else self.__default_acc_func(
                pre_label, real_label, config.compare_row)
            train_num += bx.size(0)

        return train_loss, train_correct, train_num

    def _val_epoch(self, model, val_loader, device, config):
        """
        测试一个epoch
        """
        model.eval()
        val_loss, val_correct, val_num = 0.0, 0, 0

        with torch.no_grad():
            for bx, by in tqdm(val_loader, desc="Validating", ):
                bx, by = bx.to(device), by.to(device)
                output = model(bx)
                pre_label, real_label = self.predict_label_func(output, by)
                loss = self.loss_func(*self.change_output_target_to_loss_func(output, by))

                val_loss += loss.item() * bx.size(0)
                val_correct += self.acc_func(pre_label, real_label) if self.acc_func is not None else self.__default_acc_func(
                    pre_label, real_label, config.compare_row)
                val_num += bx.size(0)

        return val_loss, val_correct, val_num

    def save_best_model(self, best_model_wts, path):
        """
        保存最佳模型
        """
        torch.save(best_model_wts, path)

    def plot_train_process(self, train_process):
        """
        绘制训练过程
        """
        plot_name = os.path.basename(os.getcwd())
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Loss', 'Accuracy'))

        fig.add_trace(go.Scatter(x=train_process['epoch'], y=train_process['train_loss'],
                                 mode='lines+markers', name='Train Loss'), row=1, col=1)
        fig.add_trace(go.Scatter(x=train_process['epoch'], y=train_process['val_loss'],
                                 mode='lines+markers', name='Val Loss'), row=1, col=1)

        fig.add_trace(go.Scatter(x=train_process['epoch'], y=train_process['train_acc'],
                                 mode='lines+markers', name='Train Accuracy'), row=1, col=2)
        fig.add_trace(go.Scatter(x=train_process['epoch'], y=train_process['val_acc'],
                                 mode='lines+markers', name='Val Accuracy'), row=1, col=2)

        fig.update_layout(title_text=plot_name, height=600, width=1000)
        fig.show()

    def test(self, model, test_loader, config: TestConfig):
        """
        测试模型
        """
        if config.clear_log_file:
            try:
                os.remove('test_log.jsonl')
            except FileNotFoundError:
                pass
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if config.load_model_path is not None:
            try:
                model.load_state_dict(torch.load(config.load_model_path, map_location=device, weights_only=True))
            except FileNotFoundError:
                self.logger.error(f"模型文件未找到: {config.load_model_path}")
                return

        model.to(device)
        model.eval()

        test_acc, test_num, error_num = 0, 0, 0
        debug_outputs = []  # 用于收集调试输出的列表

        with torch.no_grad():
            for i, (dx, dy) in enumerate(tqdm(test_loader, desc="Testing")):
                dx, dy = dx.to(device), dy.to(device)
                output = model(dx)
                pred, real_label = self.predict_label_func(output, dy)

                if isinstance(pred, torch.Tensor) and pred.dim() > 1:
                    self.acc_func(pred, real_label) if self.acc_func is not None else self.__default_acc_func(
                        pred, real_label, config.row_compare)
                    test_num += dx.size(0) * (pred.size(1) if not config.row_compare else 1)
                else:
                    test_acc += torch.sum(pred == real_label).item()
                    test_num += dx.size(0)

                if config.debug and i < config.debug_num:
                    error_num = self._debug_output(pred, real_label, config.classes, error_num, debug_outputs)

        # 输出收集的调试信息
        for output in debug_outputs:
            if output.startswith(Fore.RED):
                self.logger.error(output)
            else:
                self.logger.info(output)

        if config.debug:
            self.logger.info(f"检测数量: {config.debug_num}，错误数量: {error_num}")

        results = {
            "test_accuracy": test_acc / test_num,
            "total_samples": test_num,
            "correct_predictions": test_acc
        }
        self.save_config_and_results(config, results, 'test_log.jsonl', sort=config.sort_log_by_test_acc)

        self.logger.info(f'Test Total Accuracy: {results["test_accuracy"] * 100:.2f}%')

    def _debug_output(self, pred, real_label, classes, error_num, debug_outputs):
        """
        收集调试信息
        """
        if isinstance(pred, torch.Tensor) and pred.dim() > 1:
            for p, r in zip(pred, real_label):
                if torch.all(p == r):
                    debug_outputs.append(f"真实值: {r.tolist()} ------- 预测值: {p.tolist()}")
                else:
                    error_num += 1
                    debug_outputs.append(
                        f"{Fore.RED}真实值: {r.tolist()} ------- 预测值: {p.tolist()}{Style.RESET_ALL}")
        else:
            if classes is None:
                if pred.item() != real_label.item():
                    error_num += 1
                    debug_outputs.append(
                        f"{Fore.RED}真实值: {real_label.item()} ------- 预测值: {pred.item()}{Style.RESET_ALL}")
                else:
                    debug_outputs.append(f"真实值: {real_label.item()} ------- 预测值: {pred.item()}")
            else:
                if pred.item() != real_label.item():
                    error_num += 1
                    debug_outputs.append(
                        f"{Fore.RED}真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}{Style.RESET_ALL}")
                else:
                    debug_outputs.append(f"真实值: {classes[real_label.item()]} ------- 预测值: {classes[pred.item()]}")

        return error_num

    def print_model_summary(self, model, input_size):
        """
        打印模型摘要
        """
        summary(model, input_size)


if __name__ == '__main__':
    # 使用示例
    train_config = TrainConfig()
    test_config = TestConfig()

    # 创建一个简单的模型
    model = nn.Sequential(
        nn.Linear(10, 20),
        nn.ReLU(),
        nn.Linear(20, 2)
    )

    # 创建一些虚拟数据
    train_data = torch.randn(100, 10)
    train_labels = torch.randint(0, 2, (100,))
    train_dataset = torch.utils.data.TensorDataset(train_data, train_labels)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32)

    test_data = torch.randn(50, 10)
    test_labels = torch.randint(0, 2, (50,))
    test_dataset = torch.utils.data.TensorDataset(test_data, test_labels)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32)

    # 创建TrainTestUtils实例
    utils = TrainTestUtils()

    # 训练模型
    best_model_wts, train_process = utils.train(model, train_loader, test_loader, train_config)

    # 保存最佳模型
    utils.save_best_model(best_model_wts, 'best_model.pth')

    # 绘制训练过程
    utils.plot_train_process(train_process)

    # 测试模型
    utils.test(model, test_loader, test_config)

    # 打印模型摘要
    utils.print_model_summary(model, (10,))
