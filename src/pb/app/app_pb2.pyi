"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import forwarder.basic_pb2
import forwarder.history_pb2
import forwarder.mq_pb2
import forwarder.realtime_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _PickListType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _PickListTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PickListType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TYPE_ADD: _PickListType.ValueType  # 0
    TYPE_REMOVE: _PickListType.ValueType  # 1

class PickListType(_PickListType, metaclass=_PickListTypeEnumTypeWrapper): ...

TYPE_ADD: PickListType.ValueType  # 0
TYPE_REMOVE: PickListType.ValueType  # 1
global___PickListType = PickListType

@typing_extensions.final
class PickRealMap(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class PickMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: global___PickListType.ValueType
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___PickListType.ValueType = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    PICK_MAP_FIELD_NUMBER: builtins.int
    @property
    def pick_map(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, global___PickListType.ValueType]: ...
    def __init__(
        self,
        *,
        pick_map: collections.abc.Mapping[builtins.str, global___PickListType.ValueType] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["pick_map", b"pick_map"]) -> None: ...

global___PickRealMap = PickRealMap

@typing_extensions.final
class PickFuture(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    code: builtins.str
    def __init__(
        self,
        *,
        code: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code"]) -> None: ...

global___PickFuture = PickFuture

@typing_extensions.final
class WSMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FUTURE_DETAIL_FIELD_NUMBER: builtins.int
    FUTURE_TICK_FIELD_NUMBER: builtins.int
    HISTORY_KBAR_FIELD_NUMBER: builtins.int
    SNAPSHOT_FIELD_NUMBER: builtins.int
    TRADE_INDEX_FIELD_NUMBER: builtins.int
    @property
    def future_detail(self) -> forwarder.basic_pb2.FutureDetailMessage: ...
    @property
    def future_tick(self) -> forwarder.mq_pb2.FutureRealTimeTickMessage: ...
    @property
    def history_kbar(self) -> forwarder.history_pb2.HistoryKbarResponse: ...
    @property
    def snapshot(self) -> forwarder.realtime_pb2.SnapshotMessage: ...
    @property
    def trade_index(self) -> global___TradeIndex: ...
    def __init__(
        self,
        *,
        future_detail: forwarder.basic_pb2.FutureDetailMessage | None = ...,
        future_tick: forwarder.mq_pb2.FutureRealTimeTickMessage | None = ...,
        history_kbar: forwarder.history_pb2.HistoryKbarResponse | None = ...,
        snapshot: forwarder.realtime_pb2.SnapshotMessage | None = ...,
        trade_index: global___TradeIndex | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["data", b"data", "future_detail", b"future_detail", "future_tick", b"future_tick", "history_kbar", b"history_kbar", "snapshot", b"snapshot", "trade_index", b"trade_index"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data", "future_detail", b"future_detail", "future_tick", b"future_tick", "history_kbar", b"history_kbar", "snapshot", b"snapshot", "trade_index", b"trade_index"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data", b"data"]) -> typing_extensions.Literal["future_detail", "future_tick", "history_kbar", "snapshot", "trade_index"] | None: ...

global___WSMessage = WSMessage

@typing_extensions.final
class TradeIndex(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TSE_FIELD_NUMBER: builtins.int
    OTC_FIELD_NUMBER: builtins.int
    NASDAQ_FIELD_NUMBER: builtins.int
    NF_FIELD_NUMBER: builtins.int
    @property
    def tse(self) -> global___IndexStatus: ...
    @property
    def otc(self) -> global___IndexStatus: ...
    @property
    def nasdaq(self) -> global___IndexStatus: ...
    @property
    def nf(self) -> global___IndexStatus: ...
    def __init__(
        self,
        *,
        tse: global___IndexStatus | None = ...,
        otc: global___IndexStatus | None = ...,
        nasdaq: global___IndexStatus | None = ...,
        nf: global___IndexStatus | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["nasdaq", b"nasdaq", "nf", b"nf", "otc", b"otc", "tse", b"tse"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["nasdaq", b"nasdaq", "nf", b"nf", "otc", b"otc", "tse", b"tse"]) -> None: ...

global___TradeIndex = TradeIndex

@typing_extensions.final
class IndexStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BREAK_COUNT_FIELD_NUMBER: builtins.int
    PRICE_CHG_FIELD_NUMBER: builtins.int
    break_count: builtins.int
    price_chg: builtins.float
    def __init__(
        self,
        *,
        break_count: builtins.int = ...,
        price_chg: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["break_count", b"break_count", "price_chg", b"price_chg"]) -> None: ...

global___IndexStatus = IndexStatus
