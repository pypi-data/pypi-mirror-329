"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/blob/v1/event.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccelestia/blob/v1/event.proto\x12\x10celestia.blob.v1"J\n\x10EventPayForBlobs\x12\x0e\n\x06signer\x18\x01 \x01(\t\x12\x12\n\nblob_sizes\x18\x02 \x03(\r\x12\x12\n\nnamespaces\x18\x03 \x03(\x0cB2Z0github.com/celestiaorg/celestia-app/x/blob/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.blob.v1.event_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/blob/types'
    _globals['_EVENTPAYFORBLOBS']._serialized_start = 50
    _globals['_EVENTPAYFORBLOBS']._serialized_end = 124