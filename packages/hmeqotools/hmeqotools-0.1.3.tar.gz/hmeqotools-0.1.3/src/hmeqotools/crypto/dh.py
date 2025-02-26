from __future__ import annotations

import random

from hmeqotools import mathutil


class DH:
    def __init__(self, p: int, g: int, e: int):
        """Diffie-Hellman算法

        Arguments:
            p (int): 质数
            g (int): 随机整数
            e (int): 私钥
        """
        self.p = p
        self.g = g
        self.e = e

    @staticmethod
    def generate_p(bits: int):
        """随机质数"""
        range_b = 2**bits
        range_a = range_b >> 1
        range_b -= 1
        while True:
            num = random.randint(range_a, range_b)
            if mathutil.is_prime(num):
                return num

    @staticmethod
    def generate_g(p: int):
        """根据p的大小生成随机整数"""
        return random.randint(p >> 1, p - 1)

    @classmethod
    def generate(cls, p: int | None = None, bits=2048):
        p = cls.generate_p(bits)
        g = cls.generate_g(p)
        return DH(p, g, p if p else cls.randint(100000, 999999))

    def public_key(self):
        """合成公钥"""
        return pow(self.g, self.e, self.p)

    def final(self, key: int):
        return pow(key, self.e, self.p)

    randint = random.randint


def main():
    dh = DH.generate()
    # 生成公钥
    public_key = dh.public_key()
    print(public_key)
    # 发送给对方，并接受对方的公钥
    other_public_key = int(input("请输入对方的公钥: "))
    # 合成共同密钥
    aes_key = dh.final(other_public_key)
    print(aes_key)


if __name__ == "__main__":
    main()
