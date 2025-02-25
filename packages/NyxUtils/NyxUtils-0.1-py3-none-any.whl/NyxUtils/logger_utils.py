import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class LoggerUtils:
    # 定义日志级别
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    # 默认日志格式
    DEFAULT_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    # 初始化日志设置
    def __init__(self, level: str = 'INFO', to_console: bool = True, log_dir: str = '', format: str = None) -> None:
        """
        初始化日志系统：设置日志级别、是否输出到控制台、日志文件保存路径和日志格式。
        
        :param level: 日志级别，默认为'INFO'
        :param to_console: 是否输出日志到控制台，默认为True
        :param log_dir: 日志文件保存目录，默认为空，表示只输出到控制台
        :param format: 自定义日志格式，默认为None，使用默认格式
        """
        self.level = level
        self.to_console = to_console
        self.log_dir = log_dir
        self.log_format = format or self.DEFAULT_FORMAT
        self.logger = logging.getLogger(__name__)
        self.initialize_logger()

    def initialize_logger(self) -> None:
        """
        统一初始化日志系统：设置日志级别、是否输出到控制台、日志文件保存路径和日志格式。
        """
        # 设置日志级别
        self.logger.setLevel(self.LEVELS.get(self.level, logging.INFO))

        # 如果提供了日志目录，则创建文件处理器
        if self.log_dir:
            # 日志目录设置
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            # 日志文件路径
            log_filename = datetime.now().strftime("%Y-%m-%d") + '.log'
            log_filepath = os.path.join(self.log_dir, log_filename)

            # 设置按天切割日志
            file_handler = TimedRotatingFileHandler(log_filepath, when = "midnight", interval = 1, backupCount = 7)
            file_handler.setLevel(self.LEVELS.get(self.level, logging.INFO))

            # 格式化器
            formatter = logging.Formatter(self.log_format)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # 配置控制台日志处理器
        if self.to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.LEVELS.get(self.level, logging.INFO))

            # 格式化器
            formatter = logging.Formatter(self.log_format)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, msg: str) -> None:
        """
        记录调试级别的日志。

        :param msg: 要记录的日志消息
        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """
        记录信息级别的日志。

        :param msg: 要记录的日志消息
        """
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """
        记录警告级别的日志。

        :param msg: 要记录的日志消息
        """
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """
        记录错误级别的日志。

        :param msg: 要记录的日志消息
        """
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """
        记录严重错误级别的日志。

        :param msg: 要记录的日志消息
        """
        self.logger.critical(msg)


__all__ = ['self']
