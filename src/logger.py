import logging
from datetime import datetime

from env import RequiredEnv

log_format = str()
env = RequiredEnv()

if env.log_format == "json":
    log_format = '{"time":"%(asctime)s","user":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
else:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    f'./logs/{datetime.now().strftime("%Y-%m-%d")}-toc-sinopac-python.log'
)
console_handler.setFormatter(logging.Formatter(log_format))
file_handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
