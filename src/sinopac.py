import threading
import typing
from datetime import datetime
from pprint import pformat
from re import search

import shioaji as sj

from constant import DayTrade, SecurityType
from logger import logger

ORDER_STATUS_CB_LOCK = threading.Lock()


class Sinopac:
    def __init__(self):
        self.__api = sj.Shioaji()
        self.__login_status = 0
        # public
        self.stock_num_list = []
        self.order_status_list = []
        # lock
        self.__login_lock = threading.Lock()
        self.__order_status_lock = threading.Lock()
        # callback
        self.__api.set_order_callback(place_order_callback)
        self.__api.quote.set_event_callback(event_callback)
        self.__api.quote.set_on_tick_stk_v1_callback(quote_callback_v1)
        self.__api.quote.set_on_bidask_stk_v1_callback(bid_ask_callback)

    def login(self, person_id: str, passwd: str, ca_passwd: str, is_first: bool):
        self.__api.login(
            person_id=person_id,
            passwd=passwd,
            contracts_cb=self.login_cb,
            subscribe_trade=is_first,
            fetch_contract=is_first,
        )
        while True:
            if self.__login_status == 100:
                break
        self.__api.activate_ca(
            ca_path=f'./data/{person_id}.pfx',
            ca_passwd=ca_passwd,
            person_id=person_id,
        )
        self.fill_stock_num_list()
        return self

    def login_cb(self, security_type):
        with self.__login_lock:
            if security_type.value in [item.value for item in SecurityType]:
                self.__login_status += 25
                logger.info('login progress: %d%%, %s', self.__login_status, security_type)

    def list_accounts(self):
        return self.__api.list_accounts()

    def fill_stock_num_list(self):
        for all_contract in self.__api.Contracts.Stocks:
            for day_trade_stock in all_contract:
                if day_trade_stock.day_trade == DayTrade.Yes.value:
                    self.stock_num_list.append(day_trade_stock.code)
        while True:
            if len(self.stock_num_list) != 0:
                break
        logger.info('Filling stock_num_list, total: %d', len(self.stock_num_list))

    def update_order_status_instant(self):
        self.__api.update_status(timeout=0, cb=order_status_callback)

    def update_local_order_status(self):
        with self.__order_status_lock:
            self.__api.update_status()
            self.order_status_list = self.__api.list_trades()

    def snapshots(self, contracts):
        return self.__api.snapshots(contracts)

    def get_contract_tse_001(self):
        return self.__api.Contracts.Indexs.TSE.TSE001

    def get_contract_by_stock_num(self, num):
        return self.__api.Contracts.Stocks[num]

    def ticks(self, contract, date):
        return self.__api.ticks(contract, date)


def place_order_callback(order_state, order: dict):
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


def event_callback(resp_code: int, event_code: int, info: str, event: str):
    length_arr = [
        len(str(resp_code)),
        len(str(event_code)),
        len(info),
        len(event),
    ]
    tmp = {
        'resp_code': resp_code,
        'event_code': event_code,
        'info': info,
        'event': event,
    }
    logger.info(pformat(tmp, width=max(length_arr)))


def quote_callback_v1(exchange: sj.Exchange, tick):
    logger.info('Exchange: %s, tick: %s', exchange, tick.code)


def bid_ask_callback(exchange: sj.Exchange, bidask):
    logger.info('Exchange: %s, bidask: %s', exchange, bidask.code)


def order_status_callback(reply: typing.List[sj.order.Trade]):
    with ORDER_STATUS_CB_LOCK:
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
