import copy
import json
import re
from typing import Dict, Any, Union, List


# JSON 处理功能类
class JSONUtils:

    @staticmethod
    def to_json(data: Any, pretty: bool = True) -> Union[str, bool]:
        """
        将数据转换为 JSON 字符串，支持是否格式化输出。

        示例:
        >>> data = {"name": "Alice", "age": 30}
        >>> json_str = to_json(data, pretty=True)
        >>> print(json_str)
        {
            "name": "Alice",
            "age": 30
        }

        >>> json_str = to_json(data, pretty=False)
        >>> print(json_str)
        {"name": "Alice","age": 30}

        :param data: 要转换的数据，可以是字典、列表等类型。
        :param pretty: 是否格式化输出。
        :return: 返回 JSON 格式的字符串，如果 `data` 不是字典或列表，则返回 False。

        注意: 若 `data` 不是字典或列表类型，方法将会返回 False。
        """
        if not isinstance(data, (dict, list)):
            return False
        return json.dumps(data, ensure_ascii = False, indent = 4 if pretty else None)

    @staticmethod
    def from_json(json_str: str) -> Any:
        """
        将 JSON 字符串解析为 Python 对象。

        示例:
        >>> json_str = '{"name": "Alice", "age": 30}'
        >>> data = from_json(json_str)
        >>> print(data)
        {'name': 'Alice', 'age': 30}

        :param json_str: JSON 格式的字符串。
        :return: 转换后的 Python 对象。     
        """
        return json.loads(json_str)

    @staticmethod
    def write_json(file_path: str, data: Any, pretty: bool = True) -> bool:
        """
        将 Python 数据写入 JSON 文件。

        示例:
        >>> data = {"name": "Alice", "age": 30}
        >>> success = write_json("data.json", data, pretty=True)
        >>> print(success)
        True

        :param file_path: 文件路径。
        :param data: 要写入的数据，通常是字典或列表。
        :param pretty: 是否格式化输出。
        :return: 是否成功写入文件。

        注意: 若 `data` 不是字典或者列表类型，方法将会返回 False。
        """
        if not isinstance(data, (dict, list)):
            return False

        try:
            with open(file_path, 'w', encoding = 'utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 4 if pretty else None)
            return True
        except Exception:
            return False

    @staticmethod
    def read_json(file_path: str) -> Union[Any, bool]:
        """
        从 JSON 文件读取数据并返回 Python 对象。

        示例:
        >>> data = read_json("data.json")
        >>> print(data)
        {'name': 'Alice', 'age': 30}

        :param file_path: 文件路径。
        :return: 读取的 JSON 数据，或失败时返回 False。
        """
        try:
            with open(file_path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            if isinstance(data, (dict, list)):  # 确保读取到的是字典或列表
                return data
            else:
                return False
        except Exception:
            return False

    @staticmethod
    def validate_json(json_str: str) -> bool:
        """
        校验给定的字符串是否为有效的 JSON 格式。

        示例:
        >>> json_str = '{"name": "Alice", "age": 30}'
        >>> is_valid = validate_json(json_str)
        >>> print(is_valid)
        True

        :param json_str: JSON 格式的字符串。
        :return: 如果是有效的 JSON 格式返回 True，否则返回 False。
        """
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def merge_json(json1: Dict[str, Any], json2: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并两个 JSON 数据。

        示例:
        >>> json1 = {"name": "Alice"}
        >>> json2 = {"age": 30}
        >>> merged = merge_json(json1, json2)
        >>> print(merged)
        {'name': 'Alice', 'age': 30}

        :param json1: 第一个 JSON 数据（字典）。
        :param json2: 第二个 JSON 数据（字典）。
        :return: 合并后的字典。

        注意: 若 `json1` 或 `json2` 不是字典类型，方法将会返回 False。
        """
        if not isinstance(json1, dict) or not isinstance(json2, dict):
            return False

        merged = copy.deepcopy(json1)  # 确保是深拷贝
        merged.update(json2)
        return merged

    @staticmethod
    def deep_copy_json(json_data: Any) -> Any:
        """
        返回给定 JSON 数据的深拷贝。

        示例:
        >>> data = {"name": "Alice", "age": 30}
        >>> copied_data = deep_copy_json(data)
        >>> print(copied_data)
        {'name': 'Alice', 'age': 30}

        :param json_data: 需要拷贝的 JSON 数据。
        :return: 深拷贝的 JSON 数据。

        注意: 若 `json_data` 不是字典或列表类型，方法将会返回 False。
        """
        if not isinstance(json_data, (dict, list)):
            return False

        return copy.deepcopy(json_data)

    @staticmethod
    def pretty_print_json(json_str: str) -> None:
        """
        以格式化的方式打印 JSON 字符串。

        示例:
        >>> json_str = '{"name": "Alice", "age": 30}'
        >>> pretty_print_json(json_str)
        {
            "name": "Alice",
            "age": 30
        }

        :param json_str: 要打印的 JSON 字符串。
        """
        data = JSONUtils.from_json(json_str)
        print(JSONUtils.to_json(data, pretty = True))

    @staticmethod
    def get_json_keys(json_data: Dict[str, Any]) -> List[str]:
        """
        获取 JSON 数据中的所有键。

        示例:
        >>> data = {"name": "Alice", "age": 30}
        >>> keys = get_json_keys(data)
        >>> print(keys)
        ['name', 'age']

        :param json_data: 要提取键的 JSON 数据（字典）。
        :return: 所有键的列表。
        """
        if not isinstance(json_data, dict):
            raise ValueError("Input data must be a dictionary.")
        return list(json_data.keys())

    @staticmethod
    def get_nested_key_paths(json_data: Dict[str, Any], target_key: str, path: List[str] = None) -> List[List[str]]:
        """
        获取指定键在嵌套 JSON 数据中的所有路径。

        示例:
        >>> data = {"person": {"name": "Alice", "address": {"city": "New York"}}}
        >>> paths = get_nested_key_paths(data, "name")
        >>> print(paths)
        [['person', 'name']]

        :param json_data: 要搜索的 JSON 数据（字典）。
        :param target_key: 目标键。
        :param path: 当前路径（递归使用）。
        :return: 键的路径列表，每个路径是一个列表。
        """
        if path is None:
            path = []

        paths = []
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                new_path = path + [key]
                if key == target_key:
                    paths.append(new_path)
                elif isinstance(value, dict):
                    paths.extend(JSONUtils.get_nested_key_paths(value, target_key, new_path))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            paths.extend(JSONUtils.get_nested_key_paths(item, target_key, new_path))
        return paths

    @staticmethod
    def get(json_data: Any, keys: List[str], default: Any = None) -> Any:
        """
        按路径获取嵌套 JSON 数据中的某个键值对。支持字典、列表和数组索引。

        示例:
        >>> data = {"person": {"name": "Alice", "addresses": [{"city": "New York"}, {"city": "Beijing"}]}}
        >>> value = get(data, ["person", "addresses", 1, "city"])
        >>> print(value)  # 输出：Beijing

        >>> data = {"user": {"profile": {"name": "Bob", "age": 30}}}
        >>> value = get(data, ["user", "profile", "name"])
        >>> print(value)  # 输出：Bob

        >>> data = {"items": [1, 2, 3, 4, 5]}
        >>> value = get(data, ["items", 2])
        >>> print(value)  # 输出：3

        >>> value = get(data, ["items", 10], default="Not Found")
        >>> print(value)  # 输出：Not Found

        :param json_data: 要查找的 JSON 数据。
        :param keys: 键的路径列表，逐层查找，支持索引。
        :param default: 如果路径中的键不存在，返回的默认值（默认为 None）。
        :return: 如果找到，返回键的值，否则返回默认值。
        """
        for key in keys:
            if isinstance(json_data, dict):
                json_data = json_data.get(key, default)
            elif isinstance(json_data, list):
                try:
                    json_data = json_data[int(key)]  # 转换为整数索引
                except (ValueError, IndexError):
                    return default
            else:
                return default
        return json_data

    def update(json_data: Any, keys: List[str], value: Any) -> bool:
        """
        按路径更新嵌套 JSON 数据中的某个键值对。支持字典和数组索引。

        示例:
        >>> data = {"person": {"name": "Alice", "address": {"city": "New York"}}}
        >>> result = update(data, ["person", "address", "city"], "Los Angeles")
        >>> print(result)  # 输出: True
        >>> print(data["person"]["address"]["city"])  # 输出: Los Angeles

        >>> data = {"person": {"name": "Alice", "addresses": [{"city": "New York"}, {"city": "Beijing"}]}}
        >>> result = update(data, ["person", "addresses", 1, "city"], "Shanghai")
        >>> print(result)  # 输出: True
        >>> print(data["person"]["addresses"][1]["city"])  # 输出: Shanghai

        :param json_data: 要更新的 JSON 数据。
        :param keys: 键的路径列表，逐层更新。
        :param value: 要更新的值。
        :return: 如果更新成功，返回 True；否则返回 False。
        """
        for segment in keys[:-1]:  # 遍历到倒数第二层
            if isinstance(json_data, dict):
                json_data = json_data.setdefault(segment, {})
            elif isinstance(json_data, list):
                try:
                    json_data = json_data[int(segment)]
                except (ValueError, IndexError):
                    return False  # 如果索引无效或超出范围，返回 False
            else:
                return False  # 如果路径无效，返回 False

        # 更新目标键
        if isinstance(json_data, dict):
            json_data[keys[-1]] = value
            return True
        elif isinstance(json_data, list):
            try:
                index = int(keys[-1])
                if index < len(json_data):  # 确保索引有效
                    json_data[index] = value
                    return True
                else:
                    return False  # 索引超出范围
            except (ValueError, IndexError):
                return False  # 如果无法转换为有效索引或索引无效
        else:
            return False  # 如果目标类型不是字典或列表，返回 False

    @staticmethod
    def delete(json_data: Any, keys: List[str]) -> bool:
        """
        按路径删除嵌套 JSON 数据中的某个键值对，支持字典和数组索引。

        示例:
        >>> data = {"person": {"name": "Alice", "address": {"city": "New York"}}}
        >>> result = delete(data, ["person", "address", "city"])
        >>> print(result)  # 输出: True
        >>> print(data["person"]["address"].get("city"))  # 输出: None

        >>> data = {"person": {"name": "Alice", "addresses": [{"city": "New York"}, {"city": "Beijing"}]}}
        >>> result = delete(data, ["person", "addresses", 1, "city"])
        >>> print(result)  # 输出: True
        >>> print(data["person"]["addresses"][1].get("city"))  # 输出: None

        :param json_data: 要删除键值对的 JSON 数据。
        :param keys: 键的路径列表，逐层删除。
        :return: 如果删除成功，返回 True；否则返回 False。
        """
        for segment in keys[:-1]:  # 遍历到倒数第二层
            if isinstance(json_data, dict):
                json_data = json_data.get(segment)
                if json_data is None:  # 如果路径中的某个键不存在，提前返回 False
                    return False
            elif isinstance(json_data, list):
                try:
                    json_data = json_data[int(segment)]
                except (ValueError, IndexError):
                    return False  # 如果索引无效或超出范围，返回 False
            else:
                return False  # 如果路径无效，返回 False

        # 删除目标键
        if isinstance(json_data, dict) and keys[-1] in json_data:
            del json_data[keys[-1]]
            return True
        elif isinstance(json_data, list):
            try:
                index = int(keys[-1])
                if 0 <= index < len(json_data):  # 确保索引有效
                    del json_data[index]
                    return True
            except (ValueError, IndexError):
                return False  # 如果无法转换为有效索引或索引无效
        return False  # 如果目标键不存在或不是字典/列表，返回 False

    @staticmethod
    def add_or_update(json_data: Any, keys: List[str], value: Any) -> bool:
        """
        按路径添加或更新值。如果路径中某些部分不存在，则创建它们。
        如果路径中的键已经存在，则更新该键的值。支持数组索引。

        示例:
        >>> data = {"person": {"name": "Alice", "address": {"city": "New York"}}}
        >>> result = add_or_update(data, ["person", "address", "zip"], "10001")
        >>> print(result)  # True
        >>> print(data["person"]["address"]["zip"])  # 10001

        >>> result = add_or_update(data, ["person", "address", "city"], "Los Angeles")
        >>> print(result)  # True
        >>> print(data["person"]["address"]["city"])  # Los Angeles

        >>> data = {"items": [1, 2, 3]}
        >>> result = add_or_update(data, ["items", 1], 5)
        >>> print(result)  # True
        >>> print(data["items"][1])  # 5

        :param json_data: 要更新的 JSON 数据。
        :param keys: 键的路径列表，逐层添加。
        :param value: 要添加或更新的值。
        :return: 如果键存在并成功更新，或者键不存在并成功添加返回 True，否则返回 False。

        注意: 如果路径中的数组索引越界，会自动扩展数组。
        """
        if not isinstance(json_data, dict):
            raise ValueError("json_data should be a dictionary")

        if not keys:
            return False

        current_data = json_data
        for segment in keys[:-1]:  # 遍历到倒数第二层
            if isinstance(segment, int):  # 如果是数组索引
                if not isinstance(current_data, list):
                    raise ValueError(f"Path segment '{segment}' is not an array.")
                if segment >= len(current_data):  # 如果索引超出范围
                    current_data.extend([None] * (segment + 1 - len(current_data)))  # 扩展数组
                current_data = current_data[segment]
            else:
                if not isinstance(current_data, dict):
                    raise ValueError(f"Path segment '{segment}' is not a dictionary.")
                if current_data.get(segment) is None:
                    current_data[segment] = {}  # 如果当前部分是 None，则初始化为字典
                current_data = current_data[segment]  # 继续下一层

        # 到达最后一层，添加或更新值
        last_key = keys[-1]
        if isinstance(last_key, int):  # 如果是数组索引
            if not isinstance(current_data, list):
                raise ValueError(f"Path segment '{last_key}' is not an array.")
            if last_key >= len(current_data):  # 如果索引超出范围
                current_data.extend([None] * (last_key + 1 - len(current_data)))  # 扩展数组
            current_data[last_key] = value
        else:  # 否则更新字典中的值
            current_data[last_key] = value

        return True

    @staticmethod
    def change_key_name(json_data: Any, keys: List[str], new_key: str) -> bool:
        """
        按路径更改嵌套 JSON 数据中的某个键名，支持字典和数组索引。
        如果新的键名已经存在，则跳过修改。

        示例:
        >>> data = {"person": {"name": "Alice", "address": {"city": "New York"}}}
        >>> result = change_key_name(data, ["person", "address"], "location")
        >>> print(result)  # 输出: True
        >>> print(data["person"]["location"])  # 输出: {"city": "New York"}

        >>> data = {"person": {"name": "Alice", "addresses": [{"city": "New York"}, {"city": "Beijing"}]}}
        >>> result = change_key_name(data, ["person", "addresses", 1], "location")
        >>> print(result)  # 输出: True
        >>> print(data["person"]["addresses"][1]["location"])  # 输出: {"city": "Beijing"}

        :param json_data: 要修改键名的 JSON 数据。
        :param keys: 键的路径列表，逐层定位到需要更改的键。
        :param new_key: 新的键名。
        :return: 如果修改成功，返回 True；否则返回 False。
        """
        for segment in keys[:-1]:  # 遍历到倒数第二层
            if isinstance(json_data, dict):
                json_data = json_data.get(segment)
                if json_data is None:  # 如果路径中的某个键不存在，提前返回 False
                    return False
            elif isinstance(json_data, list):
                try:
                    json_data = json_data[int(segment)]
                except (ValueError, IndexError):
                    return False  # 如果索引无效或超出范围，返回 False
            else:
                return False  # 如果路径无效，返回 False

        # 处理最后一层，修改键名
        if isinstance(json_data, dict) and keys[-1] in json_data:
            # 如果目标位置的键名已存在，则跳过
            if new_key in json_data:
                return False  # 如果新键名已存在，返回 False，表示未修改
            # 获取旧键名的值，并删除旧键
            json_data[new_key] = json_data.pop(keys[-1])
            return True
        elif isinstance(json_data, list):
            try:
                index = int(keys[-1])
                if 0 <= index < len(json_data):  # 确保索引有效
                    # 如果是字典，修改字典中的键名
                    if isinstance(json_data[index], dict):
                        # 如果目标字典已有新键名，则跳过
                        if new_key in json_data[index]:
                            return False
                        json_data[index][new_key] = json_data[index].pop(keys[-1])
                        return True
            except (ValueError, IndexError):
                return False  # 如果无法转换为有效索引或索引无效
        return False  # 如果目标键不存在或不是字典/列表，返回 False

    @staticmethod
    def fill_missing_keys_non_recursive(default_config, json_data):
        """
        检查 json_data 中缺失的键，并补充默认值。

        功能描述:
        - 遍历默认配置字典（default_config）和目标 JSON 数据（json_data），检查目标数据中是否缺少某些键。
        - 如果缺少某个键，则使用默认配置中的值来填充。
        - 采用栈结构，以非递归的方式处理嵌套字典和列表。

        使用场景:
        - 用于确保目标 JSON 数据包含所有默认配置的键，尤其适用于需要合并默认配置与用户提供的数据的场景。
        - 适用于深度嵌套的字典和列表配置。

        示例:
        >>> default_config = {"key1": "value1", "key2": {"nested_key": "default"}, "key3": []}
        >>> json_data = {"key2": {"nested_key": "existing_value"}}
        >>> fill_missing_keys_non_recursive(default_config, json_data)
        # json_data 会变为 {"key1": "value1", "key2": {"nested_key": "existing_value"}, "key3": []}

        注意事项:
        - 默认配置中的字典会自动填充到目标数据中。
        - 如果目标数据中已有该键且值为字典或列表，则会继续处理其嵌套结构。

        :param default_config: 默认配置字典（DEFAULT_CONFIG），包含所需的键及其默认值。
        :param json_data: 要检查并填充的 JSON 数据。
        """
        stack = [(default_config, json_data)]  # 初始化栈，包含默认配置和待检查的数据

        while stack:
            # 弹出栈顶元素
            default_dict, current_dict = stack.pop()

            for key, default_value in default_dict.items():
                if key not in current_dict:
                    # 如果当前字典缺少某个键，填充默认值
                    current_dict[key] = default_value
                elif isinstance(default_value, dict):
                    # 如果默认值是字典，添加到栈中，进行嵌套字典的处理
                    if key not in current_dict:
                        current_dict[key] = {}
                    stack.append((default_value, current_dict[key]))
                elif isinstance(default_value, list):
                    # 如果默认值是列表，初始化为空列表（可以根据需求填充）
                    if key not in current_dict:
                        current_dict[key] = []

    @staticmethod
    def get_filtered_data(
        data: List[Dict[str, Any]], target_keys: List[str], filters: Dict[str, Union[str, List[Any], Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        从字典列表中提取指定键值，并根据多个条件进行筛选。

        支持条件：'eq'（等于）、'gt'（大于）、'lt'（小于）、'in'（包含）、'regex'（正则表达式）

        示例:
        >>> data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
        >>> target_keys = ["name", "age"]
        >>> filters = {"name": {"eq": "Bob"}, "age": {"gt": 25}}
        >>> result = get_filtered_data(data, target_keys, filters)
        >>> print(result)
        [{'name': 'Bob', 'age': 25}]

        :param data: 包含字典的列表
        :param target_keys: 目标键的列表
        :param filters: 筛选条件字典，支持多个条件
        :return: 提取的字典列表
        :raises ValueError: 如果输入数据格式不正确，抛出错误
        :raises TypeError: 如果参数类型不匹配，抛出错误
        """
        if not isinstance(data, list):
            raise TypeError("The 'data' parameter must be a list.")

        if not all(isinstance(item, dict) for item in data):
            raise ValueError("All elements in 'data' must be dictionaries.")

        if not isinstance(target_keys, list):
            raise TypeError("The 'target_keys' parameter must be a list.")

        if not all(isinstance(key, str) for key in target_keys):
            raise ValueError("All elements in 'target_keys' must be strings.")

        # 如果没有传入 filters，默认是空字典
        filters = filters or {}

        def _apply_filter(value: Any, filter_value: Dict[str, Any]) -> bool:
            """
            应用单个过滤条件，支持多个操作符：'eq', 'gt', 'lt', 'in', 'regex'
            """
            if isinstance(filter_value, dict):
                for operator, filter_param in filter_value.items():
                    if operator == "eq":
                        if value != filter_param:
                            return False
                    elif operator == "gt":
                        if not isinstance(value, (int, float)) or value <= filter_param:
                            return False
                    elif operator == "lt":
                        if not isinstance(value, (int, float)) or value >= filter_param:
                            return False
                    elif operator == "in":
                        if value not in filter_param:
                            return False
                    elif operator == "regex":
                        if not isinstance(value, str) or not re.match(filter_param, value):
                            return False
                    else:
                        raise ValueError(f"Unsupported filter operator: {operator}")
            else:
                raise ValueError("Filter must be a dictionary with operator keys (eq, gt, lt, etc.).")

            return True

        filtered_data = []
        for item in data:
            # 对每个字典进行筛选
            if all(_apply_filter(item.get(key), filter_value) for key, filter_value in filters.items()):
                # 提取目标键值
                filtered_item = {key: item.get(key, None) for key in target_keys}
                filtered_data.append(filtered_item)

        return filtered_data


__all__ = ['JSONUtils']
