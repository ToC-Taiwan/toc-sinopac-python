# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sinopac_forwarder.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17sinopac_forwarder.proto\x12\x11sinopac_forwarder\x1a\x1bgoogle/protobuf/empty.proto\"\x1a\n\x0b\x46unctionErr\x12\x0b\n\x03\x65rr\x18\x01 \x01(\t\"-\n\x07OrderID\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x10\n\x08simulate\x18\x02 \x01(\x08\"X\n\x10StockOrderDetail\x12\x11\n\tstock_num\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x10\n\x08quantity\x18\x03 \x01(\x03\x12\x10\n\x08simulate\x18\x04 \x01(\x08\">\n\x0bTradeResult\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\r\n\x05\x65rror\x18\x03 \x01(\t\"g\n\rEventResponse\x12\x11\n\tresp_code\x18\x01 \x01(\x03\x12\x12\n\nevent_code\x18\x02 \x01(\x03\x12\x0c\n\x04info\x18\x03 \x01(\t\x12\r\n\x05\x65vent\x18\x04 \x01(\t\x12\x12\n\nevent_time\x18\x05 \x01(\t\"\x14\n\x04\x44\x61te\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\"\x1e\n\rTokenResponse\x12\r\n\x05token\x18\x01 \x01(\t\"$\n\x0bStockNumArr\x12\x15\n\rstock_num_arr\x18\x01 \x03(\t\":\n\x13StockNumArrWithDate\x12\x15\n\rstock_num_arr\x18\x01 \x03(\t\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\"A\n\x16StockNumArrWithDateArr\x12\x15\n\rstock_num_arr\x18\x01 \x03(\t\x12\x10\n\x08\x64\x61te_arr\x18\x02 \x03(\t\"K\n\x13StockDetailResponse\x12\x34\n\x05stock\x18\x01 \x03(\x0b\x32%.sinopac_forwarder.StockDetailMessage\"\x8f\x01\n\x12StockDetailMessage\x12\x10\n\x08\x65xchange\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x11\n\treference\x18\x05 \x01(\x01\x12\x13\n\x0bupdate_date\x18\x06 \x01(\t\x12\x11\n\tday_trade\x18\x07 \x01(\t\"N\n\x15StockSnapshotResponse\x12\x35\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\'.sinopac_forwarder.StockSnapshotMessage\"\xb0\x03\n\x14StockSnapshotMessage\x12\n\n\x02ts\x18\x01 \x01(\x03\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x10\n\x08\x65xchange\x18\x03 \x01(\t\x12\x0c\n\x04open\x18\x04 \x01(\x01\x12\x0c\n\x04high\x18\x05 \x01(\x01\x12\x0b\n\x03low\x18\x06 \x01(\x01\x12\r\n\x05\x63lose\x18\x07 \x01(\x01\x12\x11\n\ttick_type\x18\x08 \x01(\t\x12\x14\n\x0c\x63hange_price\x18\t \x01(\x01\x12\x13\n\x0b\x63hange_rate\x18\n \x01(\x01\x12\x13\n\x0b\x63hange_type\x18\x0b \x01(\t\x12\x15\n\raverage_price\x18\x0c \x01(\x01\x12\x0e\n\x06volume\x18\r \x01(\x03\x12\x14\n\x0ctotal_volume\x18\x0e \x01(\x03\x12\x0e\n\x06\x61mount\x18\x0f \x01(\x03\x12\x14\n\x0ctotal_amount\x18\x10 \x01(\x03\x12\x18\n\x10yesterday_volume\x18\x11 \x01(\x01\x12\x11\n\tbuy_price\x18\x12 \x01(\x01\x12\x12\n\nbuy_volume\x18\x13 \x01(\x01\x12\x12\n\nsell_price\x18\x14 \x01(\x01\x12\x13\n\x0bsell_volume\x18\x15 \x01(\x03\x12\x14\n\x0cvolume_ratio\x18\x16 \x01(\x01\"T\n\x18StockHistoryTickResponse\x12\x38\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32*.sinopac_forwarder.StockHistoryTickMessage\"\xb8\x01\n\x17StockHistoryTickMessage\x12\n\n\x02ts\x18\x01 \x01(\x03\x12\r\n\x05\x63lose\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x03\x12\x11\n\tbid_price\x18\x04 \x01(\x01\x12\x12\n\nbid_volume\x18\x05 \x01(\x03\x12\x11\n\task_price\x18\x06 \x01(\x01\x12\x12\n\nask_volume\x18\x07 \x01(\x03\x12\x11\n\ttick_type\x18\x08 \x01(\x03\x12\x11\n\tstock_num\x18\t \x01(\t\"T\n\x18StockHistoryKbarResponse\x12\x38\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32*.sinopac_forwarder.StockHistoryKbarMessage\"\x80\x01\n\x17StockHistoryKbarMessage\x12\n\n\x02ts\x18\x01 \x01(\x03\x12\r\n\x05\x43lose\x18\x02 \x01(\x01\x12\x0c\n\x04Open\x18\x03 \x01(\x01\x12\x0c\n\x04High\x18\x04 \x01(\x01\x12\x0b\n\x03Low\x18\x05 \x01(\x01\x12\x0e\n\x06Volume\x18\x06 \x01(\x03\x12\x11\n\tstock_num\x18\x07 \x01(\t\"V\n\x19StockHistoryCloseResponse\x12\x39\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32+.sinopac_forwarder.StockHistoryCloseMessage\"E\n\x18StockHistoryCloseMessage\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\r\n\x05\x63lose\x18\x03 \x01(\x01\"0\n\x11VolumeRankRequest\x12\r\n\x05\x63ount\x18\x01 \x01(\x03\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\"R\n\x17StockVolumeRankResponse\x12\x37\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32).sinopac_forwarder.StockVolumeRankMessage\"\x8e\x04\n\x16StockVolumeRankMessage\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\n\n\x02ts\x18\x04 \x01(\x03\x12\x0c\n\x04open\x18\x05 \x01(\x01\x12\x0c\n\x04high\x18\x06 \x01(\x01\x12\x0b\n\x03low\x18\x07 \x01(\x01\x12\r\n\x05\x63lose\x18\x08 \x01(\x01\x12\x13\n\x0bprice_range\x18\t \x01(\x01\x12\x11\n\ttick_type\x18\n \x01(\x03\x12\x14\n\x0c\x63hange_price\x18\x0b \x01(\x01\x12\x13\n\x0b\x63hange_type\x18\x0c \x01(\x03\x12\x15\n\raverage_price\x18\r \x01(\x01\x12\x0e\n\x06volume\x18\x0e \x01(\x03\x12\x14\n\x0ctotal_volume\x18\x0f \x01(\x03\x12\x0e\n\x06\x61mount\x18\x10 \x01(\x03\x12\x14\n\x0ctotal_amount\x18\x11 \x01(\x03\x12\x18\n\x10yesterday_volume\x18\x12 \x01(\x03\x12\x14\n\x0cvolume_ratio\x18\x13 \x01(\x01\x12\x11\n\tbuy_price\x18\x14 \x01(\x01\x12\x12\n\nbuy_volume\x18\x15 \x01(\x03\x12\x12\n\nsell_price\x18\x16 \x01(\x01\x12\x13\n\x0bsell_volume\x18\x17 \x01(\x03\x12\x12\n\nbid_orders\x18\x18 \x01(\x03\x12\x13\n\x0b\x62id_volumes\x18\x19 \x01(\x03\x12\x12\n\nask_orders\x18\x1a \x01(\x03\x12\x13\n\x0b\x61sk_volumes\x18\x1b \x01(\x03\"%\n\x11SubscribeResponse\x12\x10\n\x08\x66\x61il_arr\x18\x01 \x03(\t\"\xaf\x03\n\x19StockRealTimeTickResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x11\n\tdate_time\x18\x02 \x01(\t\x12\x0c\n\x04open\x18\x03 \x01(\x01\x12\x11\n\tavg_price\x18\x04 \x01(\x01\x12\r\n\x05\x63lose\x18\x05 \x01(\x01\x12\x0c\n\x04high\x18\x06 \x01(\x01\x12\x0b\n\x03low\x18\x07 \x01(\x01\x12\x0e\n\x06\x61mount\x18\x08 \x01(\x01\x12\x14\n\x0ctotal_amount\x18\t \x01(\x01\x12\x0e\n\x06volume\x18\n \x01(\x03\x12\x14\n\x0ctotal_volume\x18\x0b \x01(\x03\x12\x11\n\ttick_type\x18\x0c \x01(\x03\x12\x10\n\x08\x63hg_type\x18\r \x01(\x03\x12\x11\n\tprice_chg\x18\x0e \x01(\x01\x12\x0f\n\x07pct_chg\x18\x0f \x01(\x01\x12\x1a\n\x12\x62id_side_total_vol\x18\x10 \x01(\x03\x12\x1a\n\x12\x61sk_side_total_vol\x18\x11 \x01(\x03\x12\x1a\n\x12\x62id_side_total_cnt\x18\x12 \x01(\x03\x12\x1a\n\x12\x61sk_side_total_cnt\x18\x13 \x01(\x03\x12\x0f\n\x07suspend\x18\x14 \x01(\x03\x12\x10\n\x08simtrade\x18\x15 \x01(\x03\"\xdb\x01\n\x1bStockRealTimeBidAskResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x11\n\tdate_time\x18\x02 \x01(\t\x12\x11\n\tbid_price\x18\x03 \x03(\x01\x12\x12\n\nbid_volume\x18\x04 \x03(\x03\x12\x14\n\x0c\x64iff_bid_vol\x18\x05 \x03(\x03\x12\x11\n\task_price\x18\x06 \x03(\x01\x12\x12\n\nask_volume\x18\x07 \x03(\x03\x12\x14\n\x0c\x64iff_ask_vol\x18\x08 \x03(\x03\x12\x0f\n\x07suspend\x18\t \x01(\x03\x12\x10\n\x08simtrade\x18\n \x01(\x03\"H\n\x13StockOrderStatusArr\x12\x31\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32#.sinopac_forwarder.StockOrderStatus\"\x87\x01\n\x10StockOrderStatus\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tion\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x01\x12\x10\n\x08quantity\x18\x05 \x01(\x03\x12\x10\n\x08order_id\x18\x06 \x01(\t\x12\x12\n\norder_time\x18\x07 \x01(\t2\xaf\r\n\x10SinopacForwarder\x12L\n\x0eGetServerToken\x12\x16.google.protobuf.Empty\x1a .sinopac_forwarder.TokenResponse\"\x00\x12U\n\x11GetAllStockDetail\x12\x16.google.protobuf.Empty\x1a&.sinopac_forwarder.StockDetailResponse\"\x00\x12Y\n\x13GetAllStockSnapshot\x12\x16.google.protobuf.Empty\x1a(.sinopac_forwarder.StockSnapshotResponse\"\x00\x12\x66\n\x18GetStockSnapshotByNumArr\x12\x1e.sinopac_forwarder.StockNumArr\x1a(.sinopac_forwarder.StockSnapshotResponse\"\x00\x12Y\n\x13GetStockSnapshotTSE\x12\x16.google.protobuf.Empty\x1a(.sinopac_forwarder.StockSnapshotResponse\"\x00\x12l\n\x13GetStockHistoryTick\x12&.sinopac_forwarder.StockNumArrWithDate\x1a+.sinopac_forwarder.StockHistoryTickResponse\"\x00\x12l\n\x13GetStockHistoryKbar\x12&.sinopac_forwarder.StockNumArrWithDate\x1a+.sinopac_forwarder.StockHistoryKbarResponse\"\x00\x12n\n\x14GetStockHistoryClose\x12&.sinopac_forwarder.StockNumArrWithDate\x1a,.sinopac_forwarder.StockHistoryCloseResponse\"\x00\x12z\n\x1dGetStockHistoryCloseByDateArr\x12).sinopac_forwarder.StockNumArrWithDateArr\x1a,.sinopac_forwarder.StockHistoryCloseResponse\"\x00\x12`\n\x16GetStockTSEHistoryTick\x12\x17.sinopac_forwarder.Date\x1a+.sinopac_forwarder.StockHistoryTickResponse\"\x00\x12`\n\x16GetStockTSEHistoryKbar\x12\x17.sinopac_forwarder.Date\x1a+.sinopac_forwarder.StockHistoryKbarResponse\"\x00\x12\x62\n\x17GetStockTSEHistoryClose\x12\x17.sinopac_forwarder.Date\x1a,.sinopac_forwarder.StockHistoryCloseResponse\"\x00\x12h\n\x12GetStockVolumeRank\x12$.sinopac_forwarder.VolumeRankRequest\x1a*.sinopac_forwarder.StockVolumeRankResponse\"\x00\x12\\\n\x12SubscribeStockTick\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12^\n\x14SubscribeStockBidAsk\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12^\n\x14UnSubscribeStockTick\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x12`\n\x16UnSubscribeStockBidAsk\x12\x1e.sinopac_forwarder.StockNumArr\x1a$.sinopac_forwarder.SubscribeResponse\"\x00\x32\xdd\x04\n\x0cTradeService\x12Q\n\x08\x42uyStock\x12#.sinopac_forwarder.StockOrderDetail\x1a\x1e.sinopac_forwarder.TradeResult\"\x00\x12R\n\tSellStock\x12#.sinopac_forwarder.StockOrderDetail\x1a\x1e.sinopac_forwarder.TradeResult\"\x00\x12W\n\x0eSellFirstStock\x12#.sinopac_forwarder.StockOrderDetail\x1a\x1e.sinopac_forwarder.TradeResult\"\x00\x12K\n\x0b\x43\x61ncelStock\x12\x1a.sinopac_forwarder.OrderID\x1a\x1e.sinopac_forwarder.TradeResult\"\x00\x12R\n\x12GetOrderStatusByID\x12\x1a.sinopac_forwarder.OrderID\x1a\x1e.sinopac_forwarder.TradeResult\"\x00\x12U\n\x11GetOrderStatusArr\x12\x16.google.protobuf.Empty\x1a&.sinopac_forwarder.StockOrderStatusArr\"\x00\x12U\n\x19GetNonBlockOrderStatusArr\x12\x16.google.protobuf.Empty\x1a\x1e.sinopac_forwarder.FunctionErr\"\x00\x42\x06Z\x04./pbb\x06proto3')



