"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/signal/v1/tx.proto')
_sym_db = _symbol_database.Default()
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bcelestia/signal/v1/tx.proto\x12\x12celestia.signal.v1\x1a\x1cgoogle/api/annotations.proto">\n\x10MsgSignalVersion\x12\x19\n\x11validator_address\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x04"\x1a\n\x18MsgSignalVersionResponse"\x1f\n\rMsgTryUpgrade\x12\x0e\n\x06signer\x18\x01 \x01(\t"\x17\n\x15MsgTryUpgradeResponse2\xfd\x01\n\x03Msg\x12~\n\rSignalVersion\x12$.celestia.signal.v1.MsgSignalVersion\x1a,.celestia.signal.v1.MsgSignalVersionResponse"\x19\x82\xd3\xe4\x93\x02\x13"\x11/signal/v1/signal\x12v\n\nTryUpgrade\x12!.celestia.signal.v1.MsgTryUpgrade\x1a).celestia.signal.v1.MsgTryUpgradeResponse"\x1a\x82\xd3\xe4\x93\x02\x14"\x12/signal/v1/upgradeB4Z2github.com/celestiaorg/celestia-app/x/signal/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.signal.v1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/celestiaorg/celestia-app/x/signal/types'
    _globals['_MSG'].methods_by_name['SignalVersion']._loaded_options = None
    _globals['_MSG'].methods_by_name['SignalVersion']._serialized_options = b'\x82\xd3\xe4\x93\x02\x13"\x11/signal/v1/signal'
    _globals['_MSG'].methods_by_name['TryUpgrade']._loaded_options = None
    _globals['_MSG'].methods_by_name['TryUpgrade']._serialized_options = b'\x82\xd3\xe4\x93\x02\x14"\x12/signal/v1/upgrade'
    _globals['_MSGSIGNALVERSION']._serialized_start = 81
    _globals['_MSGSIGNALVERSION']._serialized_end = 143
    _globals['_MSGSIGNALVERSIONRESPONSE']._serialized_start = 145
    _globals['_MSGSIGNALVERSIONRESPONSE']._serialized_end = 171
    _globals['_MSGTRYUPGRADE']._serialized_start = 173
    _globals['_MSGTRYUPGRADE']._serialized_end = 204
    _globals['_MSGTRYUPGRADERESPONSE']._serialized_start = 206
    _globals['_MSGTRYUPGRADERESPONSE']._serialized_end = 229
    _globals['_MSG']._serialized_start = 232
    _globals['_MSG']._serialized_end = 485