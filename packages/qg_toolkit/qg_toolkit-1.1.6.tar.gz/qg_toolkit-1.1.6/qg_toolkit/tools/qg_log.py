import time

from tqdm import tqdm
from colorama import Fore, Style


def qlog(msg, level=''):
    """ 自定义日志函数，带颜色 """
    level_colors = {
        'info': Fore.GREEN,
        'warn': Fore.YELLOW,
        'error': Fore.RED,
        'debug': Fore.CYAN
    }

    # 获取当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 获取对应的颜色，如果没有找到则不使用颜色
    color = level_colors.get(level, '')

    # 格式化日志信息
    log = f'[{now}]: {color}{msg}{Style.RESET_ALL}'

    tqdm.write(log)


def progress_bar(iterable, **kwargs):
    """ 自定义进度条，带颜色 """
    # 设置描述文字为绿色
    desc = Fore.GREEN + kwargs.pop('desc', '') + Style.RESET_ALL
    # 自定义格式，确保只出现一次百分比，并设置颜色
    bar_format = (
            "{desc} "  # 描述
            "%s{bar}%s "  # 进度条部分
            % (Fore.BLUE, Style.RESET_ALL)
    )
    bar_format += Fore.CYAN + "{percentage:3.0f}%" + Style.RESET_ALL  # 百分比颜色
    bar_format += " | " + Fore.MAGENTA + "{n_fmt}/{total_fmt}" + Style.RESET_ALL  # 计数颜色
    bar_format += " [" + Fore.YELLOW + "{elapsed}<{remaining}" + Style.RESET_ALL  # 耗时颜色
    bar_format += ", " + Fore.GREEN + "{rate_fmt}" + Style.RESET_ALL  # 速率颜色
    bar_format += "{postfix}]"  # 其他信息

    return tqdm(
        iterable,
        desc=desc,  # 带颜色的描述文字
        bar_format=bar_format,
        **kwargs
    )


if __name__ == '__main__':
    # 示例使用
    # qlog("这是信息日志", "info")
    # qlog("这是警告日志", "warn")
    # qlog("这是错误日志", "error")
    # qlog("这是调试日志", "debug")
    # qlog("这是默认日志")
    for i in progress_bar(range(100), desc='Processing'):
        qlog(f'msgssssssssssssssss', 'info')
        time.sleep(0.01)
