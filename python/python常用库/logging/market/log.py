"""
日志模块

日志保存在 ./logs/ 文件夹下

"""
import os
import sys
import logging
import logging.handlers

# 文件主目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日志路径 当前目录下的 logs文件夹
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE_PATH = os.path.join(LOG_DIR, 'output.log')
ERROR_LOG_FILE_PATH = os.path.join(LOG_DIR, 'error.log')

# 创建logger记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 文件处理器，保存日志到文件
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# 文件日志
file_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILE_PATH, 
    maxBytes=1024 * 1024,  # 日志最大为1Mb
    backupCount=2,  # 最多备份2个日志
    encoding='utf8'
)

file_handler.setLevel(logging.INFO)

# 异常文件日志
error_file_handler = logging.handlers.RotatingFileHandler(
    filename=ERROR_LOG_FILE_PATH, 
    maxBytes=1024 * 1024,  # 日志最大为1Mb
    backupCount=2,  # 最多备份2个日志
    encoding='utf8'
)

error_file_handler.setLevel(logging.ERROR)

# 输出日志到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# 显示格式
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(error_file_handler)
logger.addHandler(stream_handler)


# 异常捕获
def error_callback(exc_type, exc_value, exc_traceback):
    logger.error("", exc_info=(
       exc_type, exc_value, exc_traceback))


sys.excepthook = error_callback


logger.debug('日志初始化完毕')
