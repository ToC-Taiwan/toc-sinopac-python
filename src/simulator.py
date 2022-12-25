import random
import string
import threading
import time
from datetime import datetime

import shioaji as sj

from logger import logger
from sinopac import OrderStatus, Sinopac


class Simulator:
    def __init__(self, sinopac: Sinopac):
        self.sinopac = sinopac
        self.__api = sinopac.get_sj_api()

        # key: stock_num or code, value: count
        self.__simulation_lock = threading.Lock()
        self.__simulation_count_map: dict[str, int] = {}

        self.stock_num_list = self.sinopac.get_stock_num_list()
        for stock in self.stock_num_list:
            self.__simulation_count_map[stock] = 0

        self.future_code_list = self.sinopac.get_future_code_list()
        for future in self.future_code_list:
            self.__simulation_count_map[future] = 0

        self.__order_status_lock = threading.Lock()
        self.order_status_list: list[sj.order.Trade] = []

    def get_order_status(self):
        return self.order_status_list

    def get_order_status_by_id(self, order_id: str):
        if len(self.order_status_list) == 0:
            return OrderStatus("", "", "order list is empty")

        for order in self.order_status_list:
            if order.status.id == order_id:
                return OrderStatus(order_id, order.status.status, "")

        return OrderStatus("", "", "order not found")

    def reset_simulator(self):
        clear_count = int()
        with self.__simulation_lock:
            for stock in self.stock_num_list:
                s = self.__simulation_count_map[stock]
                if s != 0:
                    self.__simulation_count_map[stock] = 0
                    clear_count += 1
            for future in self.future_code_list:
                f = self.__simulation_count_map[future]
                if f != 0:
                    self.__simulation_count_map[future] = 0
                    clear_count += 1
            if clear_count > 0:
                logger.info("clear %d simulation order", clear_count)

        with self.__order_status_lock:
            self.order_status_list = []

    def finish_simulation_order(self, order: sj.order.Trade, wait: int):
        self.order_status_list.append(order)
        with self.__simulation_lock:
            buy_later = False
            if order.order.action == sj.constant.Action.Buy and self.__simulation_count_map[order.contract.code] < 0:
                buy_later = True
                self.__simulation_count_map[order.contract.code] += order.order.quantity
            if order.order.action == sj.constant.Action.Sell:
                self.__simulation_count_map[order.contract.code] -= order.order.quantity

        time.sleep(wait)
        with self.__simulation_lock:
            for sim in self.order_status_list:
                if sim.status.id == order.status.id:
                    sim.status.status = sj.constant.Status.Filled
                    if sim.order.action == sj.constant.Action.Buy and buy_later is False:
                        self.__simulation_count_map[sim.contract.code] += sim.order.quantity

    def buy_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account,
        )
        contract = self.sinopac.get_contract_by_stock_num(stock_num)

        with self.__simulation_lock:
            if self.__simulation_count_map[stock_num] < 0:
                if quantity + self.__simulation_count_map[stock_num] > 0:
                    return OrderStatus("", "", "buy later quantity is too big")
        sim_order = sj.order.Trade(
            contract=contract,
            order=order,
            status=sj.order.OrderStatus(
                id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                status=sj.constant.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account,
        )
        contract = self.sinopac.get_contract_by_stock_num(stock_num)

        with self.__simulation_lock:
            if quantity > self.__simulation_count_map[stock_num]:
                return OrderStatus("", "", "quantity is too big")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_first_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            first_sell=sj.constant.StockFirstSell.Yes,
            account=self.__api.stock_account,
        )
        contract = self.sinopac.get_contract_by_stock_num(stock_num)

        with self.__simulation_lock:
            if self.__simulation_count_map[stock_num] > 0:
                return OrderStatus("", "", "can not sell first")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def cancel_stock(self, order_id: str):
        for order in self.order_status_list:
            if order.status.id == order_id and order.status.status != sj.constant.Status.Cancelled:
                order.status.status = sj.constant.Status.Cancelled
                return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")

    def buy_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.sinopac.get_contract_by_future_code(code)
        with self.__simulation_lock:
            if self.__simulation_count_map[code] < 0:
                if quantity + self.__simulation_count_map[code] > 0:
                    return OrderStatus("", "", "buy later quantity is too big")
        sim_order = sj.order.Trade(
            contract=contract,
            order=order,
            status=sj.order.OrderStatus(
                id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                status=sj.constant.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.sinopac.get_contract_by_future_code(code)
        with self.__simulation_lock:
            if quantity > self.__simulation_count_map[code]:
                return OrderStatus("", "", "quantity is too big")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_first_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.sinopac.get_contract_by_future_code(code)
        with self.__simulation_lock:
            if self.__simulation_count_map[code] > 0:
                return OrderStatus("", "", "can not sell first")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8)),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def cancel_future(self, order_id: str):
        for order in self.order_status_list:
            if order.status.id == order_id and order.status.status != sj.constant.Status.Cancelled:
                order.status.status = sj.constant.Status.Cancelled
                return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")
