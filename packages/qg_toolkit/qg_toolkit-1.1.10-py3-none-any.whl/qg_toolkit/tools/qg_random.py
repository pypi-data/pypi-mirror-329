import random
import string
from faker import Faker

from qg_toolkit.tools.qg_solana import QGSolana


class QGRandom:
    fake = Faker(locale="en_US")
    suffix = "@gmailiil.com"
    domain = "gmail.com"

    @classmethod
    def generate_random_name(cls):
        name = cls.fake.name().replace(" ", "").lower()
        return name

    @classmethod
    def generate_first_name(cls):
        name = cls.fake.name()
        return name.split(' ')[0]

    @classmethod
    def generate_random_email(cls, length):
        username = ''.join(random.choices(string.ascii_lowercase, k=length))
        email = f'{username}{cls.suffix}'
        return email

    @classmethod
    def generate_random_str(cls, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @classmethod
    def generate_batch_email(cls, num, length=8, prefix=None, suffix=None):
        """
        生成指定数量的邮件地址列表。

        参数:
        num (int): 要生成的邮件地址数量。
        length (int, 可选): 邮件地址用户名部分的总长度，默认为8。
        prefix (str, 可选): 邮件地址用户名部分的前缀，其长度与随机生成部分长度之和需等于length指定长度，默认为None，即没有前缀。若前缀长度大于length则抛出异常。

        返回:
        list: 生成的邮件地址列表。
        """
        if prefix and len(prefix) > length:
            raise ValueError(f"前缀长度({len(prefix)})大于指定的用户名总长度({length})")
        suffix = suffix or cls.domain
        return [
            f"{(prefix or '') + ''.join(random.choices(string.ascii_lowercase + string.digits, k=(length - len(prefix) if prefix else length)))}@{suffix}"
            for _ in range(num)
        ]

if __name__ == '__main__':
    emails = QGRandom.generate_batch_email(10, prefix='test')
    print(emails)