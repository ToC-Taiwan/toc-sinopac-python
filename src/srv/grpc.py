from concurrent import futures

import grpc

import trade_pb2
import trade_pb2_grpc


class ToCSinopacBackEnd(trade_pb2_grpc.ToCSinopacBackEndServicer):
    def HealthCheck(self, request, _):
        return trade_pb2.Echo(message=request.message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trade_pb2_grpc.add_ToCSinopacBackEndServicer_to_server(ToCSinopacBackEnd(), server)
    server.add_insecure_port('[::]:56666')
    server.start()
    server.wait_for_termination()
