import logging
from datetime import datetime

from env import RequiredEnv

log_format = str()
env = RequiredEnv()

if env.log_format == "json":
    log_format = '{"time":"%(asctime)s","user":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
else:
    log_format = "%(levelname)s[%(asctime)s] %(message)s"


console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    f'./logs/{datetime.now().strftime("%Y-%m-%d")}-toc-sinopac-python.log'
)

console_handler.setFormatter(logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S"))
file_handler.setFormatter(logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S"))

logging.addLevelName(50, "CRIT")
logging.addLevelName(40, "ERRO")
logging.addLevelName(30, "WARN")
logging.addLevelName(20, "INFO")
logging.addLevelName(10, "DEBU")

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
