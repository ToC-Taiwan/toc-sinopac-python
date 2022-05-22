import logging
import os
from datetime import datetime

deployment = os.getenv('DEPLOYMENT')
log_format = str()
extension_name = str()

if deployment == 'docker':
    log_format = '{"time":"%(asctime)s","user":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
    extension_name = '.json'
else:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    extension_name = '.log'

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('./logs/'+datetime.now().strftime("%Y-%m-%d")+extension_name)

console_handler.setFormatter(logging.Formatter(log_format))
file_handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.info('Logger initialized')
