import threading
from pprint import pformat
from re import search

import shioaji as sj

from logger import logger


class Sinopac:
    def __init__(self):
        self.api = sj.Shioaji()
        self.login_lock = threading.Lock()
        self.login_status = 0
        self.api.set_order_callback(place_order_callback)
        self.api.quote.set_event_callback(event_callback)
        self.api.quote.set_on_tick_stk_v1_callback(quote_callback_v1)
        self.api.quote.set_on_bidask_stk_v1_callback(bid_ask_callback)

    def login(self, person_id: str, passwd: str, ca_passwd: str, is_first: bool):
        self.api.login(
            person_id=person_id,
            passwd=passwd,
            contracts_cb=self.login_cb,
            subscribe_trade=is_first,
            fetch_contract=is_first,
        )
        while True:
            if self.login_status == 100:
                break
        self.api.activate_ca(
            ca_path=f'./data/{person_id}.pfx',
            ca_passwd=ca_passwd,
            person_id=person_id,
        )
        return self

    def login_cb(self, security_type: sj.constant.SecurityType):
        with self.login_lock:
            if security_type.value in ('STK', 'IND', 'FUT', 'OPT'):
                self.login_status += 25
                logger.info('login progress: %d%%, %s', self.login_status, security_type)

    def list_accounts(self):
        return self.api.list_accounts()


def place_order_callback(order_state: sj.constant.OrderState, order: dict):
    '''Place order callback'''
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


def quote_callback_v1(exchange: sj.Exchange, tick: sj.TickSTKv1):
    logger.info('Exchange: %s, tick: %s', exchange, tick.code)


def bid_ask_callback(exchange: sj.Exchange, bidask: sj.BidAskSTKv1):
    logger.info('Exchange: %s, bidask: %s', exchange, bidask.code)
