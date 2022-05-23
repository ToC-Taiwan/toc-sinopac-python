import typing
from concurrent import futures

import grpc

import trade_pb2
import trade_pb2_grpc
from logger import logger
from sinopac import Sinopac


class ToCSinopacBackEnd(trade_pb2_grpc.ToCSinopacBackEndServicer):
    def HealthCheck(self, request, _):
        return trade_pb2.Echo(message=request.message)


def serve(port: str, main_connection: Sinopac, workers: typing.List[Sinopac]):
    logger.info('main_worker: %s', main_connection.list_accounts())
    for worker in workers:
        logger.info('workers: %s', worker.list_accounts())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trade_pb2_grpc.add_ToCSinopacBackEndServicer_to_server(ToCSinopacBackEnd(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()
