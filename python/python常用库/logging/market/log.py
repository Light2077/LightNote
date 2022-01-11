import os
import logging
import logging.handlers

# 创建logger记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 文件处理器，保存日志到文件
log_filedir = './logs'
log_filename = 'mylog.log'
log_filepath = os.path.join(log_filedir, log_filename)
if not os.path.isdir(log_filedir):
    os.makedirs(log_filedir)

file_handler = logging.handlers.RotatingFileHandler(
    filename=log_filepath, 
    maxBytes=10,  # 日志最大为1m
    backupCount=2,  # 最多备份5个日志
    encoding='utf8'
)

file_handler.setLevel(logging.DEBUG)

# 输出日志到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 显示格式
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug('日志初始化完毕')
