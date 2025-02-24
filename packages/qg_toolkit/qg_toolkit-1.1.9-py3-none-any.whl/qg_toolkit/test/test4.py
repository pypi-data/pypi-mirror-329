from qg_toolkit.tools.qg_log import *
from qg_toolkit.tools.qg_solana import QGSolana
from qg_toolkit.tools.qg_ton import QGTon

# qlog("这是信息日志", "info")
# qlog("这是警告日志", "warn")
# qlog("这是错误日志", "error")
# qlog("这是调试日志", "debug")
# qlog("这是默认日志")
# for i in progress_bar(range(100), desc='进度：'):
#     time.sleep(0.01)

QGTon.generate_wallet(40, 'ton钱包.txt')
print("第一个钱包生成完成")
QGSolana.generate_wallet_v2(30, 'sol钱包.txt')
print("第二个钱包生成完成")