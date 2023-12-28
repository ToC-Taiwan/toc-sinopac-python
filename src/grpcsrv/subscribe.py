from pb import entity_pb2, subscribe_pb2, subscribe_pb2_grpc
from sinopac_worker import SinopacWorkerPool


class RPCSubscribe(subscribe_pb2_grpc.SubscribeDataInterfaceServicer):
    def __init__(self, workers: SinopacWorkerPool):
        self.workers = workers

    def SubscribeStockTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.subscribe_stock_tick(stock_num, request.odd)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.unsubscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeStockBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.subscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.unsubscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeFutureTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.subscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.unsubscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def SubscribeFutureBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.subscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.unsubscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeAllTick(self, request, _):
        result = self.workers.unsubscribe_all_tick()
        if len(result["stock"]) > 0 or len(result["future"]) > 0:
            return entity_pb2.ErrorMessage(err="UnSubscribeAllTick fail")
        return entity_pb2.ErrorMessage(err="")

    def UnSubscribeAllBidAsk(self, request, _):
        result = self.workers.unsubscribe_all_bidask()
        if len(result["stock"]) > 0 or len(result["future"]) > 0:
            return entity_pb2.ErrorMessage(err="UnSubscribeAllBidAsk fail")
        return entity_pb2.ErrorMessage(err="")