_FUNCTIONERR = DESCRIPTOR.message_types_by_name['FunctionErr']
_ORDERID = DESCRIPTOR.message_types_by_name['OrderID']
_STOCKORDERDETAIL = DESCRIPTOR.message_types_by_name['StockOrderDetail']
_TRADERESULT = DESCRIPTOR.message_types_by_name['TradeResult']
_EVENTRESPONSE = DESCRIPTOR.message_types_by_name['EventResponse']
_DATE = DESCRIPTOR.message_types_by_name['Date']
_TOKENRESPONSE = DESCRIPTOR.message_types_by_name['TokenResponse']
_STOCKNUMARR = DESCRIPTOR.message_types_by_name['StockNumArr']
_STOCKNUMARRWITHDATE = DESCRIPTOR.message_types_by_name['StockNumArrWithDate']
_STOCKNUMARRWITHDATEARR = DESCRIPTOR.message_types_by_name['StockNumArrWithDateArr']
_STOCKDETAILRESPONSE = DESCRIPTOR.message_types_by_name['StockDetailResponse']
_STOCKDETAILMESSAGE = DESCRIPTOR.message_types_by_name['StockDetailMessage']
_STOCKSNAPSHOTRESPONSE = DESCRIPTOR.message_types_by_name['StockSnapshotResponse']
_STOCKSNAPSHOTMESSAGE = DESCRIPTOR.message_types_by_name['StockSnapshotMessage']
_STOCKHISTORYTICKRESPONSE = DESCRIPTOR.message_types_by_name['StockHistoryTickResponse']
_STOCKHISTORYTICKMESSAGE = DESCRIPTOR.message_types_by_name['StockHistoryTickMessage']
_STOCKHISTORYKBARRESPONSE = DESCRIPTOR.message_types_by_name['StockHistoryKbarResponse']
_STOCKHISTORYKBARMESSAGE = DESCRIPTOR.message_types_by_name['StockHistoryKbarMessage']
_STOCKHISTORYCLOSERESPONSE = DESCRIPTOR.message_types_by_name['StockHistoryCloseResponse']
_STOCKHISTORYCLOSEMESSAGE = DESCRIPTOR.message_types_by_name['StockHistoryCloseMessage']
_VOLUMERANKREQUEST = DESCRIPTOR.message_types_by_name['VolumeRankRequest']
_STOCKVOLUMERANKRESPONSE = DESCRIPTOR.message_types_by_name['StockVolumeRankResponse']
_STOCKVOLUMERANKMESSAGE = DESCRIPTOR.message_types_by_name['StockVolumeRankMessage']
_SUBSCRIBERESPONSE = DESCRIPTOR.message_types_by_name['SubscribeResponse']
_STOCKREALTIMETICKRESPONSE = DESCRIPTOR.message_types_by_name['StockRealTimeTickResponse']
_STOCKREALTIMEBIDASKRESPONSE = DESCRIPTOR.message_types_by_name['StockRealTimeBidAskResponse']
_STOCKORDERSTATUSARR = DESCRIPTOR.message_types_by_name['StockOrderStatusArr']
_STOCKORDERSTATUS = DESCRIPTOR.message_types_by_name['StockOrderStatus']
FunctionErr = _reflection.GeneratedProtocolMessageType('FunctionErr', (_message.Message,), {
  'DESCRIPTOR' : _FUNCTIONERR,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.FunctionErr)
  })
