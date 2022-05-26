import threading

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

    def login(self, person_id: str, passwd: str, ca_passwd: str, is_first: bool):
        '''
        login _summary_

        Args:
            person_id (str): _description_
            passwd (str): _description_
            ca_passwd (str): _description_
            is_first (bool): _description_

        Returns:
            _type_: _description_
        '''
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
        '''
        login_cb _summary_

        Args:
            security_type (_type_): _description_
        '''
        with self.__login_lock:
            if security_type.value in [item.value for item in SecurityType]:
                self.__login_status += 25
                logger.info('login progress: %d%%, %s', self.__login_status, security_type)

    def set_event_callback(self, func):
        '''
        set_event_callback _summary_

        Args:
            security_type (_type_): _description_
        '''
        self.__api.quote.set_event_callback(func)

    def set_on_tick_stk_v1_callback(self, func):
        '''
        set_on_tick_stk_v1_callback _summary_

        Args:
            func (_type_): _description_
        '''
        self.__api.quote.set_on_tick_stk_v1_callback(func)

    def set_on_bidask_stk_v1_callback(self, func):
        '''
        set_on_bidask_stk_v1_callback _summary_

        Args:
            func (_type_): _description_
        '''
        self.__api.quote.set_on_bidask_stk_v1_callback(func)

    def set_order_callback(self, func):
        '''
        set_order_callback _summary_

        Args:
            func (_type_): _description_
        '''
        self.__api.set_order_callback(func)

    def set_order_status_callback(self, func):
        '''
        set_order_status_callback _summary_

        Args:
            func (_type_): _description_
        '''
        self.order_status_callback = func

    def list_accounts(self):
        '''
        list_accounts _summary_

        Returns:
            _type_: _description_
        '''
        return self.__api.list_accounts()

    def fill_stock_num_list(self):
        '''
        fill_stock_num_list _summary_
        '''
        for all_contract in self.__api.Contracts.Stocks:
            for day_trade_stock in all_contract:
                if day_trade_stock.day_trade == DayTrade.Yes.value:
                    self.stock_num_list.append(day_trade_stock.code)
        while True:
            if len(self.stock_num_list) != 0:
                break
        logger.info('Filling stock_num_list, total: %d', len(self.stock_num_list))

    def update_order_status_instant(self):
        '''
        update_order_status_instant _summary_
        '''
        self.__api.update_status(timeout=0, cb=self.order_status_callback)

    def update_local_order_status(self):
        '''
        update_local_order_status _summary_
        '''
        with self.__order_status_lock:
            self.__api.update_status()
            self.order_status_list = self.__api.list_trades()

    def snapshots(self, contracts):
        '''
        snapshots _summary_

        Args:
            contracts (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.snapshots(contracts)

    def get_contract_tse_001(self):
        '''
        get_contract_tse_001 _summary_

        Returns:
            _type_: _description_
        '''
        return self.__api.Contracts.Indexs.TSE.TSE001

    def get_contract_by_stock_num(self, num):
        '''
        get_contract_by_stock_num _summary_

        Args:
            num (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.Contracts.Stocks[num]

    def ticks(self, contract, date):
        '''
        ticks _summary_

        Args:
            contract (_type_): _description_
            date (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.ticks(contract, date)

    def kbars(self, contract, date):
        '''
        kbars _summary_

        Args:
            contract (_type_): _description_
            date (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.kbars(
            contract=contract,
            start=date,
            end=date,
        )

    def get_stock_last_close_by_date(self, contract, date):
        '''
        kbars _summary_

        Args:
            contract (_type_): _description_
            date (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.quote.ticks(
            contract=contract,
            date=date,
            query_type=sj.constant.TicksQueryType.LastCount,
            last_cnt=1,
        ).close[0]

    def get_stock_volume_rank_by_date(self, count, date):
        '''
        kbars _summary_

        Args:
            contract (_type_): _description_
            date (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return self.__api.scanners(
            scanner_type=sj.constant.ScannerType.VolumeRank,
            count=count,
            date=date,
        )

    def subscribe_stock_tick(self, stock_num):
        '''
        subscribe_stock_tick _summary_

        Args:
            count (_type_): _description_
            date (_type_): _description_
        '''
        try:
            self.__api.quote.subscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def unsubscribe_stock_tick(self, stock_num):
        '''
        unsubscribe_stock_tick _summary_

        Args:
            stock_num (_type_): _description_
        '''
        try:
            self.__api.quote.unsubscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def subscribe_stock_bidask(self, stock_num):
        '''
        subscribe_stock_bidask _summary_

        Args:
            stock_num (_type_): _description_
        '''
        try:
            self.__api.quote.subscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def unsubscribe_stock_bidask(self, stock_num):
        '''
        unsubscribe_stock_bidask _summary_

        Args:
            stock_num (_type_): _description_
        '''
        try:
            self.__api.quote.unsubscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num
