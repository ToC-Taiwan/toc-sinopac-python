import logging
from datetime import datetime

from env import RequiredEnv

log_format = str()
extension_name = str()
env = RequiredEnv()

if env.deployment == "prod":
    log_format = '{"time":"%(asctime)s","user":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
    extension_name = "json"
else:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    extension_name = "log"

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    f'./logs/{datetime.now().strftime("%Y-%m-%d")}.{extension_name}'
)
console_handler.setFormatter(logging.Formatter(log_format))
file_handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
