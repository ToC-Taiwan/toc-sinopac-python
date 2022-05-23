import threading
import typing
from concurrent import futures

import grpc
import numpy as np

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
        tse_001 = MAIN_WORKER.get_contract_tse_001()
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
            contract = MAIN_WORKER.get_contract_by_stock_num(row)
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

    def GetAllStockSnapshot(self, request, _):
        contracts = []
        tmp = MAIN_WORKER.stock_num_list
        for stock in tmp:
            contracts.append(MAIN_WORKER.get_contract_by_stock_num(stock))
        snapshots = MAIN_WORKER.snapshots(contracts)
        response = trade_pb2.StockSnapshotResponse(req_timestamp=request.timestamp)
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotByNumArr(self, request, _):
        contracts = []
        tmp = request.stock_num_arr
        for stock in tmp:
            contracts.append(MAIN_WORKER.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, len(SINOPAC_WORKDER_LIST))
        snapshots = []
        threads = []
        lock = threading.Lock()
        for i, split in enumerate(splits):
            threads.append(threading.Thread(target=fill_sinopac_snapshot_arr, args=(split, snapshots, SINOPAC_WORKDER_LIST[i], lock)))
            threads[i].start()
        for t in threads:
            t.join()
        response = trade_pb2.StockSnapshotResponse(req_timestamp=request.timestamp)
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response


def serve(port: str, main_connection: Sinopac, workers: typing.List[Sinopac]):
    global MAIN_WORKER, SINOPAC_WORKDER_LIST  # pylint: disable=global-statement
    MAIN_WORKER = main_connection
    SINOPAC_WORKDER_LIST = workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trade_pb2_grpc.add_ToCSinopacBackEndServicer_to_server(ToCSinopacBackEnd(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info('gRPC server started at port %s', port)
    server.wait_for_termination()


def sinopac_snapshot_to_pb(result) -> trade_pb2.StockSnapshotMessage:
    tmp = trade_pb2.StockSnapshotMessage()
    tmp.ts = result.ts
    tmp.code = result.code
    tmp.exchange = result.exchange
    tmp.open = result.open
    tmp.high = result.high
    tmp.low = result.low
    tmp.close = result.close
    tmp.tick_type = result.tick_type
    tmp.change_price = result.change_price
    tmp.change_rate = result.change_rate
    tmp.change_type = result.change_type
    tmp.average_price = result.average_price
    tmp.volume = result.volume
    tmp.total_volume = result.total_volume
    tmp.amount = result.amount
    tmp.total_amount = result.total_amount
    tmp.yesterday_volume = result.yesterday_volume
    tmp.buy_price = result.buy_price
    tmp.buy_volume = result.buy_volume
    tmp.sell_price = result.sell_price
    tmp.sell_volume = result.sell_volume
    tmp.volume_ratio = result.volume_ratio
    return tmp


def fill_sinopac_snapshot_arr(contracts, snapshots, sinopac: Sinopac, mutex):
    tmp = sinopac.snapshots(contracts)
    with mutex:
        snapshots.extend(tmp)
