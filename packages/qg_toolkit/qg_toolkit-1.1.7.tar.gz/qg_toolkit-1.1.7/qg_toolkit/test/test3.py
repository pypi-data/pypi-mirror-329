# 应该要等于
# 私钥：5BhdGWX7xN8NMDGAUhJnAi3tbctAn9cNHpbSAoB2xNycTUMYETSiYTay1p6VtJKrUzAJj3AtjuTHxSztg6REvCvh
# 地址：2XnrTMCL1iT88FQvDwYQcQoD1BDMF54GYcLQjijGLcn9

from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, Bip44Changes, base58

from mnemonic import Mnemonic
from solders.keypair import Keypair

# 助记词
mnemonic = "maximum judge sad asthma spice wink dash pattern useless harvest tornado practice"
print(f"助记词: {mnemonic}")
seed_bytes = Bip39SeedGenerator(mnemonic).Generate("")
bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)  # 如果你使用 “Solflare”，请删除此行并进行简单的代码修改和测试
priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
public_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
key_pair = priv_key_bytes + public_key_bytes
result = {
    "mnemonic": mnemonic,
    "address": bip44_chg_ctx.PublicKey().ToAddress(),
    "private": base58.Base58Encoder.Encode(key_pair)
}
