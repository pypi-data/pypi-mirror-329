import re
from typing import List, Dict, Optional


class RegexUtils:
    # 注释里面的正则，双斜杠是为了转义，否则运行的时候会打印空行，实际应该是单斜杠
    @staticmethod
    def is_full_match(pattern: str, text: str, flags: int = 0) -> bool:
        """
        检查整个字符串是否完全匹配正则模式。

        该方法使用正则表达式模式检查输入的文本是否完全符合指定的模式。
        如果整个字符串（从头到尾）都匹配该正则模式，返回 True；否则，返回 False。

        例如，如果正则模式要求匹配一个精确的电话号码格式，
        那么 "123-456-7890" 将匹配，但 "123-45-7890" 或 "abcd" 则不会匹配。

        示例:
        >>> RegexUtils.is_full_match(r"\\d{3}-\\d{3}-\\d{4}", "123-456-7890")
        True
        >>> RegexUtils.is_full_match(r"\\d{3}-\\d{3}-\\d{4}", "123-456-78")
        False
        >>> RegexUtils.is_full_match(r"\\d{3}-\\d{3}-\\d{4}", "Hello world")
        False

        :param pattern: 正则模式。可以是任何有效的正则表达式，表示要匹配的模式。
        :param text: 需要匹配的文本。该文本必须完全符合给定的模式才能返回 True。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 如果整个文本完全匹配模式，则返回 True；否则，返回 False。

        注意: 该方法是通过 `re.fullmatch()` 实现的，只有当整个字符串与正则模式完全匹配时，才会返回匹配。
        """
        return bool(re.fullmatch(pattern, text, flags))

    @staticmethod
    def is_match(pattern: str, text: str, flags: int = 0) -> bool:
        """
        使用正则表达式检查字符串是否匹配模式。

        该方法通过 `re.search()` 来检查文本中是否有部分匹配正则模式。
        如果文本中存在与模式部分匹配的区域，返回 True；否则，返回 False。

        示例:
        >>> RegexUtils.is_match(r"\\d{3}-\\d{2}-\\d{4}", "My SSN is 123-45-6789")
        True

        :param pattern: 正则模式。可以是任何有效的正则表达式。
        :param text: 需要匹配的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 如果文本中存在匹配模式的部分，则返回 True；否则，返回 False。
        """
        return bool(re.search(pattern, text, flags))

    @staticmethod
    def find_all(pattern: str, text: str, flags: int = 0) -> List[str]:
        """
        查找所有匹配的字符串并返回列表。

        该方法通过 `re.findall()` 查找文本中所有符合给定正则模式的子串，并返回它们的列表。

        示例:
        >>> RegexUtils.find_all(r"\\d+", "There are 12 apples and 34 bananas.")
        ['12', '34']

        :param pattern: 正则模式。可以是任何有效的正则表达式。
        :param text: 需要搜索的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 所有匹配的字符串列表。
        """
        return re.findall(pattern, text, flags)

    @staticmethod
    def search(pattern: str, text: str, flags: int = 0) -> Optional[re.Match]:
        """
        查找文本中第一个匹配正则模式的部分并返回 match 对象。

        该方法通过 `re.search()` 查找文本中第一个符合给定正则模式的部分，并返回匹配的 `match` 对象。
        如果没有匹配的部分，则返回 `None`。

        示例:
        >>> RegexUtils.search(r"\\d{3}-\\d{2}-\\d{4}", "My SSN is 123-45-6789")
        <re.Match object; span=(11, 23), match='123-45-6789'>

        :param pattern: 正则模式。可以是任何有效的正则表达式。
        :param text: 需要搜索的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 匹配的 `match` 对象，如果没有匹配则返回 `None`。
        """
        return re.search(pattern, text, flags)

    @staticmethod
    def replace(pattern: str, replacement: str, text: str, flags: int = 0) -> str:
        """
        使用指定的字符串替换匹配的内容。

        该方法通过 `re.sub()` 对文本中符合正则模式的部分进行替换，并返回替换后的文本。

        示例:
        >>> RegexUtils.replace(r"\\d+", "X", "There are 12 apples and 34 bananas.")
        'There are X apples and X bananas.'

        :param pattern: 正则模式。可以是任何有效的正则表达式。
        :param replacement: 替换的字符串。
        :param text: 需要进行替换的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 替换后的文本。
        """
        return re.sub(pattern, replacement, text, flags = flags)

    @staticmethod
    def split(pattern: str, text: str, flags: int = 0) -> List[str]:
        """
        使用正则模式分割字符串。

        该方法通过 `re.split()` 将文本按给定正则模式进行分割，并返回分割后的字符串列表。

        示例:
        >>> RegexUtils.split(r"\\s+", "This is a test string.")
        ['This', 'is', 'a', 'test', 'string.']

        :param pattern: 正则模式。可以是任何有效的正则表达式。
        :param text: 需要分割的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 分割后的字符串列表。
        """
        return re.split(pattern, text, flags = flags)

    @staticmethod
    def extract_group_dict(pattern: str, text: str, flags: int = 0) -> Dict[str, str]:
        """
        使用正则模式查找匹配的捕获组，并返回一个字典。

        该方法通过 `re.search()` 查找文本中符合正则模式的部分，并将匹配的捕获组结果作为字典返回。
        字典的键为捕获组的名称（如果有），值为匹配的内容。

        示例:
        >>> RegexUtils.extract_group_dict(r"(?P<first_name>\\w+) (?P<last_name>\\w+)", "John Doe")
        {'first_name': 'John', 'last_name': 'Doe'}

        :param pattern: 正则模式。可以是任何有效的正则表达式，支持命名捕获组。
        :param text: 需要搜索的文本。
        :param flags: 正则标志，默认为 0。可以使用其他标志，例如 `re.IGNORECASE` 来进行大小写不敏感匹配。
        :return: 捕获组的字典，如果没有匹配则返回空字典。
        """
        match = re.search(pattern, text, flags)
        if match:
            return match.groupdict()
        return {}


__all__ = ['RegexUtils']
