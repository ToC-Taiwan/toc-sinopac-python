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
api_key = env.api_key
api_key_secret = env.api_key_secret
person_id = env.person_id
ca_password = env.ca_password
grpc_port = env.grpc_port
connection_count = env.connection_count

start_http_server(8887)

# add schedule to exit the program
init_schedule_job()

# start rabbitmq container first
rc = RabbitMQSetting()
rc.reset_rabbitmq_exchange()

main_trader: Sinopac
worker_pool: list[Sinopac] = []

for i in range(connection_count):
    logger.info("establish connection %d", i + 1)
    is_main = bool(i == 0)
    new_connection = Sinopac().login(
        SinopacUser(
            api_key,
            api_key_secret,
            person_id,
            ca_password,
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
        port=str(grpc_port),
        main_trader=main_trader,
        workers=worker_pool,
        cfg=env,
    )

except RuntimeError:
    logger.error("runtime error, retry after 30 seconds")
    time.sleep(30)
    os._exit(1)
