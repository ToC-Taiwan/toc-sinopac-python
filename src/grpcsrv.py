import typing
from concurrent import futures

import grpc

import trade_pb2
import trade_pb2_grpc
from logger import logger
from sinopac import Sinopac

MAIN_WORKER: Sinopac
SINOPAC_WORKDER_LIST: typing.List[Sinopac] = []


class ToCSinopacBackEnd(trade_pb2_grpc.ToCSinopacBackEndServicer):
    def HealthCheck(self, request, _):
        return trade_pb2.Echo(message=request.message)

    def GetAllStockDetail(self, request, _):
        response = trade_pb2.StockDetailResponse(req_timestamp=request.timestamp)
        tse_001 = MAIN_WORKER.api.Contracts.Indexs.TSE.TSE001
        res = trade_pb2.StockDetailMessage()
        res.exchange = tse_001.exchange
        res.category = tse_001.category
        res.code = tse_001.code
        res.name = tse_001.name
        res.reference = tse_001.reference
        res.update_date = tse_001.update_date
        res.day_trade = tse_001.day_trade
        response.stock.append(res)
        tmp = MAIN_WORKER.stock_num_list
        for row in tmp:
            contract = MAIN_WORKER.api.Contracts.Stocks[row]
            if contract is None:
                tmp.remove(row)
                logger.info('%s is no data', row)
                continue
            res = trade_pb2.StockDetailMessage()
            res.exchange = contract.exchange
            res.category = contract.category
            res.code = contract.code
            res.name = contract.name
            res.reference = contract.reference
            res.update_date = contract.update_date
            res.day_trade = contract.day_trade
            response.stock.append(res)
        return response


def serve(port: str, main_connection: Sinopac, workers: typing.List[Sinopac]):
    global MAIN_WORKER, SINOPAC_WORKDER_LIST
    MAIN_WORKER = main_connection
    SINOPAC_WORKDER_LIST = workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trade_pb2_grpc.add_ToCSinopacBackEndServicer_to_server(ToCSinopacBackEnd(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info('gRPC server started at port %s', port)
    server.wait_for_termination()
