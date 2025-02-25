import sys
from loguru import logger

# 定义模块名和函数名的最大长度
MAX_MODULE_LENGTH = 10
MAX_FUNCTION_LENGTH = 15
MAX_LINE_LENGTH = 4


def format_log(log, max_length):
    """格式化，截取或补齐到指定长度"""
    if isinstance(log, int):
        log = str(log)
    if len(log) > max_length:
        return log[:max_length]
    return log.ljust(max_length)


# 自定义格式化函数
def custom_format(record):
    """自定义日志格式"""
    module = format_log(record["name"], max_length=MAX_MODULE_LENGTH)
    # 先截取原始函数名
    function = record["function"][:MAX_FUNCTION_LENGTH]
    # 转义处理
    escaped_function = function.replace('<module>', 'main')
    line = format_log(record["line"], max_length=MAX_LINE_LENGTH)
    time_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
    level = "<level>{level:^9}</level>"
    location = f"<cyan>{module}:{escaped_function}:{line : ^4}</cyan>"
    message = "<level>{message}</level>"
    # 将 | 设置为红色
    separator = "<red>|</red>"
    return f"{time_str}{separator}{level}{separator}{location :^46}{separator} {message}\n"


# 移除默认的日志处理器
logger.remove()

# 添加新的处理器，使用自定义格式
logger.add(
    sink=sys.stdout,
    format=custom_format,
)
