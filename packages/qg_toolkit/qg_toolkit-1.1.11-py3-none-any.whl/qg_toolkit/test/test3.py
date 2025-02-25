from qg_toolkit.tools.qg_solana import QGSolana

qg = QGSolana.from_mnemonic("maximum judge sad asthma spice wink dash pattern useless harvest tornado practice")
print(qg.address)
print(qg.private_key)
print(qg.mnemonic)
x = QGSolana.from_private_key(qg.private_key)
print(x.address)
print(x.private_key)

wallet = QGSolana.create_wallet()
print(wallet)