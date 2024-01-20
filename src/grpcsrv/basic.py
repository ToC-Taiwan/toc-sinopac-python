import threading
import time

import google.protobuf.empty_pb2
import grpc

from logger import logger
from pb.forwarder import basic_pb2, basic_pb2_grpc
from sinopac_worker import SinopacWorkerPool


class RPCBasic(basic_pb2_grpc.BasicDataInterfaceServicer):
    def __init__(
        self,
        workers: SinopacWorkerPool,
    ):
        self.workers = workers

    def CreateLongConnection(self, request_iterator, context: grpc.ServicerContext):
        logger.info("new sinopac gRPC client connected")
        while context.is_active():
            time.sleep(1)
        self.workers.logout_and_exit()

    def Terminate(self, request, _):
        threading.Thread(target=self.wait_and_terminate, daemon=True).start()
        return google.protobuf.empty_pb2.Empty()

    def CheckUsage(self, request, _):
        usage = self.workers.check_usage()
        return basic_pb2.ShioajiUsage(
            connections=usage.connections,
            bytes=usage.bytes,
            limit_bytes=usage.limit_bytes,
            remaining_bytes=usage.remaining_bytes,
        )

    def Login(self, request, _):
        self.workers.login()
        return google.protobuf.empty_pb2.Empty()

    def wait_and_terminate(self):
        time.sleep(3)
        self.workers.logout_and_exit()

    def GetAllStockDetail(self, request, _):
        response = basic_pb2.StockDetailResponse()
        for contract in self.workers.get_stock_contract_list():
            response.stock.append(
                basic_pb2.StockDetailMessage(
                    exchange=contract.exchange,
                    category=contract.category,
                    code=contract.code,
                    name=contract.name,
                    reference=contract.reference,
                    update_date=contract.update_date,
                    day_trade=contract.day_trade,
                )
            )
        return response

    def GetAllFutureDetail(self, request, _):
        response = basic_pb2.FutureDetailResponse()
        for contract in self.workers.get_future_contract_list():
            response.future.append(
                basic_pb2.FutureDetailMessage(
                    code=contract.code,
                    symbol=contract.symbol,
                    name=contract.name,
                    category=contract.category,
                    delivery_month=contract.delivery_month,
                    delivery_date=contract.delivery_date,
                    underlying_kind=contract.underlying_kind,
                    unit=contract.unit,
                    limit_up=contract.limit_up,
                    limit_down=contract.limit_down,
                    reference=contract.reference,
                    update_date=contract.update_date,
                )
            )
        return response

    def GetAllOptionDetail(self, request, _):
        response = basic_pb2.OptionDetailResponse()
        for contract in self.workers.get_option_contract_list():
            response.option.append(
                basic_pb2.OptionDetailMessage(
                    code=contract.code,
                    symbol=contract.symbol,
                    name=contract.name,
                    category=contract.category,
                    delivery_month=contract.delivery_month,
                    delivery_date=contract.delivery_date,
                    strike_price=contract.strike_price,
                    option_right=contract.option_right,
                    underlying_kind=contract.underlying_kind,
                    unit=contract.unit,
                    limit_up=contract.limit_up,
                    limit_down=contract.limit_down,
                    reference=contract.reference,
                    update_date=contract.update_date,
                )
            )
        return response
