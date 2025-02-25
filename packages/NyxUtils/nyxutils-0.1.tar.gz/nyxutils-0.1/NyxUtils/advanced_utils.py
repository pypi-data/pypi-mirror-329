import csv
import html
import time
from typing import List, Dict, Any


# 高级实用功能类
class AdvancedUtils:

    @staticmethod
    def word_frequency(text: str) -> Dict[str, int]:
        """
        统计文本中每个单词出现的频率（忽略标点和大小写）。

        该方法将输入的文本分词，并统计每个单词出现的次数。所有单词都会转换为小写并去除标点符号。

        示例:
        >>> text = "hello world hello"
        >>> freq = AdvancedUtils.word_frequency(text)
        >>> print(freq)
        {'hello': 2, 'world': 1}

        :param text: 要分析的文本
        :return: 每个单词的出现频率字典
        """
        words = text.split()  # 将文本分割为单词
        frequency = {}  # 存储单词频率的字典
        for word in words:
            word = word.lower().strip(",.?!\"'")  # 小写并去除标点符号
            frequency[word] = frequency.get(word, 0) + 1  # 更新频率
        return frequency

    @staticmethod
    def escape_html(text: str) -> str:
        """
        将文本中的特殊字符转换为 HTML 实体。

        该方法会将文本中的 HTML 特殊字符（如 "<", ">", "&" 等）转义为 HTML 实体，
        以便安全地在网页中显示。

        示例:
        >>> html = "<div>Example</div>"
        >>> escaped = AdvancedUtils.escape_html(html)
        >>> print(escaped)
        &lt;div&gt;Example&lt;/div&gt;

        :param text: 要转义的文本
        :return: 转义后的 HTML 字符串
        """
        return html.escape(text)  # 转义 HTML 特殊字符

    @staticmethod
    def write_to_csv(file_path: str, data: List[Dict[str, Any]], headers: List[str]) -> None:
        """
        将列表数据写入 CSV 文件。

        该方法将给定的数据列表（每项为字典）写入指定路径的 CSV 文件，并且写入表头。

        示例:
        >>> data = [{'Name': 'Alice', 'Age': 30}, {'Name': 'Bob', 'Age': 25}]
        >>> headers = ['Name', 'Age']
        >>> AdvancedUtils.write_to_csv('example.csv', data, headers)

        :param file_path: CSV 文件路径
        :param data: 要写入的数据列表，每项是一个字典
        :param headers: CSV 文件的表头
        """
        with open(file_path, mode = 'w', newline = '', encoding = 'utf-8') as file:
            writer = csv.DictWriter(file, fieldnames = headers)  # 创建 CSV 写入器
            writer.writeheader()  # 写入表头
            writer.writerows(data)  # 写入数据行

    @staticmethod
    def read_from_csv(file_path: str) -> List[Dict[str, str]]:
        """
        从 CSV 文件中读取数据并返回一个字典列表。

        该方法从给定的 CSV 文件中读取数据，并将每一行数据转换为字典形式返回。

        示例:
        >>> data = AdvancedUtils.read_from_csv('example.csv')
        >>> print(data)
        [{'Name': 'Alice', 'Age': '30'}, {'Name': 'Bob', 'Age': '25'}]

        :param file_path: CSV 文件路径
        :return: 包含 CSV 数据的字典列表
        """
        with open(file_path, mode = 'r', encoding = 'utf-8') as file:
            reader = csv.DictReader(file)  # 创建 CSV 读取器
            return [row for row in reader]  # 返回字典列表

    @staticmethod
    def time_execution(func, *args, **kwargs) -> float:
        """
        测量一个函数执行的时间并返回执行时间。

        该方法会在执行指定的函数之前记录开始时间，执行后记录结束时间，并返回函数执行所消耗的时间。

        示例:
        >>> def sample_function(x): return x ** 2
        >>> exec_time = AdvancedUtils.time_execution(sample_function, 10)
        >>> print(f"Execution time: {exec_time:.6f} seconds")

        :param func: 要执行的函数
        :param args: 函数的参数
        :param kwargs: 函数的关键字参数
        :return: 执行时间（秒）
        """
        start_time = time.time()  # 记录开始时间
        func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录结束时间
        return end_time - start_time  # 返回函数执行的时间差


__all__ = ['AdvancedUtils']
