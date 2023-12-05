import logging
from datetime import datetime

from env import RequiredEnv

LOG_FORMAT = str()
env = RequiredEnv()

if env.log_format == "json":
    LOG_FORMAT = '{"time":"%(asctime)s","user":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
else:
    LOG_FORMAT = "%(levelname)s[%(asctime)s] %(message)s"


class RFC3339Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        local_time = datetime.fromtimestamp(record.created).astimezone()
        return local_time.isoformat(timespec="seconds")


formatter = RFC3339Formatter()
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%d")}-toc-sinopac-python.log')

console_handler.setFormatter(RFC3339Formatter(fmt=LOG_FORMAT))
file_handler.setFormatter(RFC3339Formatter(fmt=LOG_FORMAT))

logging.addLevelName(50, "CRIT")
logging.addLevelName(40, "ERRO")
logging.addLevelName(30, "WARN")
logging.addLevelName(20, "INFO")
logging.addLevelName(10, "DEBU")

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
