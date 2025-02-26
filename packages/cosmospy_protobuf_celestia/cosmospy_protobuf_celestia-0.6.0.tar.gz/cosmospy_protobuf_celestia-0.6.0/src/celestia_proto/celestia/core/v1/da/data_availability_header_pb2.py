"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/core/v1/da/data_availability_header.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2celestia/core/v1/da/data_availability_header.proto\x12\x13celestia.core.v1.da"A\n\x16DataAvailabilityHeader\x12\x11\n\trow_roots\x18\x01 \x03(\x0c\x12\x14\n\x0ccolumn_roots\x18\x02 \x03(\x0cB?Z=github.com/celestiaorg/celestia-app/proto/celestia/core/v1/dab\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.core.v1.da.data_availability_header_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/celestiaorg/celestia-app/proto/celestia/core/v1/da'
    _globals['_DATAAVAILABILITYHEADER']._serialized_start = 75
    _globals['_DATAAVAILABILITYHEADER']._serialized_end = 140