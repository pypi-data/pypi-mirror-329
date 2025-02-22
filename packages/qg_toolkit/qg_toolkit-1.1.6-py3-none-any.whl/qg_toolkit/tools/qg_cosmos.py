import ecdsa
import hashlib
import bech32
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator


class QGCosmos:
    def __init__(self, index=0, chain_prefix="cosmos", private_key=None, mnemonic=None):
        self.index = index
        self.chain_prefix = chain_prefix
        self.private_key = private_key
        self.mnemonic = mnemonic

        if self.mnemonic:
            self.private_key = self.mnemonic_to_private_key(self.mnemonic)

        if self.private_key:
            self.public_key, self.address = self.private_key_to_address(self.private_key)

    def mnemonic_to_private_key(self, mnemonic):
        # 使用 BIP39 生成种子
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

        # 使用 BIP44 派生路径生成私钥
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).Purpose().Coin().Account(0).Change(
            Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key_bytes = bip44_mst_ctx.PrivateKey().Raw().ToBytes()
        private_key_hex = private_key_bytes.hex()

        return private_key_hex

    def private_key_to_address(self, private_key_hex):
        # 使用提供的私钥
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)

        # 生成公钥（压缩格式）
        public_key = private_key.get_verifying_key()
        public_key_bytes = public_key.to_string("compressed")  # 使用压缩格式
        public_key_hex = public_key_bytes.hex()

        # 生成钱包地址
        # 1. 对公钥进行 SHA-256 哈希
        sha256_hash = hashlib.sha256(public_key_bytes).digest()

        # 2. 对 SHA-256 哈希结果进行 RIPEMD-160 哈希
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

        # 3. 使用 Bech32 编码生成地址
        five_bit_data = bech32.convertbits(ripemd160_hash, 8, 5)
        address = bech32.bech32_encode(self.chain_prefix, five_bit_data)

        return public_key_hex, address

    def sign_message(self, message):
        if not self.private_key:
            raise ValueError("Private key is not set.")

        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
        signature = private_key.sign(message.encode())
        return signature.hex()

    def transfer(self, to_address, amount):
        # 这里可以实现转账逻辑，通常需要调用区块链的API
        # 由于不同链的API不同，这里只是一个示例
        print(f"Transferring {amount} {self.chain_prefix} to {to_address}")
        # 返回交易哈希或交易结果
        return "tx_hash_example"

    @staticmethod
    def generate_wallets(chain_prefix, count, file_path):
        """
        批量生成钱包并保存到文件
        :param chain_prefix: 链前缀，例如 "cosmos"
        :param count: 生成的钱包数量
        :param file_path: 保存的文件路径
        """
        wallet_lines = []
        for i in range(count):
            # 生成助记词
            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)  # 生成 12 个单词的助记词
            # 生成钱包
            wallet = QGCosmos(index=i, chain_prefix=chain_prefix, mnemonic=mnemonic)
            # 存储到列表中
            wallet_lines.append(f"{i}----{wallet.address}----{wallet.private_key}----{mnemonic}\n")

        # 一次性写入文件
        with open(file_path, "a") as file:
            # file.write("index----address----private_key----mnemonic\n")  # 写入表头
            file.writelines(wallet_lines)


# 示例用法
if __name__ == "__main__":
    # 使用助记词生成钱包
    mnemonic = "people mother energy involve region define bean speed odor diet another sight"
    wallet = QGCosmos(index=0, chain_prefix="cosmos", mnemonic=mnemonic)
    print(f"Private Key: {wallet.private_key}")
    print(f"Public Key: {wallet.public_key}")
    print(f"Address: {wallet.address}")

    # 签名消息
    message = "Hello, Cosmos!"
    signature = wallet.sign_message(message)
    print(f"Signature: {signature}")

    # 转账
    to_address = "cosmos1vyu6e8aq2mtcpeltmh3nue4x6f2aznm8hstqsy"
    amount = "1000"
    tx_hash = wallet.transfer(to_address, amount)
    print(f"Transaction Hash: {tx_hash}")

    # 批量生成钱包并保存到文件
    QGCosmos.generate_wallets(chain_prefix="cosmos", count=10, file_path="wallets.txt")
    print("批量生成钱包完成，已保存到 wallets.txt")