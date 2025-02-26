"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/core/v1/tx/tx.proto')
_sym_db = _symbol_database.Default()
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccelestia/core/v1/tx/tx.proto\x12\x13celestia.core.v1.tx\x1a\x1cgoogle/api/annotations.proto" \n\x0fTxStatusRequest\x12\r\n\x05tx_id\x18\x01 \x01(\t"h\n\x10TxStatusResponse\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12\r\n\x05index\x18\x02 \x01(\r\x12\x16\n\x0eexecution_code\x18\x03 \x01(\r\x12\r\n\x05error\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t2\x83\x01\n\x02Tx\x12}\n\x08TxStatus\x12$.celestia.core.v1.tx.TxStatusRequest\x1a%.celestia.core.v1.tx.TxStatusResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/celestia/core/v1/tx/{tx_id}B1Z/github.com/celestiaorg/celestia-app/app/grpc/txb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.core.v1.tx.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z/github.com/celestiaorg/celestia-app/app/grpc/tx'
    _globals['_TX'].methods_by_name['TxStatus']._loaded_options = None
    _globals['_TX'].methods_by_name['TxStatus']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/celestia/core/v1/tx/{tx_id}'
    _globals['_TXSTATUSREQUEST']._serialized_start = 83
    _globals['_TXSTATUSREQUEST']._serialized_end = 115
    _globals['_TXSTATUSRESPONSE']._serialized_start = 117
    _globals['_TXSTATUSRESPONSE']._serialized_end = 221
    _globals['_TX']._serialized_start = 224
    _globals['_TX']._serialized_end = 355