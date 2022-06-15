"""SINOPAC PYTHON API FORWARDER"""
from cron import init_schedule_job
from env import RequiredEnv
from grpcsrv import serve
from logger import logger
from rabbitmq_container import RabbitMQContainer
from sinopac import Sinopac

env = RequiredEnv()
person_id = env.person_id
password = env.password
ca_password = env.ca_password
grpc_port = env.grpc_port
connection_count = env.connection_count

# add schedule to exit the program
init_schedule_job()

# start rabbitmq container first
rc = RabbitMQContainer()
rc.run_rabbitmq()

MAIN_WORKER: Sinopac
SINOPAC_WORKER_POOL: list[Sinopac] = []

for i in range(int(connection_count)):
    logger.info("establish connection %d", i + 1)
    is_main = bool(i == 0)
    new_connection = Sinopac().login(person_id, password, ca_password, is_main)
    if is_main is True:
        MAIN_WORKER = new_connection
        # if do not let main worker be the first worker in the pool, then continue
        # continue
    SINOPAC_WORKER_POOL.append(new_connection)

serve(port=grpc_port, main_worker=MAIN_WORKER, workers=SINOPAC_WORKER_POOL, cfg=env)
