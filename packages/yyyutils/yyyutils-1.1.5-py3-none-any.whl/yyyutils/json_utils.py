import json
from typing import Any, Dict, List, Optional, Tuple


class JSONUtils:
    """
    用于处理 JSON 数据的工具类
    """

    def __init__(self, file_path: str, cls: json.JSONEncoder = None):
        self.file_path = file_path
        self.cls = cls

    def _read_json(self) -> Dict[str, Any]:
        """读取 JSON 文件并返回解析后的数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"读取 JSON 文件时出错: {e}")
            return {}

    def write_json(self, data: Dict[str, Any]) -> None:
        """写入 JSON 文件"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, cls=self.cls, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"写入 JSON 文件时出错: {e}")

    def update_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新 JSON 文件，将 data 中的键值对更新到原 JSON 文件中"""
        old_data = self._read_json()
        old_data.update(data)
        self.write_json(old_data)
        return old_data

    def get_value(self, key: str) -> Optional[Any]:
        """获取 JSON 文件中指定 key 的值"""
        data = self._read_json()
        return data.get(key)

    def set_value(self, key: str, value: Any) -> Dict[str, Any]:
        """设置 JSON 文件中指定 key 的值"""
        data = self._read_json()
        data[key] = value
        self.write_json(data)
        return data

    def delete_key(self, key: str) -> Dict[str, Any]:
        """删除 JSON 文件中指定 key"""
        data = self._read_json()
        if key in data:
            del data[key]
            self.write_json(data)
        return data

    def get_keys(self) -> List[str]:
        """获取 JSON 文件中所有 key"""
        data = self._read_json()
        return list(data.keys())

    def get_values(self) -> List[Any]:
        """获取 JSON 文件中所有 value"""
        data = self._read_json()
        return list(data.values())

    def get_items(self) -> List[Tuple[str, Any]]:
        """获取 JSON 文件中所有键值对"""
        data = self._read_json()
        return list(data.items())

    def get_json_str(self) -> str:
        """获取 JSON 文件内容的字符串形式"""
        data = self._read_json()
        return json.dumps(data, ensure_ascii=False, indent=4)
