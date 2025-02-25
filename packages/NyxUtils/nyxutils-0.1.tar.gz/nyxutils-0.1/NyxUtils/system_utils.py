import os
import requests
import inspect
import subprocess
import threading
import time
import sys
import signal
from typing import Callable, List, Optional
import platform
if platform.system().lower() == "Windows":
    import winreg as reg


class SystemUtils:

    @staticmethod
    def is_directory_exist(directory_path: str) -> bool:
        """
        判断一个目录是否存在。

        :param directory_path: 目录的路径
        :return: 如果目录存在，返回 True，否则返回 False
        """
        return os.path.isdir(directory_path)

    @staticmethod
    def ensure_file_path_exists(file_path: str) -> bool:
        """
        判断文件路径是否存在，不存在则创建文件。
        如果文件的目录不存在，会先创建目录。
        
        :param file_path: 文件路径
        :return: 文件已存在返回 True 不存在则创建，并返回False
        """
        # 获取目录路径
        dir_path = os.path.dirname(file_path)

        # 如果目录不存在，创建目录
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 如果文件不存在，创建文件
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as f:  # 创建文件
                pass
            return False
        else:
            return True

    @staticmethod
    def get_root_script_path() -> str:
        """
        获取项目中最初执行的脚本路径。

        示例:
        >>> get_root_script_path()
        '/path/to/project'

        :return: 最初执行的脚本所在的绝对路径
        """
        # 返回脚本路径，确保以斜杠结尾
        return os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep

    @staticmethod
    def set_system_proxy(
        proxy_address: str,
        no_proxy:
        str = 'localhost,127.*,10.*,172.16.*,172.17.*,172.18.*,172.19.*,172.20.*,172.21.*,172.22.*,172.23.*,172.24.*,172.25.*,172.26.*,172.27.*,172.28.*,172.29.*,172.30.*,172.31.*,192.168.*'
    ) -> bool:
        """
        设置系统代理（Windows 和 Linux/macOS）。

        示例:
        >>> set_system_proxy("your_proxy_address:port", "example.com,anotherdomain.com")

        :param proxy_address: 代理服务器地址
        :param no_proxy: 不使用代理的域名，按逗号分隔（可选）
        :return: 成功设置代理时返回 True，失败时返回 False
        """
        system = platform.system().lower()

        if system == "windows":
            # Windows 系统设置代理
            reg_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

            try:
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_key, 0, reg.KEY_WRITE)
            except WindowsError as e:
                return False

            reg.SetValueEx(key, 'ProxyServer', 0, reg.REG_SZ, proxy_address)
            reg.SetValueEx(key, 'ProxyEnable', 0, reg.REG_DWORD, 1)

            if no_proxy:
                reg.SetValueEx(key, 'ProxyOverride', 0, reg.REG_SZ, no_proxy)

            reg.CloseKey(key)
            return True

        elif system == "linux" or system == "darwin":  # Linux 或 macOS
            # Linux/macOS 系统设置代理
            os.environ['HTTP_PROXY'] = proxy_address
            os.environ['HTTPS_PROXY'] = proxy_address

            if no_proxy:
                os.environ['NO_PROXY'] = no_proxy

            return True
        else:
            return False

    @staticmethod
    def remove_system_proxy() -> bool:
        """
        删除系统代理（Windows 和 Linux/macOS）。

        示例:
        >>> remove_system_proxy()

        :return: 成功禁用代理时返回 True，失败时返回 False
        """
        system = platform.system().lower()

        if system == "windows":
            # Windows 系统删除代理
            reg_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

            try:
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_key, 0, reg.KEY_WRITE)
            except WindowsError as e:
                return False

            reg.SetValueEx(key, 'ProxyEnable', 0, reg.REG_DWORD, 0)

            reg.CloseKey(key)
            return True

        elif system == "linux" or system == "darwin":  # Linux 或 macOS
            # Linux/macOS 系统删除代理
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)
            os.environ.pop('NO_PROXY', None)

            return True
        else:
            return False

    @staticmethod
    def test_page_load_speed(url: str, proxy_address: str = None) -> float:
        """
        测试网页加载速度，并支持通过代理访问。

        功能描述:
        - 测试指定网页的加载时间，支持通过代理服务器设置访问代理。
        - 如果未设置代理，则直接访问网页。

        使用场景:
        - 用于评估网页的加载性能。
        - 当需要测试通过代理访问网页的速度时可调用此方法。

        示例:
        >>> speed = test_page_load_speed("https://example.com")
        >>> print(f"Page load time: {speed:.2f} ms")

        >>> speed_with_proxy = test_page_load_speed("https://example.com", proxy_address="127.0.0.1:8080")
        >>> print(f"Page load time with proxy: {speed_with_proxy:.2f} ms")

        注意事项:
        - 如果代理设置不正确或目标网页无法访问，该方法将返回 -1。
        - 确保提供的 `url` 是有效的完整网页地址。
        - 超时时间为 10 秒，超过此时间将视为失败。

        :param url: 网页地址，字符串类型，必须是有效的 URL（如 "https://example.com"）。
        :param proxy_address: 可选参数，代理服务器的地址和端口，格式为 'hostname:port'。如无需代理则传入 None。
        :return: 网页加载时间，单位为毫秒。如果加载失败或请求异常，返回 -1。
        """
        # 如果提供了代理地址，则构建代理字典
        if proxy_address:
            proxies = {"http": f"{proxy_address}", "https": f"{proxy_address}"}
        else:
            proxies = None

        # 记录开始时间
        start_time = time.time()

        try:
            # 发送请求并测量响应时间
            response = requests.get(url, proxies = proxies, timeout = 10)
            response.raise_for_status()  # 检查请求是否成功
        except requests.RequestException as e:
            # 返回 -1 表示请求失败
            return -1

        # 记录结束时间
        end_time = time.time()

        # 计算网页加载时间并转换为毫秒
        load_time_ms = (end_time - start_time) * 1000
        return load_time_ms


