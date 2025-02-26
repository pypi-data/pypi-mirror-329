# -*- coding:utf-8 -*-
"""
@Created on : 2023/6/11 19:33
@Author: XDTEAM
@Des: 一个简单的 JSON 元数据管理器，用于读取、写入和操作 JSON 文件。
"""
from pathlib import Path
import json


class MetadataManager:

    def __init__(self, cache_dir: str = 'cache_path'):
        """
        初始化MetadataManager对象，并创建缓存目录。

        :param cache_dir: 缓存目录的名称，默认为当前目录下的'cache_path'。
        """
        self.cache_path = Path.cwd() / cache_dir
        self.cache_path.mkdir(exist_ok=True)

    def _load_json(self, file_name: str) -> dict:
        """
        加载指定文件名的JSON文件，并返回解析后的字典。

        :param file_name: 不包含扩展名的文件名。
        :return: 解析后的字典，如果文件不存在则返回空字典。
        """
        file_path = self.cache_path / f'{file_name}.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def _save_json(self, file_name: str, data: dict):
        """
        将字典保存到指定文件名的JSON文件中。

        :param file_name: 不包含扩展名的文件名。
        :param data: 要保存的字典数据。
        """
        file_path = self.cache_path / f'{file_name}.json'
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=7)

    def read(self, file_name: str, *keys) -> dict or None:
        """
        读取JSON文件中的数据，并根据提供的多个键依次访问嵌套的数据。

        :param file_name: 不包含扩展名的文件名。
        :param keys: 可变长度的键列表，用于依次访问嵌套的数据。
        :return: 返回最终找到的值或None（如果任何键不存在），如果未提供键则返回整个字典。
        """
        data = self._load_json(file_name)

        # 如果没有提供额外的键，直接返回加载的数据
        if not keys:
            return data

        try:
            for key in keys:
                data = data[key]
            return data
        except (KeyError, TypeError):  # KeyError是当键不存在时抛出的异常，TypeError是当尝试索引非映射对象时抛出的异常
            return None

    def delete(self, file_name: str, *keys) -> bool:
        """
        删除JSON文件中指定嵌套键的值。

        :param file_name: 不包含扩展名的文件名。
        :param keys: 可变长度的键列表，用于指定要删除的嵌套键路径。
        :return: 操作成功返回True，失败返回False。
        """
        data = self._load_json(file_name)

        # 如果没有提供键，直接返回False，因为不知道要删除什么
        if not keys:
            return False

        # 创建一个指向data的可变引用，以便在嵌套结构中移动
        current_level = data

        # 遍历所有提供的键，除了最后一个，为它们创建必要的嵌套层级
        for key in keys[:-1]:
            if key in current_level and isinstance(current_level[key], dict):
                current_level = current_level[key]
            else:
                # 如果任何一个中间键不存在或不是字典类型，则无法继续，返回False
                return False

        # 尝试从最内层的字典中删除最终的键
        final_key = keys[-1]
        if final_key in current_level:
            del current_level[final_key]
            self._save_json(file_name, data)
            return True

        # 如果最终的键不存在，则返回False
        return False

    def add(self, file_name: str, *keys, value, unique: bool = False) -> bool:
        """
        添加或更新指定嵌套键的值。

        :param file_name: 不包含扩展名的文件名。
        :param keys: 可变长度的键列表，用于指定要添加或更新的嵌套键路径。
        :param value: 要设置的值。
        :param unique: 值是否唯一，默认为False。如果unique为True则不添加重复项。
        :return: 操作成功返回True。
        """
        data = self._load_json(file_name)
        # 创建一个指向data的可变引用，以便在嵌套结构中移动
        current_level = data

        # 遍历所有提供的键，除了最后一个，为它们创建必要的嵌套层级
        for key in keys[:-1]:
            if key not in current_level or not isinstance(current_level[key], dict):
                current_level[key] = {}
            current_level = current_level[key]

        # 在最内层的键上设置值
        final_key = keys[-1]

        # 如果 unique 为 True，检查值是否已经存在
        if unique:
            if final_key in current_level and current_level[final_key] == value:
                return False  # 已存在，不添加

        # 设置值
        current_level[final_key] = value

        # 保存更新后的数据到文件
        self._save_json(file_name, data)
        return True

    def add_to_list(self, file_name: str, *keys, value, unique: bool = False) -> bool:
        """
        向指定键的列表中添加元素。

        :param file_name: 不包含扩展名的文件名。
        :param keys: 可变长度的键列表，用于指定要添加元素的嵌套键路径。
        :param value: 要添加的元素。
        :param unique: 值是否唯一，默认为False。如果unique为True则不添加重复项。
        :return: 如果成功添加或已经存在（当unique为True）则返回True，否则返回False。
        """
        data = self._load_json(file_name)

        # 创建一个指向data的可变引用，以便在嵌套结构中移动
        current_level = data

        # 遍历所有提供的键，除了最后一个，为它们创建必要的嵌套层级
        for key in keys[:-1]:
            if key not in current_level or not isinstance(current_level[key], dict):
                current_level[key] = {}
            current_level = current_level[key]

        # 最后一个键是目标列表的键
        final_key = keys[-1]

        # 确保目标键存在并且是一个列表
        if final_key not in current_level:
            current_level[final_key] = []

        if unique:
            # 检查值的唯一性
            existing_values = current_level[final_key]

            # 如果value是字典，转换为字符串以便进行比较
            if isinstance(value, dict):
                value_to_check = str(value)  # 或者使用其他方法来序列化字典
                existing_values_as_set = {str(v) for v in existing_values if isinstance(v, dict)}
            else:
                value_to_check = value
                existing_values_as_set = set(existing_values)

            if value_to_check in existing_values_as_set:
                return False  # 已存在，不添加

        # 添加元素
        current_level[final_key].append(value)
        self._save_json(file_name, data)
        return True

    def remove_from_list(self, file_name: str, *keys, value) -> bool:
        """
        从指定键的列表中移除元素。

        :param file_name: 不包含扩展名的文件名。
        :param keys: 可变长度的键列表，用于指定要移除元素的嵌套键路径。
        :param value: 要移除的元素。
        :return: 如果成功移除则返回True，否则返回False。
        """
        data = self._load_json(file_name)

        # 创建一个指向data的可变引用，以便在嵌套结构中移动
        current_level = data

        # 遍历所有提供的键，找到目标列表的层级
        for key in keys[:-1]:
            if key in current_level and isinstance(current_level[key], dict):
                current_level = current_level[key]
            else:
                return False  # 如果任何一个中间键不存在或不是字典类型，则返回False

        # 最后一个键是目标列表的键
        final_key = keys[-1]

        # 确保目标键存在并且是一个列表
        if final_key in current_level and isinstance(current_level[final_key], list):
            if value in current_level[final_key]:
                current_level[final_key].remove(value)
                self._save_json(file_name, data)
                return True  # 成功移除
        return False  # 未找到元素或目标键不存在
