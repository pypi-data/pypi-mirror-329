import os
import shutil
import mimetypes


class FileUtils:

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        读取文件内容并返回文件的文本。

        示例:
        >>> content = FileUtils.read_file("example.txt")
        >>> print(content)
        Hello, World!

        :param file_path: 文件路径
        :return: 文件内容字符串
        :raises FileNotFoundError: 如果文件不存在则抛出异常
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件未找到: {file_path}")
        with open(file_path, 'r', encoding = 'utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path: str, content: str, append: bool = False) -> bool:
        """
        将指定内容写入文件，支持覆盖或追加模式。

        示例:
        >>> FileUtils.write_file("example.txt", "Hello, World!")
        >>> content = FileUtils.read_file("example.txt")
        >>> print(content)
        Hello, World!

        :param file_path: 文件路径
        :param content: 要写入的内容
        :param append: 是否追加写入（默认为覆盖写入）
        :return: 如果文件写入成功，返回 True；否则返回 False
        """
        try:
            mode = 'a' if append else 'w'  # 如果 append 为 True，使用追加模式
            with open(file_path, mode, encoding = 'utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> str:
        """
        获取文件的大小，并返回人类可读的格式（如 B、KB、MB）。

        示例:
        >>> size = FileUtils.get_file_size("example.txt")
        >>> print(size)
        13B

        :param file_path: 文件路径
        :return: 文件大小（如 13B、1.2KB、2MB）
        """
        if not os.path.exists(file_path):
            return "0B"
        size_bytes = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f}{unit}"
            size_bytes /= 1024

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        删除指定的文件。

        示例:
        >>> result = FileUtils.delete_file("example.txt")
        >>> print(result)
        True

        :param file_path: 文件路径
        :return: 如果文件删除成功，返回 True；否则返回 False
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def copy_file(src_path: str, dest_path: str) -> bool:
        """
        复制文件到指定的目标路径。

        示例:
        >>> result = FileUtils.copy_file("example.txt", "copy_example.txt")
        >>> print(result)
        True

        :param src_path: 源文件路径
        :param dest_path: 目标文件路径
        :return: 如果文件复制成功，返回 True；否则返回 False
        """
        try:
            if os.path.exists(src_path):
                shutil.copy(src_path, dest_path)
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def rename_file(old_path: str, new_path: str) -> bool:
        """
        重命名文件。

        示例:
        >>> result = FileUtils.rename_file("old_name.txt", "new_name.txt")
        >>> print(result)
        True

        :param old_path: 旧文件路径
        :param new_path: 新文件路径
        :return: 如果文件重命名成功，返回 True；否则返回 False
        """
        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_image(file_path) -> bool:
        mime_type, _ = mimetypes.guess_type(file_path)
        # 判断是否是图片类型，但排除 GIF 文件
        return mime_type and mime_type.startswith('image')

    def is_gif_image(file_path) -> bool:
        mime_type, _ = mimetypes.guess_type(file_path)
        # 判断是否是图片类型，但排除 GIF 文件
        return mime_type and mime_type.startswith('image') and mime_type == 'image/gif'

    @staticmethod
    def is_video(file_path) -> bool:
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type and mime_type.startswith('video')


__all__ = ['FileUtils']
