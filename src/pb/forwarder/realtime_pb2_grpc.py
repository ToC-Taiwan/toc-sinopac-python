# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from forwarder import entity_pb2 as forwarder_dot_entity__pb2
from forwarder import realtime_pb2 as forwarder_dot_realtime__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class RealTimeDataInterfaceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllStockSnapshot = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetAllStockSnapshot',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
                )
        self.GetStockSnapshotByNumArr = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetStockSnapshotByNumArr',
                request_serializer=forwarder_dot_entity__pb2.StockNumArr.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
                )
        self.GetStockSnapshotTSE = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetStockSnapshotTSE',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
                )
        self.GetStockSnapshotOTC = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetStockSnapshotOTC',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
                )
        self.GetNasdaq = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetNasdaq',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.YahooFinancePrice.FromString,
                )
        self.GetNasdaqFuture = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetNasdaqFuture',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.YahooFinancePrice.FromString,
                )
        self.GetStockVolumeRank = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetStockVolumeRank',
                request_serializer=forwarder_dot_realtime__pb2.VolumeRankRequest.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.StockVolumeRankResponse.FromString,
                )
        self.GetFutureSnapshotByCodeArr = channel.unary_unary(
                '/forwarder.RealTimeDataInterface/GetFutureSnapshotByCodeArr',
                request_serializer=forwarder_dot_entity__pb2.FutureCodeArr.SerializeToString,
                response_deserializer=forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
                )


class RealTimeDataInterfaceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllStockSnapshot(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStockSnapshotByNumArr(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStockSnapshotTSE(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStockSnapshotOTC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNasdaq(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNasdaqFuture(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStockVolumeRank(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFutureSnapshotByCodeArr(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RealTimeDataInterfaceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllStockSnapshot': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllStockSnapshot,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.SnapshotResponse.SerializeToString,
            ),
            'GetStockSnapshotByNumArr': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStockSnapshotByNumArr,
                    request_deserializer=forwarder_dot_entity__pb2.StockNumArr.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.SnapshotResponse.SerializeToString,
            ),
            'GetStockSnapshotTSE': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStockSnapshotTSE,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.SnapshotResponse.SerializeToString,
            ),
            'GetStockSnapshotOTC': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStockSnapshotOTC,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.SnapshotResponse.SerializeToString,
            ),
            'GetNasdaq': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNasdaq,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.YahooFinancePrice.SerializeToString,
            ),
            'GetNasdaqFuture': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNasdaqFuture,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.YahooFinancePrice.SerializeToString,
            ),
            'GetStockVolumeRank': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStockVolumeRank,
                    request_deserializer=forwarder_dot_realtime__pb2.VolumeRankRequest.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.StockVolumeRankResponse.SerializeToString,
            ),
            'GetFutureSnapshotByCodeArr': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFutureSnapshotByCodeArr,
                    request_deserializer=forwarder_dot_entity__pb2.FutureCodeArr.FromString,
                    response_serializer=forwarder_dot_realtime__pb2.SnapshotResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'forwarder.RealTimeDataInterface', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RealTimeDataInterface(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllStockSnapshot(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetAllStockSnapshot',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStockSnapshotByNumArr(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetStockSnapshotByNumArr',
            forwarder_dot_entity__pb2.StockNumArr.SerializeToString,
            forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStockSnapshotTSE(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetStockSnapshotTSE',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStockSnapshotOTC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetStockSnapshotOTC',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNasdaq(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetNasdaq',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            forwarder_dot_realtime__pb2.YahooFinancePrice.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNasdaqFuture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetNasdaqFuture',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            forwarder_dot_realtime__pb2.YahooFinancePrice.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStockVolumeRank(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetStockVolumeRank',
            forwarder_dot_realtime__pb2.VolumeRankRequest.SerializeToString,
            forwarder_dot_realtime__pb2.StockVolumeRankResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFutureSnapshotByCodeArr(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/forwarder.RealTimeDataInterface/GetFutureSnapshotByCodeArr',
            forwarder_dot_entity__pb2.FutureCodeArr.SerializeToString,
            forwarder_dot_realtime__pb2.SnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