class ProcessExecutor:
    """
    该类用于启动外部进程并实时读取其标准输出和标准错误。输出通过回调函数返回给调用者，以便在主线程中更新 UI 或进行其他处理。

    示例:
    >>> def print_output(output: str):
    >>>     print(output)
    >>>
    >>> command = ["ping", "google.com", "-c", "5"]
    >>> executor = ProcessExecutor()
    >>> success = executor.start_process(
    >>>     command,
    >>>     update_callback=print_output,
    >>>     error_callback=print_output,
    >>>     timeout=10
    >>> )
    >>> print(success)  # 如果启动成功，返回 True，否则返回 False
    >>> success_stop = executor.stop_process()
    >>> print(success_stop)  # 如果停止成功，返回 True，否则返回 False
    """

    def __init__(self) -> None:
        """
        初始化 ProcessExecutor 实例。
        """
        self.process = None

        # 捕获主进程退出的信号
        signal.signal(signal.SIGTERM, self._handle_exit_signal)
        signal.signal(signal.SIGINT, self._handle_exit_signal)

    def _handle_exit_signal(self, signum, frame) -> None:
        """
        捕获主进程退出信号后，通知子进程退出。

        :param signum: 信号编号
        :param frame: 当前的栈帧
        """
        if self.process:
            self.stop_process()

    def start_process(
        self,
        command: List[str],
        update_callback: Optional[Callable[[str], None]] = None,
        error_callback: Optional[Callable[[str], None]] = None,
        timeout: Optional[int] = None,
        buffer_size: int = 1
    ) -> bool:
        """
        启动外部进程并通过回调函数传递输出。

        :param command: 启动的外部程序命令和参数列表。
        :param update_callback: 用于处理标准输出的回调函数。
        :param error_callback: 用于处理标准错误的回调函数。如果为 None，则不捕获标准错误。
        :param timeout: 可选的进程超时（秒）。如果指定时间内进程未结束，则强制终止。
        :param buffer_size: 可选缓冲区大小，默认为 1（行缓冲）。
        :return: 返回 True 如果启动成功，返回 False 如果启动失败。
        """
        if self.process and self.is_running():
            if update_callback:
                update_callback(f"进程已经在运行: {command}")
            return False

        # 判断操作系统
        is_windows = platform.system() == 'Windows'

        try:
            self.process = subprocess.Popen(
                command,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE if error_callback else subprocess.DEVNULL,
                bufsize = buffer_size,
                universal_newlines = True,
                creationflags = subprocess.CREATE_NO_WINDOW if is_windows else 0  # 隐藏窗口，仅在Windows上使用
            )
        except FileNotFoundError:
            if update_callback:
                update_callback(f"错误: 未找到命令 {command[0]}")
            return False
        except PermissionError:
            if update_callback:
                update_callback(f"错误: 权限不足执行命令 {command[0]}")
            return False
        except Exception as e:
            if update_callback:
                update_callback(f"未知错误: {e}")
            return False

        threading.Thread(target = self._read_stdout, args = (update_callback,), daemon = True).start()

        if error_callback:
            threading.Thread(target = self._read_stderr, args = (error_callback,), daemon = True).start()

        if timeout:
            threading.Thread(target = self._monitor_timeout, args = (timeout, update_callback), daemon = True).start()

        return True

    def _read_stdout(self, update_callback: Optional[Callable[[str], None]]) -> None:
        try:
            for line in self.process.stdout:
                if update_callback:
                    update_callback(line.strip())
        except Exception as e:
            if update_callback:
                update_callback(f"读取标准输出时出错: {e}")

    def _read_stderr(self, error_callback: Optional[Callable[[str], None]]) -> None:
        try:
            for line in self.process.stderr:
                if error_callback:
                    error_callback(line.strip())
        except Exception as e:
            if error_callback:
                error_callback(f"读取标准错误时出错: {e}")

    def _monitor_timeout(self, timeout: int, update_callback: Optional[Callable[[str], None]]) -> None:
        time.sleep(timeout)
        if self.process and self.process.poll() is None:
            if update_callback:
                update_callback("进程超时，正在强制终止进程...")
            self.stop_process()

    def stop_process(self) -> bool:
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout = 5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                return False
            else:
                return True
        return False

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None


__all__ = ['SystemUtils', 'ProcessExecutor']
