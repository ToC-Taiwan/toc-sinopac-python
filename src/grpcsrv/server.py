from concurrent import futures

import grpc

from logger import logger
from pb.forwarder import basic_pb2_grpc, history_pb2_grpc, realtime_pb2_grpc, subscribe_pb2_grpc, trade_pb2_grpc
from realtime_us import RealTimeUS
from simulator import Simulator
from worker_pool import WorkerPool

from .basic import RPCBasic
from .history import RPCHistory
from .realtime import RPCRealTime
from .subscribe import RPCSubscribe
from .trade import RPCTrade


class GRPCServer:
    def __init__(self, worker_pool: WorkerPool):
        logger.info("Shioaji version: %s", worker_pool.get_sj_version())

        # simulator
        simulator = Simulator(worker_pool.get_main())

        # gRPC servicer
        basic_servicer = RPCBasic(worker_pool)
        history_servicer = RPCHistory(worker_pool)
        realtime_servicer = RPCRealTime(RealTimeUS(), worker_pool)
        subscribe_servicer = RPCSubscribe(worker_pool)
        trade_servicer = RPCTrade(simulator, worker_pool)

        new_server = grpc.server(
            futures.ThreadPoolExecutor(),
            options=[
                (
                    "grpc.max_send_message_length",
                    1024 * 1024 * 1024,
                ),
                (
                    "grpc.max_receive_message_length",
                    1024 * 1024 * 1024,
                ),
            ],
        )
        basic_pb2_grpc.add_BasicDataInterfaceServicer_to_server(basic_servicer, new_server)
        history_pb2_grpc.add_HistoryDataInterfaceServicer_to_server(history_servicer, new_server)
        realtime_pb2_grpc.add_RealTimeDataInterfaceServicer_to_server(realtime_servicer, new_server)
        subscribe_pb2_grpc.add_SubscribeDataInterfaceServicer_to_server(subscribe_servicer, new_server)
        trade_pb2_grpc.add_TradeInterfaceServicer_to_server(trade_servicer, new_server)

        self.grpc_srv = new_server

    def serve(self, port: str):
        self.grpc_srv.add_insecure_port(f"[::]:{port}")
        self.grpc_srv.start()
        logger.info("gRPC Server started at port %s", port)
        self.grpc_srv.wait_for_termination()