_sym_db.RegisterMessage(FunctionErr)

OrderID = _reflection.GeneratedProtocolMessageType('OrderID', (_message.Message,), {
  'DESCRIPTOR' : _ORDERID,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.OrderID)
  })
_sym_db.RegisterMessage(OrderID)

StockOrderDetail = _reflection.GeneratedProtocolMessageType('StockOrderDetail', (_message.Message,), {
  'DESCRIPTOR' : _STOCKORDERDETAIL,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockOrderDetail)
  })
_sym_db.RegisterMessage(StockOrderDetail)

TradeResult = _reflection.GeneratedProtocolMessageType('TradeResult', (_message.Message,), {
  'DESCRIPTOR' : _TRADERESULT,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.TradeResult)
  })
_sym_db.RegisterMessage(TradeResult)

EventResponse = _reflection.GeneratedProtocolMessageType('EventResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.EventResponse)
  })
_sym_db.RegisterMessage(EventResponse)

Date = _reflection.GeneratedProtocolMessageType('Date', (_message.Message,), {
  'DESCRIPTOR' : _DATE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.Date)
  })
_sym_db.RegisterMessage(Date)

TokenResponse = _reflection.GeneratedProtocolMessageType('TokenResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOKENRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.TokenResponse)
  })
_sym_db.RegisterMessage(TokenResponse)

