from typing import List


# 数学操作类
class MathUtils:

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        判断一个数字是否为素数。

        示例:
        >>> print(MathUtils.is_prime(17))
        True
        >>> print(MathUtils.is_prime(18))
        False

        :param n: 要检查的数字
        :return: 如果是素数返回 True，否则返回 False
        """
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def generate_fibonacci(n: int) -> List[int]:
        """
        生成斐波那契数列，返回前 n 项。

        示例:
        >>> print(MathUtils.generate_fibonacci(5))
        [0, 1, 1, 2, 3]

        :param n: 要生成的斐波那契数列的长度
        :return: 生成的斐波那契数列列表
        """
        if n <= 0:
            return []
        fib = [0, 1]
        for _ in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib[:n]


__all__ = ['MathUtils']
