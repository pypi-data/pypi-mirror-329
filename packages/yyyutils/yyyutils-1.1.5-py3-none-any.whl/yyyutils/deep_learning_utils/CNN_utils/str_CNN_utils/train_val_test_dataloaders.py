from dataclasses import dataclass
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
import torch
import numpy as np
from collections import abc as container_abcs
import re


@dataclass
class DataLoadersConfig:
    train_rate: float = 0.8
    val_rate: float = 0.1
    test_rate: float = 0.1
    batch_size: int = 32
    shuffle: bool = True
    num_workers: int = 0
    exchange_dim: tuple = None
    pad: bool = True


class DataUtils:
    def __init__(self):
        self.__collate_fn = self.collate_fn

    @staticmethod
    def __default_collate_fn(batch, pad=False, exchange_dim=None):
        elem = batch[0]
        elem_type = type(elem)

        if isinstance(elem, torch.Tensor):
            try:
                return torch.stack(batch, 0)
            except RuntimeError as e:
                print(f"Error stacking tensors: {e}")
                print(f"Tensor shapes: {[t.shape for t in batch]}")
                raise
        elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
                and elem_type.__name__ != 'string_':
            if elem_type.__name__ == 'ndarray' or elem_type.__name__ == 'memmap':
                if np.dtype(elem.dtype).kind in ['U', 'S']:
                    raise TypeError("Numpy arrays with string dtypes are not supported.")
                return DataUtils.__default_collate_fn([torch.as_tensor(b) for b in batch], pad, exchange_dim)
            elif elem.shape == ():  # scalars
                return torch.as_tensor(batch)
        elif isinstance(elem, float):
            return torch.tensor(batch, dtype=torch.float64)
        elif isinstance(elem, int):
            return torch.tensor(batch)
        elif isinstance(elem, str):
            return batch
        elif isinstance(elem, container_abcs.Mapping):
            return {key: DataUtils.__default_collate_fn([d[key] for d in batch], pad, exchange_dim) for key in elem}
        elif isinstance(elem, tuple) and hasattr(elem, '_fields'):  # namedtuple
            return elem_type(*(DataUtils.__default_collate_fn(samples, pad, exchange_dim) for samples in zip(*batch)))
        elif isinstance(elem, container_abcs.Sequence):
            it = iter(batch)
            elem_size = len(next(it))
            if not all(len(elem) == elem_size for elem in it):
                raise RuntimeError('each element in list of batch should be of equal size')
            transposed = list(zip(*batch))
            return [DataUtils.__default_collate_fn(samples, pad, exchange_dim) for samples in transposed]

        raise TypeError(f'Default collate function does not support {elem_type}')

    @staticmethod
    def process_batch(batch, pad, exchange_dim):
        if isinstance(batch, torch.Tensor):
            if pad:
                batch = pad_sequence([b for b in batch], batch_first=True)
            if exchange_dim is not None:
                batch = batch.permute(exchange_dim)
        return batch

    @staticmethod
    def collate_fn(batch, pad=False, exchange_dim=None):
        result = DataUtils.__default_collate_fn(batch, pad, exchange_dim)
        return DataUtils.process_batch(result, pad, exchange_dim)

    def train_val_test_dataloaders(self, dataset: Dataset, config: DataLoadersConfig, collate_fn=None):
        """
        构建训练集、验证集、测试集的DataLoader
        :param dataset: 输入数据集
        :param config: DataLoadersConfig 配置对象
        :param collate_fn: 可选的自定义 collate_fn 函数
        :return: 训练集、验证集、测试集的 DataLoader
        """
        if collate_fn is not None:
            self.__collate_fn = collate_fn

        # 确保数据集划分的比例总和为1
        assert abs(config.train_rate + config.val_rate + config.test_rate - 1.0) < 1e-6, \
            "The sum of train_rate, val_rate, and test_rate must be 1.0"

        # 划分数据集
        data_size = len(dataset)
        train_size = int(data_size * config.train_rate)
        val_size = int(data_size * config.val_rate)
        test_size = data_size - train_size - val_size

        train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
            dataset, [train_size, val_size, test_size])

        # 构建数据加载器
        train_loader = DataLoader(
            train_dataset,
            batch_size=config.batch_size,
            num_workers=config.num_workers,
            collate_fn=lambda batch: self.__collate_fn(batch, config.pad, config.exchange_dim),
            shuffle=config.shuffle
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=config.batch_size,
            num_workers=config.num_workers,
            collate_fn=lambda batch: self.__collate_fn(batch, config.pad, config.exchange_dim),
            shuffle=config.shuffle
        ) if val_size > 0 else None

        test_loader = DataLoader(
            test_dataset,
            batch_size=config.batch_size,
            num_workers=config.num_workers,
            collate_fn=lambda batch: self.__collate_fn(batch, config.pad, config.exchange_dim)
        ) if test_size > 0 else None

        return train_loader, val_loader, test_loader
