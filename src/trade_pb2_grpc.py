# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import trade_pb2 as trade__pb2


class ToCSinopacBackEndStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
                '/toc_machine_trading.ToCSinopacBackEnd/HealthCheck',
                request_serializer=trade__pb2.Echo.SerializeToString,
                response_deserializer=trade__pb2.Echo.FromString,
                )
        self.GetAllStockDetail = channel.unary_unary(
                '/toc_machine_trading.ToCSinopacBackEnd/GetAllStockDetail',
                request_serializer=trade__pb2.RequestTime.SerializeToString,
                response_deserializer=trade__pb2.StockDetailResponse.FromString,
                )


class ToCSinopacBackEndServicer(object):
    """Missing associated documentation comment in .proto file."""

    def HealthCheck(self, request, context):
        """for go side to check python alive
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllStockDetail(self, request, context):
        """Get all stock detail
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ToCSinopacBackEndServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=trade__pb2.Echo.FromString,
                    response_serializer=trade__pb2.Echo.SerializeToString,
            ),
            'GetAllStockDetail': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllStockDetail,
                    request_deserializer=trade__pb2.RequestTime.FromString,
                    response_serializer=trade__pb2.StockDetailResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'toc_machine_trading.ToCSinopacBackEnd', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ToCSinopacBackEnd(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/toc_machine_trading.ToCSinopacBackEnd/HealthCheck',
            trade__pb2.Echo.SerializeToString,
            trade__pb2.Echo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllStockDetail(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/toc_machine_trading.ToCSinopacBackEnd/GetAllStockDetail',
            trade__pb2.RequestTime.SerializeToString,
            trade__pb2.StockDetailResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