StockNumArr = _reflection.GeneratedProtocolMessageType('StockNumArr', (_message.Message,), {
  'DESCRIPTOR' : _STOCKNUMARR,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockNumArr)
  })
_sym_db.RegisterMessage(StockNumArr)

StockNumArrWithDate = _reflection.GeneratedProtocolMessageType('StockNumArrWithDate', (_message.Message,), {
  'DESCRIPTOR' : _STOCKNUMARRWITHDATE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockNumArrWithDate)
  })
_sym_db.RegisterMessage(StockNumArrWithDate)

StockNumArrWithDateArr = _reflection.GeneratedProtocolMessageType('StockNumArrWithDateArr', (_message.Message,), {
  'DESCRIPTOR' : _STOCKNUMARRWITHDATEARR,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockNumArrWithDateArr)
  })
_sym_db.RegisterMessage(StockNumArrWithDateArr)

StockDetailResponse = _reflection.GeneratedProtocolMessageType('StockDetailResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKDETAILRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockDetailResponse)
  })
_sym_db.RegisterMessage(StockDetailResponse)

StockDetailMessage = _reflection.GeneratedProtocolMessageType('StockDetailMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKDETAILMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockDetailMessage)
  })
_sym_db.RegisterMessage(StockDetailMessage)

