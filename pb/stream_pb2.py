# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stream.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cstream.proto\x12\x11sinopac_forwarder\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0c\x63ommon.proto\"\"\n\x11YahooFinancePrice\x12\r\n\x05price\x18\x01 \x01(\x01\"0\n\x11VolumeRankRequest\x12\r\n\x05\x63ount\x18\x01 \x01(\x03\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\"D\n\x10SnapshotResponse\x12\x30\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\".sinopac_forwarder.SnapshotMessage\"\xab\x03\n\x0fSnapshotMessage\x12\n\n\x02ts\x18\x01 \x01(\x03\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x10\n\x08\x65xchange\x18\x03 \x01(\t\x12\x0c\n\x04open\x18\x04 \x01(\x01\x12\x0c\n\x04high\x18\x05 \x01(\x01\x12\x0b\n\x03low\x18\x06 \x01(\x01\x12\r\n\x05\x63lose\x18\x07 \x01(\x01\x12\x11\n\ttick_type\x18\x08 \x01(\t\x12\x14\n\x0c\x63hange_price\x18\t \x01(\x01\x12\x13\n\x0b\x63hange_rate\x18\n \x01(\x01\x12\x13\n\x0b\x63hange_type\x18\x0b \x01(\t\x12\x15\n\raverage_price\x18\x0c \x01(\x01\x12\x0e\n\x06volume\x18\r \x01(\x03\x12\x14\n\x0ctotal_volume\x18\x0e \x01(\x03\x12\x0e\n\x06\x61mount\x18\x0f \x01(\x03\x12\x14\n\x0ctotal_amount\x18\x10 \x01(\x03\x12\x18\n\x10yesterday_volume\x18\x11 \x01(\x01\x12\x11\n\tbuy_price\x18\x12 \x01(\x01\x12\x12\n\nbuy_volume\x18\x13 \x01(\x01\x12\x12\n\nsell_price\x18\x14 \x01(\x01\x12\x13\n\x0bsell_volume\x18\x15 \x01(\x03\x12\x14\n\x0cvolume_ratio\x18\x16 \x01(\x01\"R\n\x17StockVolumeRankResponse\x12\x37\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32).sinopac_forwarder.StockVolumeRankMessage\"\x8e\x04\n\x16StockVolumeRankMessage\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\n\n\x02ts\x18\x04 \x01(\x03\x12\x0c\n\x04open\x18\x05 \x01(\x01\x12\x0c\n\x04high\x18\x06 \x01(\x01\x12\x0b\n\x03low\x18\x07 \x01(\x01\x12\r\n\x05\x63lose\x18\x08 \x01(\x01\x12\x13\n\x0bprice_range\x18\t \x01(\x01\x12\x11\n\ttick_type\x18\n \x01(\x03\x12\x14\n\x0c\x63hange_price\x18\x0b \x01(\x01\x12\x13\n\x0b\x63hange_type\x18\x0c \x01(\x03\x12\x15\n\raverage_price\x18\r \x01(\x01\x12\x0e\n\x06volume\x18\x0e \x01(\x03\x12\x14\n\x0ctotal_volume\x18\x0f \x01(\x03\x12\x0e\n\x06\x61mount\x18\x10 \x01(\x03\x12\x14\n\x0ctotal_amount\x18\x11 \x01(\x03\x12\x18\n\x10yesterday_volume\x18\x12 \x01(\x03\x12\x14\n\x0cvolume_ratio\x18\x13 \x01(\x01\x12\x11\n\tbuy_price\x18\x14 \x01(\x01\x12\x12\n\nbuy_volume\x18\x15 \x01(\x03\x12\x12\n\nsell_price\x18\x16 \x01(\x01\x12\x13\n\x0bsell_volume\x18\x17 \x01(\x03\x12\x12\n\nbid_orders\x18\x18 \x01(\x03\x12\x13\n\x0b\x62id_volumes\x18\x19 \x01(\x03\x12\x12\n\nask_orders\x18\x1a \x01(\x03\x12\x13\n\x0b\x61sk_volumes\x18\x1b \x01(\x03\"%\n\x11SubscribeResponse\x12\x10\n\x08\x66\x61il_arr\x18\x01 \x03(\t2\xa3\r\n\x13StreamDataInterface\x12\x61\n\x18GetStockSnapshotByNumArr\x12\x1e.sinopac_forwarder.StockNumArr\x1a#.sinopac_forwarder.SnapshotResponse\"\x00\x12T\n\x13GetAllStockSnapshot\x12\x16.google.protobuf.Empty\x1a#.sinopac_forwarder.SnapshotResponse\"\x00\x12S\n\x13GetStockSnapshotTSE\x12\x16.google.protobuf.Empty\x1a\".sinopac_forwarder.SnapshotMessage\"\x00\x12S\n\x13GetStockSnapshotOTC\x12\x16.google.protobuf.Empty\x1a\".sinopac_forwarder.SnapshotMessage\"\x00\x12K\n\tGetNasdaq\x12\x16.google.protobuf.Empty\x1a$.sinopac_forwarder.YahooFinancePrice\"\x00\x12Q\n\x0fGetNasdaqFuture\x12\x16.google.protobuf.Empty\x1a$.sinopac_forwarder.YahooFinancePrice\"\x00\x12h\n\x12GetStockVolumeRank\x12$.sinopac_forwarder.VolumeRankRequest\x1a*.sinopac_forwarder.StockVolumeRankResponse\"\x00\x12\\\n\x12SubscribeStockTick\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12^\n\x14UnSubscribeStockTick\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12^\n\x14SubscribeStockBidAsk\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12`\n\x16UnSubscribeStockBidAsk\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12_\n\x13SubscribeFutureTick\x12 .sinopac_forwarder.FutureCodeArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12\x61\n\x15UnSubscribeFutureTick\x12 .sinopac_forwarder.FutureCodeArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12\x61\n\x15SubscribeFutureBidAsk\x12 .sinopac_forwarder.FutureCodeArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12\x63\n\x17UnSubscribeFutureBidAsk\x12 .sinopac_forwarder.FutureCodeArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12T\n\x17UnSubscribeStockAllTick\x12\x16.google.protobuf.Empty\x1a\x1f.sinopac_forwarder.ErrorMessage\"\x00\x12V\n\x19UnSubscribeStockAllBidAsk\x12\x16.google.protobuf.Empty\x1a\x1f.sinopac_forwarder.ErrorMessage\"\x00\x12\x65\n\x1aGetFutureSnapshotByCodeArr\x12 .sinopac_forwarder.FutureCodeArr\x1a#.sinopac_forwarder.SnapshotResponse\"\x00\x42\x06Z\x04./pbb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stream_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _YAHOOFINANCEPRICE._serialized_start=78
  _YAHOOFINANCEPRICE._serialized_end=112
  _VOLUMERANKREQUEST._serialized_start=114
  _VOLUMERANKREQUEST._serialized_end=162
  _SNAPSHOTRESPONSE._serialized_start=164
  _SNAPSHOTRESPONSE._serialized_end=232
  _SNAPSHOTMESSAGE._serialized_start=235
  _SNAPSHOTMESSAGE._serialized_end=662
  _STOCKVOLUMERANKRESPONSE._serialized_start=664
  _STOCKVOLUMERANKRESPONSE._serialized_end=746
  _STOCKVOLUMERANKMESSAGE._serialized_start=749
  _STOCKVOLUMERANKMESSAGE._serialized_end=1275
  _SUBSCRIBERESPONSE._serialized_start=1277
  _SUBSCRIBERESPONSE._serialized_end=1314
  _STREAMDATAINTERFACE._serialized_start=1317
  _STREAMDATAINTERFACE._serialized_end=3016
# @@protoc_insertion_point(module_scope)
