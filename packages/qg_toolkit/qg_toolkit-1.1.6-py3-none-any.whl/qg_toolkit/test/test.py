from aptos_sdk.account import Account
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# 助记词
mnemonic_phrase = "eight undo left fork faith phrase day increase include crawl session sponsor"

# 生成种子
mnemo = Mnemonic("english")
seed = mnemo.to_seed(mnemonic_phrase)

# 使用 BIP44 标准生成密钥对
bip44_mst_ctx = Bip44.FromSeed(seed, Bip44Coins.APTOS)
bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
private_key_str = bip44_acc_ctx.PrivateKey().Raw().ToHex()

# 使用私钥创建 Aptos 账户
account = Account.load_key(private_key_str)

# 获取账户地址、私钥和公钥
# address = account.address().address.hex()
address = str(account.address())
private_key = account.private_key
public_key = account.public_key()

print(f"Aptos Wallet Address: 0x{address}")
print(f"Aptos Wallet Private Key: {private_key}")
print(f"Aptos Wallet Public Key: {public_key}")