StockSnapshotResponse = _reflection.GeneratedProtocolMessageType('StockSnapshotResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKSNAPSHOTRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockSnapshotResponse)
  })
_sym_db.RegisterMessage(StockSnapshotResponse)

StockSnapshotMessage = _reflection.GeneratedProtocolMessageType('StockSnapshotMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKSNAPSHOTMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockSnapshotMessage)
  })
_sym_db.RegisterMessage(StockSnapshotMessage)

StockHistoryTickResponse = _reflection.GeneratedProtocolMessageType('StockHistoryTickResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYTICKRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryTickResponse)
  })
_sym_db.RegisterMessage(StockHistoryTickResponse)

StockHistoryTickMessage = _reflection.GeneratedProtocolMessageType('StockHistoryTickMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYTICKMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryTickMessage)
  })
_sym_db.RegisterMessage(StockHistoryTickMessage)

StockHistoryKbarResponse = _reflection.GeneratedProtocolMessageType('StockHistoryKbarResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYKBARRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryKbarResponse)
  })
_sym_db.RegisterMessage(StockHistoryKbarResponse)

StockHistoryKbarMessage = _reflection.GeneratedProtocolMessageType('StockHistoryKbarMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYKBARMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryKbarMessage)
  })
_sym_db.RegisterMessage(StockHistoryKbarMessage)

