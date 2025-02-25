import random
import re
import string
from typing import Union


# 字符串操作类
class StringUtils:
    # 英文国家名称集合
    ENGLISH_COUNTRIES = {
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
        "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
        "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
        "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
        "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
        "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
        "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
        "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
        "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South",
        "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
        "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
        "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
        "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay",
        "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
        "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
        "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
        "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
        "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "Hong Kong", "Macau"
    }

    # 中文国家名称集合
    CHINESE_COUNTRIES = {
        "阿富汗", "阿尔巴尼亚", "阿尔及利亚", "安道尔", "安哥拉", "安提瓜和巴布达", "阿根廷", "亚美尼亚", "澳大利亚", "奥地利", "阿塞拜疆", "巴哈马", "巴林", "孟加拉国",
        "巴巴多斯", "白俄罗斯", "比利时", "伯利兹", "贝宁", "不丹", "玻利维亚", "波黑", "博茨瓦纳", "巴西", "文莱", "保加利亚", "布基纳法索", "布隆迪", "佛得角",
        "柬埔寨", "喀麦隆", "加拿大", "中非共和国", "乍得", "智利", "中国", "哥伦比亚", "科摩罗", "刚果", "哥斯达黎加", "克罗地亚", "古巴", "塞浦路斯", "捷克",
        "刚果（金）", "丹麦", "吉布提", "多米尼加", "多米尼加共和国", "厄瓜多尔", "埃及", "萨尔瓦多", "赤道几内亚", "厄立特里亚", "爱沙尼亚", "斯威士兰", "埃塞俄比亚", "斐济",
        "芬兰", "法国", "加蓬", "冈比亚", "格鲁吉亚", "德国", "加纳", "希腊", "格林纳达", "危地马拉", "几内亚", "几内亚比绍", "圭亚那", "海地", "洪都拉斯", "匈牙利",
        "冰岛", "印度", "印度尼西亚", "伊朗", "伊拉克", "爱尔兰", "以色列", "意大利", "牙买加", "日本", "约旦", "哈萨克斯坦", "肯尼亚", "基里巴斯", "朝鲜", "韩国",
        "科威特", "吉尔吉斯斯坦", "老挝", "拉脱维亚", "黎巴嫩", "莱索托", "利比里亚", "利比亚", "列支敦士登", "立陶宛", "卢森堡", "马达加斯加", "马拉维", "马来西亚",
        "马尔代夫", "马里", "马耳他", "马绍尔群岛", "毛里塔尼亚", "毛里求斯", "墨西哥", "密克罗尼西亚", "摩尔多瓦", "摩纳哥", "蒙古", "黑山", "摩洛哥", "莫桑比克", "缅甸",
        "纳米比亚", "瑙鲁", "尼泊尔", "荷兰", "新西兰", "尼加拉瓜", "尼日尔", "尼日利亚", "北马其顿", "挪威", "阿曼", "巴基斯坦", "帕劳", "巴拿马", "巴布亚新几内亚",
        "巴拉圭", "秘鲁", "菲律宾", "波兰", "葡萄牙", "卡塔尔", "罗马尼亚", "俄罗斯", "卢旺达", "圣基茨和尼维斯", "圣卢西亚", "圣文森特和格林纳丁斯", "萨摩亚", "圣马力诺",
        "圣多美和普林西比", "沙特阿拉伯", "塞内加尔", "塞尔维亚", "塞舌尔", "塞拉利昂", "新加坡", "斯洛伐克", "斯洛文尼亚", "所罗门群岛", "索马里", "南非", "南苏丹", "西班牙",
        "斯里兰卡", "苏丹", "苏里南", "瑞典", "瑞士", "叙利亚", "塔吉克斯坦", "坦桑尼亚", "泰国", "东帝汶", "多哥", "汤加", "特立尼达和多巴哥", "突尼斯", "土耳其",
        "土库曼斯坦", "图瓦卢", "乌干达", "乌克兰", "阿联酋", "英国", "美国", "乌拉圭", "乌兹别克斯坦", "万那杜", "梵蒂冈", "委内瑞拉", "越南", "也门", "赞比亚",
        "津巴布韦", "香港", "澳门", "台湾"
    }

    @staticmethod
    def find_country_name(text: str) -> Union[str, bool]:
        """
        检查字符串是否包含任何国家名，并返回匹配的国家名（英文或中文）。
        
        :param text: 输入的字符串
        :return: 如果包含国家名，则返回匹配的国家名，否则返回 False
        """
        # 按照国家名的长度从长到短排序
        sorted_english_countries = sorted(StringUtils.ENGLISH_COUNTRIES, key = len, reverse = True)
        sorted_chinese_countries = sorted(StringUtils.CHINESE_COUNTRIES, key = len, reverse = True)

        # 检查英文国家名
        for country in sorted_english_countries:
            if country.lower() in text.lower():  # 忽略大小写
                return country

        # 检查中文国家名
        for country in sorted_chinese_countries:
            if country in text:
                return country

        return False

    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """
        生成指定长度的随机字符串，包含字母和数字。

        示例:
        >>> StringUtils.generate_random_string(10)
        'a1B2c3D4e5'

        :param length: 字符串长度（默认为 8）
        :return: 随机生成的字符串
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k = length))

    @staticmethod
    def is_palindrome(text: str) -> bool:
        """
        判断字符串是否为回文（忽略大小写和非字母数字字符）。

        示例:
        >>> StringUtils.is_palindrome("A man a plan a canal Panama")
        True

        >>> StringUtils.is_palindrome("Hello World")
        False

        :param text: 待检查的字符串
        :return: 如果是回文返回 True，否则返回 False
        """
        cleaned_text = ''.join(filter(str.isalnum, text)).casefold()
        return cleaned_text == cleaned_text[::-1]

    @staticmethod
    def reverse_string(text: str) -> str:
        """
        反转字符串。

        示例:
        >>> StringUtils.reverse_string("hello")
        'olleh'

        :param text: 原始字符串
        :return: 反转后的字符串
        """
        return text[::-1]

    @staticmethod
    def count_vowels(text: str) -> int:
        """
        统计字符串中的元音字母个数（忽略大小写）。

        示例:
        >>> StringUtils.count_vowels("Hello World")
        3

        :param text: 输入字符串
        :return: 元音字母的数量
        """
        vowels = "aeiouAEIOU"
        return sum(1 for char in text if char in vowels)

    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        将字符串转换为蛇形命名法（snake_case）。

        示例:
        >>> StringUtils.to_snake_case("HelloWorld Example")
        'hello_world_example'

        :param text: 原始字符串
        :return: 转换后的蛇形命名字符串
        """
        text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
        return text.replace(" ", "_")

    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        将字符串转换为驼峰命名法（camelCase）。

        示例:
        >>> StringUtils.to_camel_case("hello_world_example")
        'helloWorldExample'

        :param text: 原始字符串
        :return: 转换后的驼峰命名字符串
        """
        words = re.split(r'[_\s]+', text)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    @staticmethod
    def contains_substring(text: str, substring: str, ignore_case: bool = True) -> bool:
        """
        检查字符串是否包含子串（支持忽略大小写）。

        示例:
        >>> StringUtils.contains_substring("Hello World", "world")
        True

        >>> StringUtils.contains_substring("Hello World", "Python")
        False

        :param text: 原始字符串
        :param substring: 子串
        :param ignore_case: 是否忽略大小写（默认为 True）
        :return: 如果包含子串返回 True，否则返回 False
        """
        if ignore_case:
            text, substring = text.lower(), substring.lower()
        return substring in text

    @staticmethod
    def remove_whitespace(text: str) -> str:
        """
        移除字符串中的所有空白字符。

        示例:
        >>> StringUtils.remove_whitespace("  Hello   World  ")
        'HelloWorld'

        :param text: 输入字符串
        :return: 去除空白后的字符串
        """
        return ''.join(c for c in text if not c.isspace())

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """
        移除字符串中的所有标点符号。

        示例:
        >>> StringUtils.remove_punctuation("Hello, World!")
        'Hello World'

        :param text: 输入字符串
        :return: 去掉标点后的字符串
        """
        return re.sub(r'[^\w\s]', '', text)

    @staticmethod
    def find_longest_word(text: str) -> str:
        """
        找到字符串中最长的单词。

        示例:
        >>> StringUtils.find_longest_word("This is an example string")
        'example'

        :param text: 输入字符串
        :return: 最长的单词
        """
        words = text.split()
        return max(words, key = len, default = "")

    @staticmethod
    def count_words(text: str) -> int:
        """
        统计字符串中的单词数量。

        示例:
        >>> StringUtils.count_words("This is an example string")
        5

        :param text: 输入字符串
        :return: 单词的数量
        """
        return len(text.split())

    @staticmethod
    def is_numeric(text: str) -> bool:
        """
        判断字符串是否完全由数字组成。

        示例:
        >>> StringUtils.is_numeric("12345")
        True

        >>> StringUtils.is_numeric("123a45")
        False

        :param text: 输入字符串
        :return: 如果全为数字返回 True，否则返回 False
        """
        return text.isdigit()

    @staticmethod
    def swap_case(text: str) -> str:
        """
        将字符串中的大小写互换。

        示例:
        >>> StringUtils.swap_case("Hello World")
        'hELLO wORLD'

        :param text: 输入字符串
        :return: 大小写互换后的字符串
        """
        return text.swapcase()

    @staticmethod
    def starts_with(text: str, prefix: str) -> bool:
        """
        检查字符串是否以指定前缀开头。

        示例:
        >>> StringUtils.starts_with("Hello World", "Hello")
        True

        :param text: 输入字符串
        :param prefix: 前缀
        :return: 如果以指定前缀开头返回 True，否则返回 False
        """
        return text.startswith(prefix)

    @staticmethod
    def ends_with(text: str, suffix: str) -> bool:
        """
        检查字符串是否以指定后缀结尾。

        示例:
        >>> StringUtils.ends_with("Hello World", "World")
        True

        :param text: 输入字符串
        :param suffix: 后缀
        :return: 如果以指定后缀结尾返回 True，否则返回 False
        """
        return text.endswith(suffix)

    @staticmethod
    def pad_string(text: str, length: int, pad_char: str = "*", direction: str = "right") -> str:
        """
        对字符串进行左右填充以达到指定长度。

        示例:
        >>> StringUtils.pad_string("Hello", 10, "*", "right")
        'Hello*****'

        >>> StringUtils.pad_string("Hello", 10, "*", "left")
        '*****Hello'

        >>> StringUtils.pad_string("Hello", 10, "*", "both")
        '**Hello***'

        :param text: 输入字符串
        :param length: 目标长度
        :param pad_char: 填充字符（默认为空格）
        :param direction: 填充方向，可选 "right", "left", "both"
        :return: 填充后的字符串
        """
        if direction == "right":
            return text.ljust(length, pad_char)
        elif direction == "left":
            return text.rjust(length, pad_char)
        elif direction == "both":
            total_pad = length - len(text)
            left_pad = total_pad // 2
            right_pad = total_pad - left_pad
            return f"{pad_char * left_pad}{text}{pad_char * right_pad}"
        else:
            raise ValueError("Invalid direction. Use 'right', 'left', or 'both'.")

    @staticmethod
    def replace_variables(template: str, **kwargs) -> str:
        """
        使用 format 替换字符串中的变量。如果在替换过程中出现错误，会抛出异常交由上级处理。

        功能描述:
        该函数接受一个包含占位符的模板字符串，并通过传入的关键字参数替换相应的占位符。

        示例:
        >>> template = "Hello, {name}!"
        >>> replace_variables(template, name="Alice")
        'Hello, Alice!'

        :param template: 包含变量的模板字符串，格式应该为 '{key}' 形式的占位符
        :param kwargs: 要替换的变量及其值，形式为 key=value，例如 `name="Alice"`
        :return: 替换后的字符串
        :raises KeyError: 如果模板中存在未提供的变量
        :raises ValueError: 如果模板中占位符的格式不正确
        """
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError) as e:
            # 将异常抛出，交由上级处理
            raise e


__all__ = ['StringUtils']
