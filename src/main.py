"""SINOPAC PYTHON API FORWARDER"""
import os
import time

from cron import init_schedule_job
from env import RequiredEnv
from grpcsrv import serve
from logger import logger
from rabbitmq_setting import RabbitMQSetting
from sinopac import Sinopac, SinopacUser

env = RequiredEnv()
person_id = env.person_id
password = env.password
ca_password = env.ca_password
grpc_port = env.grpc_port
connection_count = env.connection_count

# add schedule to exit the program
init_schedule_job()

# start rabbitmq container first
rc = RabbitMQSetting()
rc.reset_rabbitmq_exchange()

MAIN_WORKER: Sinopac
SINOPAC_WORKER_POOL: list[Sinopac] = []

for i in range(connection_count):
    logger.info("establish connection %d", i + 1)
    is_main = bool(i == 0)
    new_connection = Sinopac().login(
        SinopacUser(person_id, password, ca_password), is_main
    )
    if is_main is True:
        MAIN_WORKER = new_connection
        # if do not let main worker be the first worker in the pool, then continue
        continue
    SINOPAC_WORKER_POOL.append(new_connection)
    logger.info("establish connection done")

try:
    serve(
        port=str(grpc_port),
        main_worker=MAIN_WORKER,
        workers=SINOPAC_WORKER_POOL,
        cfg=env,
    )

except RuntimeError:
    logger.error("runtime error, retry after 30 seconds")
    time.sleep(30)
    os._exit(1)
