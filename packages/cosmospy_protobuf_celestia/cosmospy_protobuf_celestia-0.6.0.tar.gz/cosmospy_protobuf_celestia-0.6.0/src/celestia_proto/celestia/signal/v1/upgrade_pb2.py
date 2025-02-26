"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/signal/v1/upgrade.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n celestia/signal/v1/upgrade.proto\x12\x12celestia.signal.v1"6\n\x07Upgrade\x12\x13\n\x0bapp_version\x18\x01 \x01(\x04\x12\x16\n\x0eupgrade_height\x18\x02 \x01(\x03B4Z2github.com/celestiaorg/celestia-app/x/signal/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.signal.v1.upgrade_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/celestiaorg/celestia-app/x/signal/types'
    _globals['_UPGRADE']._serialized_start = 56
    _globals['_UPGRADE']._serialized_end = 110