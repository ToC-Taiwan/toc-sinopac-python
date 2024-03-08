"""SINOPAC PYTHON API FORWARDER"""

from prometheus_client import start_http_server

from env import RequiredEnv
from grpcsrv.server import GRPCServer
from logger import logger
from mqtt import MQTT
from sinopac import ShioajiAuth
from worker_pool import QueryDataLimit, WorkerPool

if __name__ == "__main__":
    env = RequiredEnv()

    PROMETHEUS_PORT = 6666
    start_http_server(PROMETHEUS_PORT)
    logger.info("sinopac forwarder prometheus started at port %d", PROMETHEUS_PORT)

    mq = MQTT("127.0.0.1", 18883)
    worker_pool = WorkerPool(
        env.connection_count,
        ShioajiAuth(
            env.api_key,
            env.api_key_secret,
            env.person_id,
            env.ca_password,
        ),
        mq,
        QueryDataLimit(
            data=env.request_data_limit_per_second,
            portfolio=env.request_portfolio_limit_per_second,
            order=env.request_order_limit_per_second,
        ),
    )

    try:
        GRPCServer(worker_pool=worker_pool).serve(port=env.grpc_port)

    except Exception as e:
        logger.error(str(e))

    finally:
        worker_pool.logout_and_exit()
