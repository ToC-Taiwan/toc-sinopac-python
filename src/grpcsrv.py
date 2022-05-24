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
from sinopac_worker import SinopacWorker

SERVER_TOKEN = ''.join(random.choice(string.ascii_letters) for _ in range(50))
WORKERS: SinopacWorker


class ToCSinopacBackEnd(trade_pb2_grpc.ToCSinopacBackEndServicer):
    def HealthCheck(self, request, _):
        '''
        HealthCheck _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return trade_pb2.TokenResponse(req_timestamp=request.timestamp, message=SERVER_TOKEN)

    def GetAllStockDetail(self, request, _):
        '''
        GetAllStockDetail _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        response = trade_pb2.StockDetailResponse(req_timestamp=request.timestamp)
        worker = WORKERS.get()
        tse_001 = worker.get_contract_tse_001()
        response.stock.append(trade_pb2.StockDetailMessage(
            exchange=tse_001.exchange,
            category=tse_001.category,
            code=tse_001.code,
            name=tse_001.name,
            reference=tse_001.reference,
            update_date=tse_001.update_date,
            day_trade=tse_001.day_trade,
        ))
        for row in worker.stock_num_list:
            contract = worker.get_contract_by_stock_num(row)
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
        '''
        GetAllStockSnapshot _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        contracts = []
        worker = WORKERS.get()
        for stock in worker.stock_num_list:
            contracts.append(worker.get_contract_by_stock_num(stock))
        snapshots = worker.snapshots(contracts)
        response = trade_pb2.StockSnapshotResponse(req_timestamp=request.timestamp)
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotTSE(self, request, _):
        '''
        GetStockSnapshotTSE _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        worker = WORKERS.get()
        snapshots = worker.snapshots([worker.get_contract_tse_001()])
        response = trade_pb2.StockSnapshotResponse(req_timestamp=request.timestamp)
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotByNumArr(self, request, _):
        '''
        GetStockSnapshotByNumArr _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        contracts = []
        worker = WORKERS.get()
        for stock in request.stock_num_arr:
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots = []
        threads = []
        lock = threading.Lock()
        for i, split in enumerate(splits):
            threads.append(threading.Thread(target=fill_sinopac_snapshot_arr, args=(split, snapshots, WORKERS.get(), lock)))
            threads[i].start()
        for t in threads:
            t.join()
        response = trade_pb2.StockSnapshotResponse(req_timestamp=request.timestamp)
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockHistoryTick(self, request, _):
        '''
        GetStockHistoryTick _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        response = trade_pb2.StockHistoryTickResponse(req_timestamp=request.timestamp)
        lock = threading.Lock()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_tick_response,
                args=(WORKERS.get().get_contract_by_stock_num(num),
                      num,
                      request.date,
                      response,
                      WORKERS.get(),
                      lock,))

            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryKbar(self, request, _):
        '''
        GetStockHistoryKbar _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        response = trade_pb2.StockHistoryKbarResponse(req_timestamp=request.timestamp)
        lock = threading.Lock()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_kbar_response,
                args=(WORKERS.get().get_contract_by_stock_num(num),
                      num,
                      request.date,
                      response,
                      WORKERS.get(),
                      lock,))

            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryClose(self, request, _):
        '''
        GetStockHistoryClose _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        response = trade_pb2.StockHistoryCloseResponse(req_timestamp=request.timestamp)
        lock = threading.Lock()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_close_response,
                args=(WORKERS.get().get_contract_by_stock_num(num),
                      num,
                      request.date,
                      response,
                      WORKERS.get(),
                      lock,))

            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response


def sinopac_snapshot_to_pb(result) -> trade_pb2.StockSnapshotMessage:
    '''
    sinopac_snapshot_to_pb _summary_

    Args:
        result (_type_): _description_

    Returns:
        trade_pb2.StockSnapshotMessage: _description_
    '''
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
    '''
    fill_sinopac_snapshot_arr _summary_

    Args:
        contracts (_type_): _description_
        snapshots (_type_): _description_
        sinopac (Sinopac): _description_
        mutex (_type_): _description_
    '''
    tmp = sinopac.snapshots(contracts)
    with mutex:
        snapshots.extend(tmp)


def fill_history_tick_response(contract, num, date, response, sinopac: Sinopac, mutex):
    '''
    fill_history_tick_response _summary_

    Args:
        contract (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
        mutex (_type_): _description_
    '''
    ticks = sinopac.ticks(contract, date)
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
            return
    with mutex:
        for pos in range(total_count):
            response.data.append(trade_pb2.StockHistoryTickMessage(
                stock_num=num,
                ts=ticks.ts[pos],
                close=ticks.close[pos],
                volume=ticks.volume[pos],
                bid_price=ticks.bid_price[pos],
                bid_volume=ticks.bid_volume[pos],
                ask_price=ticks.ask_price[pos],
                ask_volume=ticks.ask_volume[pos],
                tick_type=ticks.tick_type[pos],
            ))


def fill_history_kbar_response(contract, num, date, response, sinopac: Sinopac, mutex):
    '''
    fill_history_kbar_response _summary_

    Args:
        contract (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
        mutex (_type_): _description_
    '''
    kbar = sinopac.kbars(contract, date)
    total_count = len(kbar.ts)
    tmp_length = [
        len(kbar.Close),
        len(kbar.Open),
        len(kbar.High),
        len(kbar.Low),
        len(kbar.Volume),
    ]
    for length in tmp_length:
        if length - total_count != 0:
            return
    with mutex:
        for pos in range(total_count):
            response.data.append(trade_pb2.StockHistoryKbarMessage(
                stock_num=num,
                ts=kbar.ts[pos],
                Close=kbar.Close[pos],
                Open=kbar.Open[pos],
                High=kbar.High[pos],
                Low=kbar.Low[pos],
                Volume=kbar.Volume[pos],
            ))


def fill_history_close_response(contract, num, date, response, sinopac: Sinopac, mutex):
    '''
    fill_history_kbar_response _summary_

    Args:
        contract (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
        mutex (_type_): _description_
    '''
    close = sinopac.get_stock_last_close_by_date(contract, date)
    with mutex:
        response.data.append(trade_pb2.StockHistoryCloseMessage(
            code=num,
            close=close,
            date=date,
        ))


def serve(port: str, main_worker: Sinopac, workers: typing.List[Sinopac]):
    '''
    serve _summary_

    Args:
        port (str): _description_
        main_connection (Sinopac): _description_
        workers (typing.List[Sinopac]): _description_
    '''
    global WORKERS  # pylint: disable=global-statement
    WORKERS = SinopacWorker(main_worker, workers)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trade_pb2_grpc.add_ToCSinopacBackEndServicer_to_server(ToCSinopacBackEnd(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info('gRPC server started at port %s', port)
    server.wait_for_termination()
