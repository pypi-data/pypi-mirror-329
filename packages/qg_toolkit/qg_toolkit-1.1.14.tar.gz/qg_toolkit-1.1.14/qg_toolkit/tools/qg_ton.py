import base64
from threading import Lock

from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from qg_toolkit.tools.qg_file import QGFile
from tqdm import tqdm


class QGTon:
    # rpc
    endpoints = {
        "mainnet": "https://mainnet.infura.io/v3/257c5f3bdfed414b88a4908b0f999377",
    }
    lock = Lock()

    def __init__(self, index, address=None, private_key=None, mnemonic=None, endpoint=None):
        # 取破解参数
        self.index = index
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        if mnemonic:
            mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonic.split(' '), WalletVersionEnum.v4r2,
                                                                      workchain=0)
            self.address = wallet.address.to_string(True, True, False)
            self.private_key = priv_k.hex()
            self.wallet = wallet

    def sign_msg(self, msg):
        signature = self.wallet.create_signing_message(msg)
        return signature

    @staticmethod
    def generate_wallet(num, filename='生成的Ton钱包.txt'):
        """生成多个Ton钱包并保存到文件"""
        wallet_data = []  # 使用列表收集所有钱包信息
        for x in tqdm(range(num), desc='Ton生成钱包进度：'):
            mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v4r2, workchain=0)
            wallet_address = wallet.address.to_string(True, True, False)
            log = f"{wallet_address}----{priv_k.hex()}----{' '.join(mnemonics)}"
            wallet_data.append(log)  # 将钱包信息添加到列表中
        # 打印所有生成的钱包信息，避免进度条干扰
        for log in wallet_data:
            print(log)
        # 将所有钱包信息一次性写入文件
        output = '\n'.join(wallet_data)
        QGFile.save_to_file(filename, output)

# if __name__ == '__main__':
# QGTon.generate_wallet(10)
# mnemonic = "xxxxxxx"
# mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonic.split(' '), WalletVersionEnum.v4r2, workchain=0)
# print(wallet.address.to_string(True, True, False))
# print(priv_k.hex())
