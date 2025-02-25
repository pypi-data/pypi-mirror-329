# from bitcoinlib.keys import Key
# from bitcoinlib.transactions import sign
# from bitcoinlib.encoding import hash160
#
# # 生成私钥和公钥
# private_key = Key()
# public_key = private_key.public()
#
# # 获取公钥的哈希（用于生成SegWit地址）
# public_key_hash = hash160(public_key.to_bytes(compressed=True))
#
# # 假设我们使用的是p2wpkh（Pay-to-Witness-Public-Key-Hash）
# # bc1q 前缀对应的是 '00' 作为版本字节
# hrp = 'bc'  # Human Readable Part
# version_byte = 0x00  # p2wpkh 使用的版本字节
# witprog = public_key_hash
#
# # 编码为Bech32地址
# address = bech32_encode(hrp, witprog, version_byte)
# print(f"Generated SegWit Address: {address}")
#
# # 假设有一个消息需要签名
# message = "Hello, Bitcoin!"
#
# # 使用私钥签名消息
# signature = sign(message, private_key)
# print(f"Signature: {signature}")
#
# # 注意：这里未展示如何验证签名，因为这通常需要一个公钥和相同的消息。
# # 验证签名需要使用签名、公钥和原始消息。