import sys
import time


# 进度条功能类
class ProgressBarUtils:

    @staticmethod
    def download_simulation(
        current: float,
        total: float,
        start_time: float,
        bar_length: int = 40,
        show_speed: bool = True,
        show_eta: bool = True
    ) -> None:
        """
        显示下载进度条
        
        :param current: 当前已下载大小（单位: MB）
        :param total_size: 文件总大小 (单位: MB)
        :param start_time: 文件下载开始的时间戳
        :param bar_length: 进度条长度（默认 40）
        :param show_speed: 是否显示下载速度（默认显示）
        :param show_eta: 是否显示预计剩余时间（默认显示）
        """
        if total <= 0:  # 避免 total = 0 时除零错误
            print("\n\033[31m错误: 总文件大小不能为 0！\033[0m")
            return

        # 计算进度比例
        progress = min(current / total, 1.0)  # 确保进度不超过100%
        filled_length = int(progress * bar_length)
        empty_length = bar_length - filled_length

        # 计算下载速度和剩余时间
        elapsed_time = max(time.time() - start_time, 1e-6)  # 计算经过的时间
        speed = current / elapsed_time if elapsed_time > 0 else 0  # 下载速度（MB/s）
        remaining_time = (total - current) / speed if current < total else 0  # 预计剩余时间

        # 构建美化的进度条
        progress_bar = (
            "\033[38;5;46m" + "━" * filled_length +  # 渐变绿色填充部分
            "\033[38;5;240m" + "━" * empty_length +  # 灰色未填充部分
            "\033[0m"  # 重置颜色
        )

        # 准备进度条输出
        output = f"[{progress_bar}] {current:.2f}/{total:.2f} MB "

        # 显示下载速度
        if show_speed:
            output += f"\033[38;5;14m{speed:.2f} MB/s\033[0m "

        # 显示剩余时间 小时:分钟:秒格式
        if show_eta and remaining_time > 0:
            remaining_time = int(remaining_time)  # 确保是整数秒
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            output += f"eta \033[38;5;11m{hours:02}:{minutes:02}:{seconds:02}\033[0m"

        # 输出进度条
        sys.stdout.write("\r" + " " * (len(output) + bar_length) + "\r")  # 确保每次刷新进度条时，之前的输出内容被完全覆盖掉
        sys.stdout.write(output)
        sys.stdout.flush()


__all__ = ['ProgressBarUtils']
