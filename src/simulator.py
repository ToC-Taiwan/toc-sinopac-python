import random
import string
import threading
import time
from datetime import datetime

import shioaji as sj
import shioaji.constant as sc
from shioaji.order import Order, Trade

from logger import logger
from sinopac import OrderStatus, Sinopac


class Simulator:
    def __init__(self, sinopac: Sinopac):
        self.sinopac = sinopac
        self.__simulation_count_map: dict[str, int] = {}  # key: stock_num or code, value: count
        self.__simulation_lock = threading.Lock()

        self.__order_map: dict[str, Trade] = {}  # order_id: Trade
        self.__order_map_lock = threading.Lock()

    def finish_simulation_order(self, order: Trade, wait: int):
        self.insert_or_update_local_order(order)
        time.sleep(wait)
        if random.randint(1, 100) > 10:
            order.status.status = sc.Status.Filled
            order.status.deal_quantity = order.order.quantity
            self.insert_or_update_local_order(order)

    def buy_stock(self, stock_num: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(stock_num, 0)
            if current < 0:
                if quantity + current > 0:
                    return OrderStatus("", "", "buy later quantity is too big")
            self.__simulation_count_map[stock_num] = current + quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_stock_num(stock_num),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Buy,
                price_type=sc.StockPriceType.LMT,
                order_type=sc.OrderType.ROD,
                order_lot=sc.StockOrderLot.Common,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_stock(self, stock_num: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(stock_num, 0)
            if quantity > current:
                return OrderStatus("", "", "quantity is too big")
            self.__simulation_count_map[stock_num] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_stock_num(stock_num),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.StockPriceType.LMT,
                order_type=sc.OrderType.ROD,
                order_lot=sc.StockOrderLot.Common,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_first_stock(self, stock_num: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(stock_num, 0)
            if current > 0:
                return OrderStatus("", "", "can not sell first")
            self.__simulation_count_map[stock_num] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_stock_num(stock_num),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.StockPriceType.LMT,
                order_type=sc.OrderType.ROD,
                order_lot=sc.StockOrderLot.Common,
                daytrade_short=True,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, random.randrange(5) + 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def cancel_stock(self, order_id: str):
        order = self.__order_map.get(order_id, None)
        if order is not None and order.status.status != sc.Status.Cancelled:
            order.status.status = sc.Status.Cancelled
            return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")

    def buy_future(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if current < 0:
                if quantity + current > 0:
                    return OrderStatus("", "", "buy later quantity is too big")
            self.__simulation_count_map[code] = current + quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_future_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Buy,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
                octype=sc.FuturesOCType.Auto,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_future(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if quantity > current:
                return OrderStatus("", "", "quantity is too big")
            self.__simulation_count_map[code] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_future_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
                octype=sc.FuturesOCType.Auto,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_first_future(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if current > 0:
                return OrderStatus("", "", "can not sell first")
            self.__simulation_count_map[code] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_future_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
                octype=sc.FuturesOCType.Auto,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def cancel_future(self, order_id: str):
        order = self.__order_map.get(order_id, None)
        if order is not None and order.status.status != sc.Status.Cancelled:
            order.status.status = sc.Status.Cancelled
            return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")

    def buy_option(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if current < 0:
                if quantity + current > 0:
                    return OrderStatus("", "", "buy later quantity is too big")
            self.__simulation_count_map[code] = current + quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_option_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Buy,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_option(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if quantity > current:
                return OrderStatus("", "", "quantity is too big")
            self.__simulation_count_map[code] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_option_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def sell_first_option(self, code: str, price: float, quantity: int):
        with self.__simulation_lock:
            current = self.__simulation_count_map.get(code, 0)
            if current > 0:
                return OrderStatus("", "", "can not sell first")
            self.__simulation_count_map[code] = current - quantity

        sim_order = Trade(
            contract=self.sinopac.get_contract_by_option_code(code),
            order=Order(
                price=price,
                quantity=quantity,
                action=sc.Action.Sell,
                price_type=sc.FuturesPriceType.LMT,
                order_type=sc.OrderType.ROD,
            ),
            status=sj.order.OrderStatus(
                id=self.random_order_id(),
                status=sc.Status.Submitted,
                status_code="",
                order_datetime=datetime.now(),
                deals=[],
            ),
        )
        threading.Thread(
            target=self.finish_simulation_order,
            args=(sim_order, 1),
            daemon=True,
        ).start()
        return OrderStatus(sim_order.status.id, sim_order.status.status, "")

    def cancel_option(self, order_id: str):
        order = self.__order_map.get(order_id, None)
        if order is not None and order.status.status != sc.Status.Cancelled:
            order.status.status = sc.Status.Cancelled
            return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")

    def random_order_id(self) -> str:
        return "".join(random.choice(string.ascii_lowercase + string.octdigits) for _ in range(8))

    def get_local_order(self):
        return list(self.__order_map.values())

    def get_local_order_by_id(self, order_id: str):
        with self.__order_map_lock:
            order = self.__order_map.get(order_id, None)
            if order is not None:
                return OrderStatus(order.status.id, order.status.status, "")

        return OrderStatus("", "", "order not found")

    def insert_or_update_local_order(self, order: Trade):
        with self.__order_map_lock:
            self.__order_map[order.status.id] = order

    def reset_simulator(self):
        with self.__simulation_lock:
            for code, count in self.__simulation_count_map.items():
                if count != 0:
                    logger.info("clear simulation for %s", code)
            self.__simulation_count_map = {}

        with self.__order_map_lock:
            self.__order_map = {}
