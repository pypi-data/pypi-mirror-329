import time
from tqdm import tqdm
from colorama import init, Fore

# 初始化 colorama
init(autoreset=True)

# 模拟一个耗时的任务
total = 100
with tqdm(total=total, desc="Processing", bar_format=f"{Fore.LIGHTBLUE_EX}{{l_bar}}{{bar}}{{r_bar}}") as pbar:
    for i in range(total):
        time.sleep(0.1)
        pbar.update(1)