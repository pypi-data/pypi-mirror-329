import base64
import hashlib
from urllib.parse import quote, unquote


# 编码解码功能类
class EncodingUtils:

    @staticmethod
    def encode_base64(data: str) -> str:
        """
        将字符串编码为 Base64 格式。

        该方法通过 Base64 编码将输入的字符串转换为一个 Base64 编码的字符串。
        Base64 编码常用于在网络传输中表示二进制数据，使其适合于 ASCII 字符集。

        示例:
        >>> encoded = EncodingUtils.encode_base64("hello")
        >>> print(encoded)
        aGVsbG8=

        :param data: 要编码的字符串。将使用 UTF-8 编码进行编码。
        :return: Base64 编码后的字符串。编码结果为可读的 ASCII 字符串。

        注意: 编码后可能会出现 "==" 结尾，这是 Base64 编码中用于填充的字符。
        """
        return base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode_base64(data: str) -> str:
        """
        将 Base64 编码的字符串解码回原始字符串。

        该方法将输入的 Base64 编码字符串解码回其原始的 UTF-8 编码字符串。

        示例:
        >>> decoded = EncodingUtils.decode_base64("aGVsbG8=")
        >>> print(decoded)
        hello

        :param data: Base64 编码的字符串。必须是有效的 Base64 编码。
        :return: 解码后的原始字符串，返回的内容为 UTF-8 编码。

        注意: 如果输入的 Base64 字符串无效，解码会抛出异常。
        """
        return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def encode_url(data: str) -> str:
        """
        对字符串进行 URL 编码。

        该方法使用 URL 编码标准，将特殊字符（如空格、符号等）编码为百分号编码（%20, %3D等），
        使其适用于 URL 或查询参数中。

        示例:
        >>> encoded = EncodingUtils.encode_url("hello world")
        >>> print(encoded)
        hello%20world

        :param data: 要编码的字符串，通常为查询参数或 URL 的一部分。
        :return: URL 编码后的字符串，所有特殊字符都被转换为 "%xx" 格式。

        注意: URL 编码确保字符串在 HTTP 请求中传输时不被误解。
        """
        return quote(data)

    @staticmethod
    def decode_url(data: str) -> str:
        """
        对 URL 编码的字符串进行解码。

        该方法将输入的 URL 编码字符串还原为原始字符串。

        示例:
        >>> decoded = EncodingUtils.decode_url("hello%20world")
        >>> print(decoded)
        hello world

        :param data: URL 编码的字符串，应该是由 `encode_url` 方法编码的。
        :return: 解码后的原始字符串，恢复为正常的字符序列。

        注意: 解码后的字符串可以包含空格、符号等。
        """
        return unquote(data)

    @staticmethod
    def hash_sha256(data: str) -> str:
        """
        生成给定字符串的 SHA-256 哈希值。

        该方法通过 SHA-256 算法生成字符串的哈希值。SHA-256 是一种常用的哈希算法，
        它产生一个长度为 256 位的固定长度输出，常用于数据完整性验证和数字签名。

        示例:
        >>> hashed = EncodingUtils.hash_sha256("hello")
        >>> print(hashed)
        2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

        :param data: 要计算哈希值的字符串。可以是任何类型的文本数据。
        :return: 计算得到的 SHA-256 哈希值，返回的结果是一个 64 字符长的十六进制字符串。

        注意: 哈希值是不可逆的，即无法从哈希值恢复原始数据。
        """

        return hashlib.sha256(data.encode('utf-8')).hexdigest()


__all__ = ['EncodingUtils']
