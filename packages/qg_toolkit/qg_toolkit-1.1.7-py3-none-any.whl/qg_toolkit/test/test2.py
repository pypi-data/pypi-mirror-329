# 助记词
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip39Languages, Bip44Changes
from solders.keypair import Keypair

# Coin that we want
coin_type = Bip44Coins.SOLANA

# Mnemonic
mnemonic = "eight undo left fork faith phrase day increase include crawl session sponsor"
seed_bytes = Bip39SeedGenerator(str(mnemonic), Bip39Languages.ENGLISH).Generate("")
bip44_seeds = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA).Purpose().Coin()
priv_key_bytes = bip44_seeds.Account(0).Change(Bip44Changes.CHAIN_EXT).PrivateKey().Raw().ToBytes()
pub_key_bytes = bip44_seeds.Account(0).Change(Bip44Changes.CHAIN_EXT).PublicKey().RawCompressed().ToBytes()[1:]
key_pair = priv_key_bytes + pub_key_bytes

# 打印地址和密钥
address = bip44_seeds.Account(0).PublicKey().ToAddress()
private_key = key_pair.hex()

print(f"{{\"address\": \"{address}\", \"private_key\": \"{private_key}\"}}")

