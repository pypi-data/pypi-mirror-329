import asyncio
import concurrent.futures

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from mnemonic import Mnemonic
from bip_utils import Bip44, Bip44Coins, Bip44Changes
from aptos_sdk.async_client import RestClient


def run_async_in_thread(async_func, *args):
    """
    使用ThreadPoolExecutor在一个线程中运行异步函数
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        rs = loop.run_until_complete(async_func(*args))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    return rs


class QGAptos:
    endpoints = {
        "devnet": "https://aptos.devnet.m1.movementlabs.xyz",
        "mainnet": "https://fullnode.mainnet.aptoslabs.com",
    }

    def __init__(self, index, address=None, private_key=None, mnemonic=None, endpoint=None):
        self.index = index
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.endpoint = endpoint
        if mnemonic and not self.private_key:
            # 生成种子
            mnemo = Mnemonic("english")
            seed = mnemo.to_seed(self.mnemonic)

            # 使用 BIP44 标准生成密钥对
            bip44_mst_ctx = Bip44.FromSeed(seed, Bip44Coins.APTOS)
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            self.private_key = bip44_acc_ctx.PrivateKey().Raw().ToHex()
        if not address and self.private_key:
            # 私钥转为公钥
            self.address = str(Account.load_key(self.private_key).address())
        self.client = RestClient(endpoint if endpoint else self.endpoints.get("devnet"))

    async def get_balance(self):
        account_resource = await self.client.account_resource(AccountAddress.from_str(self.address),
                                                              "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")
        if account_resource:
            balance = int(account_resource["data"]["coin"]["value"]) / 1e8
            print(f'【{self.address}】APT余额：{balance}')
            return balance
        return 0


async def qg_task(index, mn):
    qg = QGAptos(index=index, mnemonic=mn)
    await qg.get_balance()


if __name__ == '__main__':
    mnemonic = "eight undo left fork faith phrase day increase include crawl session sponsor"
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    results = []
    for i in range(5):
        result = executor.submit(run_async_in_thread, qg_task, i, mnemonic)
        results.append(result)
    concurrent.futures.wait(results)
    executor.shutdown()