StockHistoryCloseResponse = _reflection.GeneratedProtocolMessageType('StockHistoryCloseResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYCLOSERESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryCloseResponse)
  })
_sym_db.RegisterMessage(StockHistoryCloseResponse)

StockHistoryCloseMessage = _reflection.GeneratedProtocolMessageType('StockHistoryCloseMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKHISTORYCLOSEMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockHistoryCloseMessage)
  })
_sym_db.RegisterMessage(StockHistoryCloseMessage)

VolumeRankRequest = _reflection.GeneratedProtocolMessageType('VolumeRankRequest', (_message.Message,), {
  'DESCRIPTOR' : _VOLUMERANKREQUEST,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.VolumeRankRequest)
  })
_sym_db.RegisterMessage(VolumeRankRequest)

StockVolumeRankResponse = _reflection.GeneratedProtocolMessageType('StockVolumeRankResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKVOLUMERANKRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockVolumeRankResponse)
  })
_sym_db.RegisterMessage(StockVolumeRankResponse)

StockVolumeRankMessage = _reflection.GeneratedProtocolMessageType('StockVolumeRankMessage', (_message.Message,), {
  'DESCRIPTOR' : _STOCKVOLUMERANKMESSAGE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockVolumeRankMessage)
  })
_sym_db.RegisterMessage(StockVolumeRankMessage)

SubscribeResponse = _reflection.GeneratedProtocolMessageType('SubscribeResponse', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBERESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.SubscribeResponse)
  })
_sym_db.RegisterMessage(SubscribeResponse)

StockRealTimeTickResponse = _reflection.GeneratedProtocolMessageType('StockRealTimeTickResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKREALTIMETICKRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockRealTimeTickResponse)
  })
_sym_db.RegisterMessage(StockRealTimeTickResponse)

StockRealTimeBidAskResponse = _reflection.GeneratedProtocolMessageType('StockRealTimeBidAskResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOCKREALTIMEBIDASKRESPONSE,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockRealTimeBidAskResponse)
  })
_sym_db.RegisterMessage(StockRealTimeBidAskResponse)

StockOrderStatusArr = _reflection.GeneratedProtocolMessageType('StockOrderStatusArr', (_message.Message,), {
  'DESCRIPTOR' : _STOCKORDERSTATUSARR,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockOrderStatusArr)
  })
_sym_db.RegisterMessage(StockOrderStatusArr)

StockOrderStatus = _reflection.GeneratedProtocolMessageType('StockOrderStatus', (_message.Message,), {
  'DESCRIPTOR' : _STOCKORDERSTATUS,
  '__module__' : 'sinopac_forwarder_pb2'
  # @@protoc_insertion_point(class_scope:sinopac_forwarder.StockOrderStatus)
  })
