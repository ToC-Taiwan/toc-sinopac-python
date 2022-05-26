import random
import string
import threading
import typing
from concurrent import futures
from datetime import datetime
from queue import Queue
from re import search

import grpc
import numpy as np
import shioaji as sj

import sinopac_forwarder_pb2
import sinopac_forwarder_pb2_grpc
from logger import logger
from sinopac import Sinopac
from sinopac_worker import SinopacWorker

SERVER_TOKEN = ''.join(random.choice(string.ascii_letters) for _ in range(50))
WORKERS: SinopacWorker


class gRPCFetchData(sinopac_forwarder_pb2_grpc.SinopacForwarderServicer):
    def GetServerToken(self, request, _):
        '''
        HealthCheck _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return sinopac_forwarder_pb2.TokenResponse(token=SERVER_TOKEN)

    def GetAllStockDetail(self, request, _):
        '''
        GetAllStockDetail _summary_

        Args:
            request (_type_): _description_
            _ (_type_): _description_

        Returns:
            _type_: _description_
        '''
        response = sinopac_forwarder_pb2.StockDetailResponse()
        worker = WORKERS.get()
        tse_001 = worker.get_contract_tse_001()
        response.stock.append(sinopac_forwarder_pb2.StockDetailMessage(
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
            response.stock.append(sinopac_forwarder_pb2.StockDetailMessage(
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
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
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
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
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
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
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
        response = sinopac_forwarder_pb2.StockHistoryTickResponse()
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
        response = sinopac_forwarder_pb2.StockHistoryKbarResponse()
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
        response = sinopac_forwarder_pb2.StockHistoryCloseResponse()
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

    def GetStockVolumeRank(self, request, _):
        response = sinopac_forwarder_pb2.StockVolumeRankResponse()
        worker = WORKERS.get()
        ranks = worker.get_stock_volume_rank_by_date(request.count, request.date)
        for result in ranks:
            response.data.append(sinopac_forwarder_pb2.StockVolumeRankMessage(
                date=result.date,
                code=result.code,
                name=result.name,
                ts=result.ts,
                open=result.open,
                high=result.high,
                low=result.low,
                close=result.close,
                price_range=result.price_range,
                tick_type=result.tick_type,
                change_price=result.change_price,
                change_type=result.change_type,
                average_price=result.average_price,
                volume=result.volume,
                total_volume=result.total_volume,
                amount=result.amount,
                total_amount=result.total_amount,
                yesterday_volume=result.yesterday_volume,
                volume_ratio=result.volume_ratio,
                buy_price=result.buy_price,
                buy_volume=result.buy_volume,
                sell_price=result.sell_price,
                sell_volume=result.sell_volume,
                bid_orders=result.bid_orders,
                bid_volumes=result.bid_volumes,
                ask_orders=result.ask_orders,
                ask_volumes=result.ask_volumes,
            ))
        return response

    def SubscribeStockTick(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeStockBidAsk(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockTick(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockBidAsk(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response


class gRPCLongConnection(sinopac_forwarder_pb2_grpc.LongConeectionServiceServicer):
    def __init__(self):
        self.event_queue = Queue()
        self.quote_queue = Queue()
        self.bid_ask_queue = Queue()
        self.order_queue = Queue()
        self.order_cb_lock = threading.Lock()

    def event_callback(self, resp_code: int, event_code: int, info: str, event: str):
        '''
        event_callback _summary_

        Args:
            resp_code (int): _description_
            event_code (int): _description_
            info (str): _description_
            event (str): _description_
        '''
        tmp = {
            'resp_code': str(resp_code),
            'event_code': str(event_code),
            'info': info,
            'event': event,
        }
        self.event_queue.put(tmp)

    def EventChannel(self, request, _):
        while True:
            if self.event_queue.empty():
                continue
            event = self.event_queue.get()
            yield sinopac_forwarder_pb2.EventResponse(
                resp_code=int(event['resp_code']),
                event_code=int(event['event_code']),
                info=event['info'],
                event=event['event'],
            )

    def quote_callback_v1(self, exchange: sj.Exchange, tick):
        '''
        quote_callback_v1 _summary_

        Args:
            exchange (sj.Exchange): _description_
            tick (_type_): _description_
        '''
        self.quote_queue.put(tick)
        logger.info('Exchange: %s, tick: %s', exchange, tick.code)

    def bid_ask_callback(self, exchange: sj.Exchange, bidask):
        '''
        bid_ask_callback _summary_

        Args:
            exchange (sj.Exchange): _description_
            bidask (_type_): _description_
        '''
        self.bid_ask_queue.put(bidask)
        logger.info('Exchange: %s, bidask: %s', exchange, bidask.code)

    def place_order_callback(self, order_state, order: dict):
        '''
        place_order_callback _summary_

        Args:
            order_state (_type_): _description_
            order (dict): _description_
        '''
        self.order_queue.put(order)
        if search('DEAL', order_state) is None:
            logger.info('%s %s %.2f %d %s %d %s %s %s %s',
                        order['contract']['code'],
                        order['order']['action'],
                        order['order']['price'],
                        order['order']['quantity'],
                        order_state,
                        order['status']['exchange_ts'],
                        order['order']['id'],
                        order['operation']['op_type'],
                        order['operation']['op_code'],
                        order['operation']['op_msg'],
                        )
        else:
            logger.info('%s %s %.2f %d %s %d %s %s',
                        order['code'],
                        order['action'],
                        order['price'],
                        order['quantity'],
                        order_state,
                        order['ts'],
                        order['trade_id'],
                        order['exchange_seq'],
                        )

    def order_status_callback(self, reply: typing.List[sj.order.Trade]):
        '''
        order_status_callback _summary_

        Args:
            reply (typing.List[sj.order.Trade]): _description_
        '''
        with self.order_cb_lock:
            if len(reply) != 0:
                for order in reply:
                    if order.status.order_datetime is None:
                        order.status.order_datetime = datetime.now()
                    order_price = int()
                    if order.status.modified_price != 0:
                        order_price = order.status.modified_price
                    else:
                        order_price = order.order.price
                    logger.info('Order status callback: %s %s %.2f %d %s %s %s',
                                order.contract.code,
                                order.order.action,
                                order_price,
                                order.order.quantity,
                                order.status.id,
                                order.status.status,
                                datetime.strftime(order.status.order_datetime, '%Y-%m-%d %H:%M:%S'),
                                )


def sinopac_snapshot_to_pb(result) -> sinopac_forwarder_pb2.StockSnapshotMessage:
    '''
    sinopac_snapshot_to_pb _summary_

    Args:
        result (_type_): _description_

    Returns:
        sinopac_forwarder_pb2.StockSnapshotMessage: _description_
    '''
    return sinopac_forwarder_pb2.StockSnapshotMessage(
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
            response.data.append(sinopac_forwarder_pb2.StockHistoryTickMessage(
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
            response.data.append(sinopac_forwarder_pb2.StockHistoryKbarMessage(
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
        response.data.append(sinopac_forwarder_pb2.StockHistoryCloseMessage(
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

    # gRPC servicer
    sinopac_forwarder_servicer = gRPCFetchData()
    long_connection_servicer = gRPCLongConnection()

    # set call back
    WORKERS.set_event_cb(long_connection_servicer.event_callback)
    WORKERS.set_quote_cb(long_connection_servicer.quote_callback_v1)
    WORKERS.set_bid_ask_cb(long_connection_servicer.bid_ask_callback)
    WORKERS.set_place_order_cb(long_connection_servicer.place_order_callback)
    WORKERS.set_order_status_cb(long_connection_servicer.order_status_callback)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sinopac_forwarder_pb2_grpc.add_SinopacForwarderServicer_to_server(sinopac_forwarder_servicer, server)
    sinopac_forwarder_pb2_grpc.add_LongConeectionServiceServicer_to_server(long_connection_servicer, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info('gRPC server started at port %s', port)
    server.wait_for_termination()
