# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: subscribe.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import entity_pb2 as entity__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsubscribe.proto\x12\x14toc_python_forwarder\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0c\x65ntity.proto\"%\n\x11SubscribeResponse\x12\x10\n\x08\x66\x61il_arr\x18\x01 \x03(\t2\x88\x08\n\x16SubscribeDataInterface\x12\x62\n\x12SubscribeStockTick\x12!.toc_python_forwarder.StockNumArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12\x64\n\x14UnSubscribeStockTick\x12!.toc_python_forwarder.StockNumArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12\x64\n\x14SubscribeStockBidAsk\x12!.toc_python_forwarder.StockNumArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12\x66\n\x16UnSubscribeStockBidAsk\x12!.toc_python_forwarder.StockNumArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12\x65\n\x13SubscribeFutureTick\x12#.toc_python_forwarder.FutureCodeArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12g\n\x15UnSubscribeFutureTick\x12#.toc_python_forwarder.FutureCodeArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12g\n\x15SubscribeFutureBidAsk\x12#.toc_python_forwarder.FutureCodeArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12i\n\x17UnSubscribeFutureBidAsk\x12#.toc_python_forwarder.FutureCodeArr\x1a\'.toc_python_forwarder.SubscribeResponse\"\x00\x12W\n\x17UnSubscribeStockAllTick\x12\x16.google.protobuf.Empty\x1a\".toc_python_forwarder.ErrorMessage\"\x00\x12Y\n\x19UnSubscribeStockAllBidAsk\x12\x16.google.protobuf.Empty\x1a\".toc_python_forwarder.ErrorMessage\"\x00\x42\x06Z\x04./pbb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'subscribe_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _SUBSCRIBERESPONSE._serialized_start=84
  _SUBSCRIBERESPONSE._serialized_end=121
  _SUBSCRIBEDATAINTERFACE._serialized_start=124
  _SUBSCRIBEDATAINTERFACE._serialized_end=1156
# @@protoc_insertion_point(module_scope)
