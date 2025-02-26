"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/qgb/v1/types.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bcelestia/qgb/v1/types.proto\x12\x0fcelestia.qgb.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto"5\n\x0fBridgeValidator\x12\r\n\x05power\x18\x01 \x01(\x04\x12\x13\n\x0bevm_address\x18\x02 \x01(\t"\xad\x01\n\x06Valset\x12\r\n\x05nonce\x18\x01 \x01(\x04\x127\n\x07members\x18\x02 \x03(\x0b2 .celestia.qgb.v1.BridgeValidatorB\x04\xc8\xde\x1f\x00\x12\x0e\n\x06height\x18\x03 \x01(\x04\x122\n\x04time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01:\x17\xca\xb4-\x13AttestationRequestI"\x94\x01\n\x0eDataCommitment\x12\r\n\x05nonce\x18\x01 \x01(\x04\x12\x13\n\x0bbegin_block\x18\x02 \x01(\x04\x12\x11\n\tend_block\x18\x03 \x01(\x04\x122\n\x04time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01:\x17\xca\xb4-\x13AttestationRequestIB8Z6github.com/celestiaorg/celestia-app/x/blobstream/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.qgb.v1.types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/celestiaorg/celestia-app/x/blobstream/types'
    _globals['_VALSET'].fields_by_name['members']._loaded_options = None
    _globals['_VALSET'].fields_by_name['members']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_VALSET'].fields_by_name['time']._loaded_options = None
    _globals['_VALSET'].fields_by_name['time']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _globals['_VALSET']._loaded_options = None
    _globals['_VALSET']._serialized_options = b'\xca\xb4-\x13AttestationRequestI'
    _globals['_DATACOMMITMENT'].fields_by_name['time']._loaded_options = None
    _globals['_DATACOMMITMENT'].fields_by_name['time']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _globals['_DATACOMMITMENT']._loaded_options = None
    _globals['_DATACOMMITMENT']._serialized_options = b'\xca\xb4-\x13AttestationRequestI'
    _globals['_BRIDGEVALIDATOR']._serialized_start = 130
    _globals['_BRIDGEVALIDATOR']._serialized_end = 183
    _globals['_VALSET']._serialized_start = 186
    _globals['_VALSET']._serialized_end = 359
    _globals['_DATACOMMITMENT']._serialized_start = 362
    _globals['_DATACOMMITMENT']._serialized_end = 510