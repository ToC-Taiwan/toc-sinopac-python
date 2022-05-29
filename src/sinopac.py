import random
import string
import threading
import time
from datetime import datetime

import shioaji as sj

from constant import DayTrade, SecurityType
from logger import logger

ORDER_STATUS_CB_LOCK = threading.Lock()


class Sinopac:  # pylint: disable=too-many-public-methods
    def __init__(self):
        self.__api = sj.Shioaji()
        self.__login_status = 0
        # public
        self.stock_num_list = []
        self.order_status_list = []
        # lock
        self.__login_lock = threading.Lock()
        self.__order_status_lock = threading.Lock()
        # simulate trade
        self.__simulation_lock = threading.Lock()
        self.__courent_simulation_count = {}

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

    def finish_simulation_order(self, order: sj.order.Trade, wait: int):
        '''
        finish_simulation_order: buy stock will be sell after wait seconds,
        sell stock will be buy after wait seconds

        Args:
            order (sj.order.Trade): sinopac original order
            wait (int): unit is second
        '''
        self.order_status_list.append(order)
        with self.__simulation_lock:
            buy_later = False
            if order.order.action == sj.constant.Action.Buy and self.__courent_simulation_count[order.contract.code] < 0:
                buy_later = True
                self.__courent_simulation_count[order.contract.code] += order.order.quantity
            if order.order.action == sj.constant.Action.Sell:
                self.__courent_simulation_count[order.contract.code] -= order.order.quantity

        time.sleep(wait)
        with self.__simulation_lock:
            for sim in self.order_status_list:
                if sim.status.id == order.status.id:
                    sim.status.status = sj.constant.Status.Filled
                    if sim.order.action == sj.constant.Action.Buy and buy_later is False:
                        self.__courent_simulation_count[sim.contract.code] += sim.order.quantity

    def buy_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
        '''
        buy_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_

        Returns:
            _type_: _description_
        '''
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account
        )
        contract = self.get_contract_by_stock_num(stock_num)

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != '':
                return TradeResult(trade.order.id, trade.status.status, '')
        else:
            with self.__simulation_lock:
                if self.__courent_simulation_count[stock_num] < 0 or quantity+self.__courent_simulation_count[stock_num] != 0:
                    return TradeResult('', '', 'should buy later')
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id=''.join(random.choice(string.ascii_lowercase+string.octdigits) for _ in range(8)),
                    status=sj.constant.Status.Submitted,
                    status_code='',
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
            threading.Thread(target=self.finish_simulation_order, args=(sim_order, random.randrange(15)+1)).start()
            return TradeResult(sim_order.status.id, sim_order.status.status, '')

        return TradeResult('', '', 'unknown error')

    def sell_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
        '''
        sell_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_
            sim (_type_): _description_

        Returns:
            _type_: _description_
        '''
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account
        )
        contract = self.get_contract_by_stock_num(stock_num)

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != '':
                return TradeResult(trade.order.id, trade.status.status, '')
        else:
            order_status = sj.order.OrderStatus(
                id=''.join(random.choice(string.ascii_lowercase+string.octdigits) for _ in range(8)),
                status=sj.constant.Status.Submitted,
                status_code='',
                order_datetime=datetime.now(),
                deals=[],
            )
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=order_status,
            )
            with self.__simulation_lock:
                if quantity > self.__courent_simulation_count[stock_num]:
                    return TradeResult('', '', 'quantity is too large')
            threading.Thread(target=self.finish_simulation_order, args=(sim_order, random.randrange(15)+1)).start()
            return TradeResult(sim_order.status.id, sim_order.status.status, '')

        return TradeResult('', '', 'unknown error')

    def sell_first_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
        '''
        sell_first_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_
            sim (_type_): _description_

        Returns:
            _type_: _description_
        '''
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            first_sell=sj.constant.StockFirstSell.Yes,
            account=self.__api.stock_account
        )
        contract = self.get_contract_by_stock_num(stock_num)

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != '':
                return TradeResult(trade.order.id, trade.status.status, '')
        else:
            order_status = sj.order.OrderStatus(
                id=''.join(random.choice(string.ascii_lowercase+string.octdigits) for _ in range(8)),
                status=sj.constant.Status.Submitted,
                status_code='',
                order_datetime=datetime.now(),
                deals=[],
            )
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=order_status,
            )
            with self.__simulation_lock:
                if self.__courent_simulation_count[stock_num] > 0:
                    return TradeResult('', '', 'can not sell first')
            threading.Thread(target=self.finish_simulation_order, args=(sim_order, random.randrange(15)+1)).start()
            return TradeResult(sim_order.status.id, sim_order.status.status, '')

        return TradeResult('', '', 'unknown error')

    def cancel_stock(self, order_id: str, sim: bool):
        '''
        cancel_stock _summary_

        Args:
            order_id (_type_): _description_
            sim (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if sim is False:
            cancel_order = None
            times = int()
            while True:
                self.update_local_order_status()
                for order in self.order_status_list:
                    if order.status.id == order_id:
                        cancel_order = order
                if cancel_order is not None or times >= 10:
                    break
                times += 1
            if cancel_order is None:
                return TradeResult(order_id, '', 'id_not_found')
            if cancel_order.status.status == sj.constant.Status.Cancelled:
                return TradeResult(order_id, '', 'id_already_cancelled')
            self.__api.cancel_order(cancel_order)
            times = 0
            while True:
                if times >= 10:
                    break
                self.update_local_order_status()
                for order in self.order_status_list:
                    if order.status.id == order_id and order.status.status == sj.constant.Status.Cancelled:
                        return TradeResult(order_id, order.status.status, '')
                times += 1
        else:
            for order in self.order_status_list:
                if order.status.id == order_id and order.status.status != sj.constant.Status.Cancelled:
                    order.status.status = sj.constant.Status.Cancelled
                    return TradeResult(order_id, order.status.status, '')

        return TradeResult('', '', 'unknown error')

    def get_order_status_from_local_by_order_id(self, order_id: str, sim: bool):
        '''
        get_order_status_from_local_by_order_id _summary_

        Args:
            order_id (_type_): _description_
            sim (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if sim is False:
            self.update_local_order_status()
        if len(self.order_status_list) == 0:
            return TradeResult('', '', 'order list is empty')
        for order in self.order_status_list:
            if order.status.id == order_id:
                return TradeResult(order_id, order.status.status, '')
        return TradeResult('', '', 'unknown error')

    def get_order_status(self, sim: bool):
        '''
        get_order_status _summary_

        Args:
            sim (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if sim is False:
            self.update_order_status_instant()
            return None
        return self.order_status_list


class TradeResult():
    def __init__(self, order_id: str, status: str, error: str):
        self.order_id = order_id
        self.status = status
        self.error = error
