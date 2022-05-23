import random
import string
import threading
import typing
from concurrent import futures

import grpc
import numpy as np

import trade_pb2
import trade_pb2_grpc
from logger import logger
from sinopac import Sinopac

SERVER_TOKEN = ''.join(random.choice(string.ascii_letters) for _ in range(50))
MAIN_WORKER: Sinopac
SINOPAC_WORKDER_LIST: typing.List[Sinopac] = []


class ToCSinopacBackEnd(trade_pb2_grpc.ToCSinopacBackEndServicer):
    def HealthCheck(self, request, _):
        return trade_pb2.TokenResponse(req_timestamp=request.timestamp, message=SERVER_TOKEN)

    def GetAllStockDetail(self, request, _):
        response = trade_pb2.StockDetailResponse(req_timestamp=request.timestamp)
        tse_001 = MAIN_WORKER.get_contract_tse_001()
        response.stock.append(trade_pb2.StockDetailMessage(
            exchange=tse_001.exchange,
            category=tse_001.category,
            code=tse_001.code,
            name=tse_001.name,
            reference=tse_001.reference,
            update_date=tse_001.update_date,
            day_trade=tse_001.day_trade,
        ))
        for row in MAIN_WORKER.stock_num_list:
            contract = MAIN_WORKER.get_contract_by_stock_num(row)
            if contract is None:
                logger.error('%s has no stock data', row)
                continue
            response.stock.append(trade_pb2.StockDetailMessage(
                exchange=contract.exchange,
                category=contract.category,
                code=contract.code,
                name=contract.name,
                reference=contract.reference,
                update_date=contract.update_date,
                day_trade=contract.day_trade,
            ))
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

    def GetStockSnapshotTSE(self, request, _):
        snapshots = MAIN_WORKER.snapshots([MAIN_WORKER.get_contract_tse_001()])
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

    def GetStockHistoryTick(self, request, _):
        response = trade_pb2.StockHistoryTickResponse(req_timestamp=request.timestamp)
        response.stock_num = request.stock_num
        response.date = request.date
        ticks = MAIN_WORKER.ticks(MAIN_WORKER.get_contract_by_stock_num(request.stock_num), request.date)
        total_count = len(ticks.ts)
        tmp_length = [
            len(ticks.close),
            len(ticks.tick_type),
            len(ticks.volume),
            len(ticks.bid_price),
            len(ticks.bid_volume),
            len(ticks.ask_price),
            len(ticks.ask_volume),
        ]
        for length in tmp_length:
            if length - total_count != 0:
                return trade_pb2.StockHistoryTickResponse()
        for pos in range(total_count):
            response.data.append(trade_pb2.StockHistoryTickMessage(
                ts=ticks.ts[pos],
                close=ticks.close[pos],
                volume=ticks.volume[pos],
                bid_price=ticks.bid_price[pos],
                bid_volume=ticks.bid_volume[pos],
                ask_price=ticks.ask_price[pos],
                ask_volume=ticks.ask_volume[pos],
                tick_type=ticks.tick_type[pos],
            ))
        return response


def sinopac_snapshot_to_pb(result) -> trade_pb2.StockSnapshotMessage:
    return trade_pb2.StockSnapshotMessage(
        ts=result.ts,
        code=result.code,
        exchange=result.exchange,
        open=result.open,
        high=result.high,
        low=result.low,
        close=result.close,
        tick_type=result.tick_type,
        change_price=result.change_price,
        change_rate=result.change_rate,
        change_type=result.change_type,
        average_price=result.average_price,
        volume=result.volume,
        total_volume=result.total_volume,
        amount=result.amount,
        total_amount=result.total_amount,
        yesterday_volume=result.yesterday_volume,
        buy_price=result.buy_price,
        buy_volume=result.buy_volume,
        sell_price=result.sell_price,
        sell_volume=result.sell_volume,
        volume_ratio=result.volume_ratio,
    )


def fill_sinopac_snapshot_arr(contracts, snapshots, sinopac: Sinopac, mutex):
    tmp = sinopac.snapshots(contracts)
    with mutex:
        snapshots.extend(tmp)


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
