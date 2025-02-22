import base64
import base58
import struct
from threading import Lock

from solana import constants
from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.token.associated import get_associated_token_address
from solders.transaction import Transaction, VersionedTransaction
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams

from qg_toolkit.tools.qg_file import QGFile
from qg_toolkit.tools.qg_log import progress_bar


class QGSolana:
    # rpc
    endpoints = {
        "mainnet": "https://mainnet.infura.io/v3/257c5f3bdfed414b88a4908b0f999377",
        "mainnet2": "https://api.mainnet-beta.solana.com",
        "mainnet3": "https://fittest-aged-flower.solana-mainnet.quiknode.pro/e4283fb4f6347e50cd39b47d6ddff250327b79c1/",
    }
    lock = Lock()

    def __init__(self, index=None, address=None, private_key=None, mnemonic=None, endpoint=None):
        # 取破解参数
        # "\u0077"
        # JSON.stringify(e)
        self.index = index or 1
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        if private_key:
            self.address = str(Keypair.from_base58_string(self.private_key).pubkey())
        self.client = Client(endpoint if endpoint else self.endpoints.get("mainnet2"))
        self.get_balance()

    def sign_msg(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        signature_encode = k.sign_message(msg.encode())
        return base64.b64encode(bytes(signature_encode)).decode('utf-8')

    def sign_msg_to_base58(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        signature_encode = k.sign_message(msg.encode())
        signature = base58.b58encode(bytes(signature_encode)).decode('utf-8')
        return signature

    def sign_msg_to_hex(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        sig = k.sign_message(msg.encode())
        return bytes(sig).hex()

    def sign_msg_backpack(self, msg):
        payload = self.prepare_offchain_message(msg)
        k = Keypair.from_base58_string(self.private_key)
        signature_encode = k.sign_message(payload)
        return base64.b64encode(bytes(signature_encode)).decode('utf-8')

    @classmethod
    def prepare_offchain_message(cls, message, encoding="UTF-8", max_length=1212):
        message_bytes = message.encode(encoding)
        if len(message_bytes) > max_length:
            raise ValueError(f"超出最大消息长度 ({max_length}) !")

        # 构建消息负载
        payload = bytearray([255]) + b"solana offchain" + bytes([0]) + \
                  bytes([0 if encoding == "ASCII" else (1 if max_length == 1212 else 2)]) + \
                  len(message_bytes).to_bytes(2, byteorder='little') + message_bytes

        return bytes(payload)

    def sign_msg_hex(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        signature = k.sign_message(msg.encode())
        return bytes(signature).hex()

    def get_balance(self, address=None):
        try:
            address = address if address else self.address
            value = self.client.get_balance(Pubkey.from_string(address)).value
            value = value / 10 ** 9
            print(f'【{address}】余额：{value}')
            return value
        except Exception as e:
            print(e)

    def transfer_v2(self, to_address, to_value, is_check=False, check_balance=0.1, opts=None):
        if is_check:
            if self.get_balance(to_address) >= check_balance:
                print(f'【{self.address}】【{self.index}】目标地址：【{to_address}】余额充足，跳过！')
                return
        sender_keypair = Keypair.from_base58_string(self.private_key)  # 发送人私钥
        receiver = Pubkey.from_string(to_address)
        amount_lamports = int(to_value * constants.LAMPORTS_PER_SOL)
        transfer_ix = transfer(
            TransferParams(from_pubkey=sender_keypair.pubkey(), to_pubkey=receiver, lamports=amount_lamports))
        # print(transfer_ix)
        txn = Transaction().add(transfer_ix)
        hash = self.client.send_transaction(txn, sender_keypair, opts=opts)
        print(f'【{self.address}】【{self.index}】转账给【{to_address}】,hash: {hash.value}')
        res_json = self.client.confirm_transaction(hash.value, Commitment("confirmed")).to_json()
        print(f'【{self.address}】【{self.index}】转账给【{to_address}】,hash: {hash.value},转账结果：{res_json}')

    def batch_transfer(self, to_address_list, to_value, is_check=False, check_balance=0.1, opts=None):
        sender_keypair = Keypair.from_base58_string(self.private_key)
        for index, to_address in enumerate(to_address_list, start=1):
            if is_check:
                if self.get_balance(to_address) >= check_balance:
                    print(f'【{self.address}】【{index}】转账给【{to_address}】余额充足，跳过！')
                    continue
            receiver = Pubkey.from_string(to_address)
            amount_lamports = int(to_value * constants.LAMPORTS_PER_SOL)
            transfer_ix = transfer(
                TransferParams(from_pubkey=sender_keypair.pubkey(), to_pubkey=receiver, lamports=amount_lamports))
            txn = Transaction().add(transfer_ix)
            hash = self.client.send_transaction(txn, sender_keypair, opts=opts)
            print(f'【{self.address}】【{index}】转账给【{to_address}】,hash: {hash.value}')
            res_json = self.client.confirm_transaction(hash.value, Commitment("confirmed")).to_json()
            print(f'【{self.address}】【{index}】转账给【{to_address}】,hash: {hash.value},转账结果：{res_json}')

    def swap_by_txn_buff(self, tx_buffer):
        txn = Transaction.deserialize(tx_buffer)
        sender_keypair = Keypair.from_base58_string(self.private_key)  # 发送人私钥
        txn.sign_partial(sender_keypair)
        resp = self.client.send_raw_transaction(txn.serialize(), opts=TxOpts(skip_preflight=True))
        print(f'【{self.address}】【{self.index}】hash: {resp.value}')
        res_json = self.client.confirm_transaction(resp.value, Commitment("confirmed")).to_json()
        print(f'【{self.address}】【{self.index}】hash: {resp.value},转账结果：{res_json}')
        return resp.value

    def transfer(self, to_address, to_value, is_check=False, check_balance=0.1):
        if is_check:
            if self.get_balance(to_address) >= check_balance:
                print(f'【{to_address}】余额充足，跳过！')
                return
        sender_keypair = Keypair.from_base58_string(self.private_key)  # 发送人私钥
        receiver = Pubkey.from_string(to_address)
        # transfer_ix = transfer(TransferParams(from_pubkey=sender_keypair.pubkey(), to_pubkey=receiver, lamports=100_000))#sol精度9
        # print(transfer_ix)
        program_id = constants.SYSTEM_PROGRAM_ID
        # amount = int(0.01 * 10 ** 9)
        amount = int(to_value * constants.LAMPORTS_PER_SOL)
        amount_hex = struct.pack('<Q', amount).hex()
        data = '02000000' + amount_hex
        data_bytes = bytes.fromhex(data)
        ats = [
            AccountMeta(sender_keypair.pubkey(), True, True),
            AccountMeta(receiver, False, True)
        ]
        transfer_ix = Instruction(program_id, data_bytes, ats)
        txn = Transaction().add(transfer_ix)
        hash1 = self.client.send_transaction(txn, sender_keypair)
        print(f'【{self.address}】【{self.index}】转账给【{to_address}】,hash: {hash1.value}')
        res_json = self.client.confirm_transaction(hash1.value, Commitment("confirmed")).to_json()
        print(f'【{self.address}】【{self.index}】转账给【{to_address}】,hash: {hash1.value},转账结果：{res_json}')

    def batch_transfer(self, to_address_list, to_value, is_check=False, check_balance=0.01):
        for to_address in to_address_list:
            self.transfer(to_address, to_value, is_check, check_balance)

    def transfer_token(self, token_address: str, to_address: str, amount: float, check_self_balance: float = 1, limit_fee: float = 0.00005):

        # 加载发送者密钥
        sender_keypair = Keypair.from_base58_string(self.private_key)
        sender_public_key = sender_keypair.pubkey()
        # 加载代币合约地址和接收者地址
        token_mint_pubkey = Pubkey.from_string(token_address)
        to_pubkey = Pubkey.from_string(to_address)

        # 获取发送者和接收者的关联代币账户地址
        sender_token_account = get_associated_token_address(sender_public_key, token_mint_pubkey)
        to_token_account = get_associated_token_address(to_pubkey, token_mint_pubkey)
        # 检查代币账户是否存在（如果接收者账户不存在，需要创建）
        response = self.client.get_token_account_balance(sender_token_account)
        print(f'【{self.address}】【{self.index}】当前账户SONIC余额: {response.value.ui_amount}')
        balance = response.value.ui_amount
        if balance <= check_self_balance:
            print(f'【{self.address}】【{self.index}】余额不足，不转账！')
            return
        # 如果amount为负数/大于余额的数量，则数量等于余额
        amount = balance if amount < 0 or amount > balance else amount

        # 获取代币小数位
        token_info = self.client.get_token_supply(token_mint_pubkey)
        decimals = int(token_info.value.decimals)
        # 构建转账指令
        # 转换金额到最小单位
        lamports = int(amount * (10 ** decimals))
        transfer_instruction = transfer_checked(
            TransferCheckedParams(
                program_id=TOKEN_PROGRAM_ID,
                source=sender_token_account,
                mint=token_mint_pubkey,
                dest=to_token_account,
                owner=sender_public_key,
                amount=lamports,
                decimals=decimals,
            )
        )
        try:
            # 构建新版 MessageV0
            message_v0 = MessageV0.try_compile(
                payer=sender_public_key,  # 手续费支付者
                instructions=[transfer_instruction],  # 指令列表
                recent_blockhash=self.client.get_latest_blockhash().value.blockhash,  # 当前的 blockhash
                address_lookup_table_accounts=[]
            )
            # 创建 VersionedTransaction
            versioned_tx = VersionedTransaction(message_v0, [sender_keypair])
            simulate_response = self.client.get_fee_for_message(message_v0)
            fee = float(simulate_response.value * 1.0 / 10 ** 9)
            print(f'【{self.address}】【{self.index}】预估手续费: {fee} SOL')
            if limit_fee and fee > limit_fee:
                print(f'【{self.address}】【{self.index}】手续费过高，无法转账')
                return
            print(f'【{self.address}】【{self.index}】手续费低，开始转账')
            tx_hash = self.client.send_raw_transaction(bytes(versioned_tx), opts=TxOpts(skip_preflight=False))
            print(f"【{self.address}】【{self.index}】转账交易哈希: {tx_hash.value}")
            result = self.client.confirm_transaction(tx_hash.value, Commitment("confirmed"))
            print(f"【{self.address}】【{self.index}】交易确认结果: {result.to_json()}")
        except Exception as e:
            print(f'【{self.address}】【{self.index}】转账出错：{e}')
            raise e

    def to_pri(self):
        k = Keypair.from_base58_string(self.private_key)
        global arr
        arr.append(k.to_bytes_array())
        print(f'【{self.address}】【{self.index}】: {k.to_bytes_array()}')

    @staticmethod
    def generate_wallet(num, filename='生成的Solana钱包.txt'):
        for i in range(num):
            keypair = Keypair()
            log = f'{keypair.pubkey()}----{keypair}----{keypair.to_bytes_array()}'
            print(log)
            QGFile.save_to_file(f'{filename}', log)

    @staticmethod
    def generate_wallet_v2(num, filename='生成的Solana钱包.txt'):
        wallet_data = []  # 使用列表收集所有钱包信息
        for x in progress_bar(range(num), desc='Sol生成钱包进度：'):
            keypair = Keypair()
            log = f'{keypair.pubkey()}----{keypair}----{keypair.to_bytes_array()}\n'
            wallet_data.append(log)  # 将钱包信息添加到列表中
        # 打印所有生成的钱包信息，避免进度条干扰
        for log in wallet_data:
            print(log)
        # 将所有钱包信息一次性写入文件
        output = '\n'.join(wallet_data)
        QGFile.save_to_file(filename, output)

    @staticmethod
    def season_pda(season_id: int, program_id: str):
        season_id_buffer = bytes([season_id])
        seeds = [b"season", season_id_buffer]

        program_id_key = Pubkey.from_string(program_id)

        pda, _ = Pubkey.find_program_address(seeds, program_id_key)
        print(pda)
        print(_)
