# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: basic.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x62\x61sic.proto\x12\x14toc_python_forwarder\x1a\x1bgoogle/protobuf/empty.proto\"-\n\x0b\x42\x65\x61tMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"N\n\x13StockDetailResponse\x12\x37\n\x05stock\x18\x01 \x03(\x0b\x32(.toc_python_forwarder.StockDetailMessage\"Q\n\x14\x46utureDetailResponse\x12\x39\n\x06\x66uture\x18\x01 \x03(\x0b\x32).toc_python_forwarder.FutureDetailMessage\"Q\n\x14OptionDetailResponse\x12\x39\n\x06option\x18\x01 \x03(\x0b\x32).toc_python_forwarder.OptionDetailMessage\"\x8f\x01\n\x12StockDetailMessage\x12\x10\n\x08\x65xchange\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x11\n\treference\x18\x05 \x01(\x01\x12\x13\n\x0bupdate_date\x18\x06 \x01(\t\x12\x11\n\tday_trade\x18\x07 \x01(\t\"\xf7\x01\n\x13\x46utureDetailMessage\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x04 \x01(\t\x12\x16\n\x0e\x64\x65livery_month\x18\x05 \x01(\t\x12\x15\n\rdelivery_date\x18\x06 \x01(\t\x12\x17\n\x0funderlying_kind\x18\x07 \x01(\t\x12\x0c\n\x04unit\x18\x08 \x01(\x03\x12\x10\n\x08limit_up\x18\t \x01(\x01\x12\x12\n\nlimit_down\x18\n \x01(\x01\x12\x11\n\treference\x18\x0b \x01(\x01\x12\x13\n\x0bupdate_date\x18\x0c \x01(\t\"\xa3\x02\n\x13OptionDetailMessage\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x04 \x01(\t\x12\x16\n\x0e\x64\x65livery_month\x18\x05 \x01(\t\x12\x15\n\rdelivery_date\x18\x06 \x01(\t\x12\x14\n\x0cstrike_price\x18\x07 \x01(\x01\x12\x14\n\x0coption_right\x18\x08 \x01(\t\x12\x17\n\x0funderlying_kind\x18\t \x01(\t\x12\x0c\n\x04unit\x18\n \x01(\x03\x12\x10\n\x08limit_up\x18\x0b \x01(\x01\x12\x12\n\nlimit_down\x18\x0c \x01(\x01\x12\x11\n\treference\x18\r \x01(\x01\x12\x13\n\x0bupdate_date\x18\x0e \x01(\t2\xba\x03\n\x12\x42\x61sicDataInterface\x12U\n\tHeartbeat\x12!.toc_python_forwarder.BeatMessage\x1a!.toc_python_forwarder.BeatMessage(\x01\x30\x01\x12;\n\tTerminate\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\x12X\n\x11GetAllStockDetail\x12\x16.google.protobuf.Empty\x1a).toc_python_forwarder.StockDetailResponse\"\x00\x12Z\n\x12GetAllFutureDetail\x12\x16.google.protobuf.Empty\x1a*.toc_python_forwarder.FutureDetailResponse\"\x00\x12Z\n\x12GetAllOptionDetail\x12\x16.google.protobuf.Empty\x1a*.toc_python_forwarder.OptionDetailResponse\"\x00\x42\x06Z\x04./pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'basic_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _globals['_BEATMESSAGE']._serialized_start=66
  _globals['_BEATMESSAGE']._serialized_end=111
  _globals['_STOCKDETAILRESPONSE']._serialized_start=113
  _globals['_STOCKDETAILRESPONSE']._serialized_end=191
  _globals['_FUTUREDETAILRESPONSE']._serialized_start=193
  _globals['_FUTUREDETAILRESPONSE']._serialized_end=274
  _globals['_OPTIONDETAILRESPONSE']._serialized_start=276
  _globals['_OPTIONDETAILRESPONSE']._serialized_end=357
  _globals['_STOCKDETAILMESSAGE']._serialized_start=360
  _globals['_STOCKDETAILMESSAGE']._serialized_end=503
  _globals['_FUTUREDETAILMESSAGE']._serialized_start=506
  _globals['_FUTUREDETAILMESSAGE']._serialized_end=753
  _globals['_OPTIONDETAILMESSAGE']._serialized_start=756
  _globals['_OPTIONDETAILMESSAGE']._serialized_end=1047
  _globals['_BASICDATAINTERFACE']._serialized_start=1050
  _globals['_BASICDATAINTERFACE']._serialized_end=1492
# @@protoc_insertion_point(module_scope)