_sym_db.RegisterMessage(StockOrderStatus)

_SINOPACFORWARDER = DESCRIPTOR.services_by_name['SinopacForwarder']
_TRADESERVICE = DESCRIPTOR.services_by_name['TradeService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _FUNCTIONERR._serialized_start=75
  _FUNCTIONERR._serialized_end=101
  _ORDERID._serialized_start=103
  _ORDERID._serialized_end=148
  _STOCKORDERDETAIL._serialized_start=150
  _STOCKORDERDETAIL._serialized_end=238
  _TRADERESULT._serialized_start=240
  _TRADERESULT._serialized_end=302
  _EVENTRESPONSE._serialized_start=304
  _EVENTRESPONSE._serialized_end=407
  _DATE._serialized_start=409
  _DATE._serialized_end=429
  _TOKENRESPONSE._serialized_start=431
  _TOKENRESPONSE._serialized_end=461
  _STOCKNUMARR._serialized_start=463
  _STOCKNUMARR._serialized_end=499
  _STOCKNUMARRWITHDATE._serialized_start=501
  _STOCKNUMARRWITHDATE._serialized_end=559
  _STOCKNUMARRWITHDATEARR._serialized_start=561
  _STOCKNUMARRWITHDATEARR._serialized_end=626
  _STOCKDETAILRESPONSE._serialized_start=628
  _STOCKDETAILRESPONSE._serialized_end=703
  _STOCKDETAILMESSAGE._serialized_start=706
  _STOCKDETAILMESSAGE._serialized_end=849
  _STOCKSNAPSHOTRESPONSE._serialized_start=851
  _STOCKSNAPSHOTRESPONSE._serialized_end=929
  _STOCKSNAPSHOTMESSAGE._serialized_start=932
  _STOCKSNAPSHOTMESSAGE._serialized_end=1364
  _STOCKHISTORYTICKRESPONSE._serialized_start=1366
  _STOCKHISTORYTICKRESPONSE._serialized_end=1450
  _STOCKHISTORYTICKMESSAGE._serialized_start=1453
  _STOCKHISTORYTICKMESSAGE._serialized_end=1637
  _STOCKHISTORYKBARRESPONSE._serialized_start=1639
  _STOCKHISTORYKBARRESPONSE._serialized_end=1723
  _STOCKHISTORYKBARMESSAGE._serialized_start=1726
  _STOCKHISTORYKBARMESSAGE._serialized_end=1854
  _STOCKHISTORYCLOSERESPONSE._serialized_start=1856
  _STOCKHISTORYCLOSERESPONSE._serialized_end=1942
  _STOCKHISTORYCLOSEMESSAGE._serialized_start=1944
  _STOCKHISTORYCLOSEMESSAGE._serialized_end=2013
  _VOLUMERANKREQUEST._serialized_start=2015
  _VOLUMERANKREQUEST._serialized_end=2063
  _STOCKVOLUMERANKRESPONSE._serialized_start=2065
  _STOCKVOLUMERANKRESPONSE._serialized_end=2147
  _STOCKVOLUMERANKMESSAGE._serialized_start=2150
  _STOCKVOLUMERANKMESSAGE._serialized_end=2676
  _SUBSCRIBERESPONSE._serialized_start=2678
  _SUBSCRIBERESPONSE._serialized_end=2715
  _STOCKREALTIMETICKRESPONSE._serialized_start=2718
  _STOCKREALTIMETICKRESPONSE._serialized_end=3149
  _STOCKREALTIMEBIDASKRESPONSE._serialized_start=3152
  _STOCKREALTIMEBIDASKRESPONSE._serialized_end=3371
  _STOCKORDERSTATUSARR._serialized_start=3373
  _STOCKORDERSTATUSARR._serialized_end=3445
  _STOCKORDERSTATUS._serialized_start=3448
  _STOCKORDERSTATUS._serialized_end=3583
  _SINOPACFORWARDER._serialized_start=3586
  _SINOPACFORWARDER._serialized_end=5297
  _TRADESERVICE._serialized_start=5300
  _TRADESERVICE._serialized_end=5905
# @@protoc_insertion_point(module_scope)
