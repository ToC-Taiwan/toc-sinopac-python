"""SINOPAC PYTHON API FORWARDER"""


import os
import time

from prometheus_client import start_http_server

from cron import init_schedule_job
from env import RequiredEnv
from grpcsrv import serve
from logger import logger
from rabbitmq_setting import RabbitMQSetting
from sinopac import Sinopac, SinopacUser

env = RequiredEnv()
API_KEY = env.api_key
API_KEY_SECRET = env.api_key_secret
PERSON_ID = env.person_id
CA_PASSWORD = env.ca_password
GRPC_PORT = env.grpc_port
CONNECTION_COUNT = env.connection_count

start_http_server(8887)

# add schedule to exit the program
init_schedule_job()

# start rabbitmq container first
rc = RabbitMQSetting()
rc.reset_rabbitmq_exchange()

main_trader: Sinopac
worker_pool: list[Sinopac] = []

for i in range(CONNECTION_COUNT):
    logger.info("establish connection %d", i + 1)
    is_main = bool(i == 0)
    new_connection = Sinopac().login(
        SinopacUser(
            API_KEY,
            API_KEY_SECRET,
            PERSON_ID,
            CA_PASSWORD,
        ),
        is_main,
    )
    if is_main is True:
        main_trader = new_connection
        # if do not let main worker be the first worker in the pool, then continue
        continue
    worker_pool.append(new_connection)

try:
    serve(
        port=str(GRPC_PORT),
        main_trader=main_trader,
        workers=worker_pool,
        cfg=env,
    )

except RuntimeError:
    logger.error("runtime error, retry after 30 seconds")
    time.sleep(30)
    os._exit(0)

except KeyboardInterrupt:
    os._exit(0)
