"""SINOPAC PYTHON API FORWARDER"""

import os
import time

from prometheus_client import start_http_server

from env import RequiredEnv
from grpcsrv.server import GRPCServer
from logger import logger
from rabbitmq import RabbitMQ
from rabbitmq_api import RabbitAPI
from sinopac import ShioajiAuth
from worker_pool import QueryDataLimit, WorkerPool

if __name__ == "__main__":
    env = RequiredEnv()

    PROMETHEUS_PORT = 6666
    start_http_server(PROMETHEUS_PORT)
    logger.info("sinopac forwarder prometheus started at port %d", PROMETHEUS_PORT)

    try:
        RabbitAPI(
            env.rabbitmq_user,
            env.rabbitmq_password,
            env.rabbitmq_host,
            env.rabbitmq_exchange,
        ).reset_rabbitmq_exchange()

    except RuntimeError:
        logger.error("reset rabbitmq exchange fail, retry after 30 seconds")
        time.sleep(30)
        os._exit(0)

    rabbit = RabbitMQ(env.rabbitmq_url, env.rabbitmq_exchange)
    worker_pool = WorkerPool(
        env.connection_count,
        ShioajiAuth(
            env.api_key,
            env.api_key_secret,
            env.person_id,
            env.ca_password,
        ),
        rabbit,
        QueryDataLimit(
            data=env.request_data_limit_per_second,
            portfolio=env.request_portfolio_limit_per_second,
            order=env.request_order_limit_per_second,
        ),
    )

    try:
        server = GRPCServer(
            worker_pool=worker_pool,
            rabbit=rabbit,
        )
        server.serve(port=env.grpc_port)

    except Exception as e:
        logger.error(str(e))

    finally:
        worker_pool.logout_and_exit()
