"""SINOPAC PYTHON API FORWARDER"""


import os
import time

from prometheus_client import start_http_server

from env import RequiredEnv
from grpcsrv import GRPCServer
from logger import logger
from rabbitmq import RabbitMQS
from rabbitmq_setting import RabbitMQSetting
from sinopac import SinopacUser
from sinopac_worker import QueryDataLimit, SinopacWorkerPool

if __name__ == "__main__":
    env = RequiredEnv()

    PROMETHEUS_PORT = 6666
    start_http_server(PROMETHEUS_PORT)
    logger.info("sinopac prometheus server started at port %d", PROMETHEUS_PORT)

    try:
        rc = RabbitMQSetting(
            env.rabbitmq_user,
            env.rabbitmq_password,
            env.rabbitmq_host,
            env.rabbitmq_exchange,
        )
        rc.reset_rabbitmq_exchange()

    except RuntimeError:
        logger.error("reset rabbitmq exchange fail, retry after 30 seconds")
        time.sleep(30)
        os._exit(0)

    rabbit = RabbitMQS(
        env.rabbitmq_url,
        env.rabbitmq_exchange,
        64,
    )

    worker_pool = SinopacWorkerPool(
        env.connection_count,
        SinopacUser(
            env.api_key,
            env.api_key_secret,
            env.person_id,
            env.ca_password,
        ),
        QueryDataLimit(
            data=env.request_data_limit_per_second,
            portfolio=env.request_portfolio_limit_per_second,
            order=env.request_order_limit_per_second,
        ),
    )
    worker_pool.set_event_cb(rabbit.event_callback)
    worker_pool.set_stock_quote_cb(rabbit.stock_quote_callback_v1)
    worker_pool.set_future_quote_cb(rabbit.future_quote_callback_v1)
    worker_pool.set_stock_bid_ask_cb(rabbit.stock_bid_ask_callback)
    worker_pool.set_future_bid_ask_cb(rabbit.future_bid_ask_callback)
    worker_pool.set_non_block_order_callback(rabbit.order_status_callback)

    try:
        server = GRPCServer(
            worker_pool=worker_pool,
            rabbit=rabbit,
        )
        server.serve(port=env.grpc_port)

    except RuntimeError:
        logger.error("runtime error, retry after 30 seconds")
        time.sleep(30)

    except KeyboardInterrupt:
        logger.info("keyboard interrupt")

    finally:
        logger.info("shutdown")
        worker_pool.logout()
        os._exit(0)
