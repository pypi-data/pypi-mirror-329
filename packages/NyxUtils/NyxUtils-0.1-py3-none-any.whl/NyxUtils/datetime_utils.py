import time
import math
from datetime import datetime, timedelta


# 日期操作类
class DateTimeUtils:

    @staticmethod
    def current_timestamp() -> int:
        """
        获取当前时间的时间戳。

        该方法返回当前时间的时间戳，它是从 1970年1月1日 00:00:00 UTC 起经过的秒数。时间戳通常用于表示时间并进行时间运算。

        示例:
        >>> print(DateUtils.current_timestamp())
        1672444800

        :return: 当前时间的时间戳
        """
        return int(time.time())

    @staticmethod
    def format_timestamp(timestamp: int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        将时间戳格式化为指定格式的日期时间字符串。

        该方法接收一个时间戳，并将其转换为一个按照指定格式输出的日期时间字符串。
        默认格式为 "%Y-%m-%d %H:%M:%S"，例如：2023-01-01 00:00:00。

        示例:
        >>> print(DateUtils.format_timestamp(1672444800))
        2023-01-01 00:00:00

        :param timestamp: 时间戳
        :param fmt: 格式化的日期时间字符串格式（默认为 "%Y-%m-%d %H:%M:%S"）
        :return: 格式化后的日期时间字符串
        """
        return time.strftime(fmt, time.localtime(timestamp))

    @staticmethod
    def add_days_to_date(date: str, days: int, fmt: str = "%Y-%m-%d") -> str:
        """
        给指定的日期加上指定的天数。

        该方法将指定的日期加上一个指定的天数，并返回结果日期。日期格式默认为 "%Y-%m-%d"。
        
        示例:
        >>> new_date = DateUtils.add_days_to_date("2023-01-01", 5)
        >>> print(new_date)
        2023-01-06

        :param date: 原始日期（格式：YYYY-MM-DD）
        :param days: 要加上的天数
        :param fmt: 返回日期的格式（默认为 "%Y-%m-%d"）
        :return: 增加天数后的日期字符串
        """
        d = datetime.strptime(date, fmt)  # 解析输入的日期
        return (d + timedelta(days = days)).strftime(fmt)  # 增加天数并格式化输出

    @staticmethod
    def get_next_multiple_of_n_seconds(time: datetime = None, n: int = 60) -> datetime:
        """
        获取指定时间向上取整到最近的 n 秒的时间。如果没有传递时间，默认使用当前时间。

        示例:
        >>> now = datetime(2025, 1, 27, 14, 33, 45)
        >>> get_next_multiple_of_n_seconds(now, 10)
        datetime.datetime(2025, 1, 27, 14, 33, 50)

        >>> get_next_multiple_of_n_seconds(now, 7)
        datetime.datetime(2025, 1, 27, 14, 33, 49)

        :param time: 指定的时间，默认为 None，表示使用当前时间。如果没有传递，默认使用当前时间
        :param n: 向上取整的秒数，默认为 60 秒
        :return: 向上取整到最近的 n 秒的时间
        """
        # 如果没有传递时间，使用当前时间
        if time is None:
            time = datetime.now()

        # 计算当前时间的总秒数
        total_seconds = time.second + time.minute * 60 + time.hour * 3600

        # 计算向上取整后的秒数
        next_seconds = math.ceil(total_seconds / n) * n

        # 计算新的秒数差，并更新时间
        seconds_diff = next_seconds - total_seconds
        next_time = time + timedelta(seconds = seconds_diff)

        # 返回新的时间，保持日期和小时分钟不变
        return next_time.replace(microsecond = 0)

    @staticmethod
    def get_time_difference_in_seconds(time1: datetime, time2: datetime) -> int:
        """
        计算两个时间之间相差多少秒。

        示例:
        >>> time1 = datetime(2025, 1, 27, 14, 30, 0)
        >>> time2 = datetime(2025, 1, 27, 14, 32, 30)
        >>> get_time_difference_in_seconds(time1, time2)
        150

        :param time1: 第一个时间
        :param time2: 第二个时间
        :return: 返回两个时间相差的秒数
        """
        # 计算时间差
        time_difference = abs(time2 - time1)

        # 返回时间差的秒数
        return int(time_difference.total_seconds())


__all__ = ['DateUtils']
