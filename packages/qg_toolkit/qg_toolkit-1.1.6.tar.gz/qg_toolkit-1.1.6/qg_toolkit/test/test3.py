# from solders.pubkey import Pubkey
#
#
# def get_associated_token_address(mint_address: str, owner_address: str) -> str:
#     # Convert mint and owner addresses to Pubkey objects
#     mint = Pubkey.from_string(mint_address)
#     owner = Pubkey.from_string(owner_address)
#
#     # Associated Token Program ID
#     ASSOCIATED_TOKEN_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
#     # Token Program ID
#     TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
#     # Compute the Associated Token Account address
#     seed = [
#         bytes(owner),
#         bytes(TOKEN_PROGRAM_ID),
#         bytes(mint)
#     ]
#     # Generate a public key from the seeds
#     ata_address, _ = Pubkey.find_program_address(seed, ASSOCIATED_TOKEN_PROGRAM_ID)
#
#     return str(ata_address)
#
#
# # 示例
# mint_address = "TNSRxcUxoT9xBG3de7PiJyTDYu7kskLqcpddxnEJAS6"
# owner_address = "FdJtbk2JQQmBSbXLo78KdgBteTExhzzxuPRJKS7qtBw3"
# ata_address = get_associated_token_address(mint_address, owner_address)
# print(f"Associated Token Account Address: {ata_address}")
