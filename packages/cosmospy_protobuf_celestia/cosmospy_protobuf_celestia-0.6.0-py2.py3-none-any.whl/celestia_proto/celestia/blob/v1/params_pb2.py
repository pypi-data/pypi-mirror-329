"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/blob/v1/params.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dcelestia/blob/v1/params.proto\x12\x10celestia.blob.v1\x1a\x14gogoproto/gogo.proto"\x84\x01\n\x06Params\x127\n\x11gas_per_blob_byte\x18\x01 \x01(\rB\x1c\xf2\xde\x1f\x18yaml:"gas_per_blob_byte"\x12;\n\x13gov_max_square_size\x18\x02 \x01(\x04B\x1e\xf2\xde\x1f\x1ayaml:"gov_max_square_size":\x04\x98\xa0\x1f\x00B2Z0github.com/celestiaorg/celestia-app/x/blob/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.blob.v1.params_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/blob/types'
    _globals['_PARAMS'].fields_by_name['gas_per_blob_byte']._loaded_options = None
    _globals['_PARAMS'].fields_by_name['gas_per_blob_byte']._serialized_options = b'\xf2\xde\x1f\x18yaml:"gas_per_blob_byte"'
    _globals['_PARAMS'].fields_by_name['gov_max_square_size']._loaded_options = None
    _globals['_PARAMS'].fields_by_name['gov_max_square_size']._serialized_options = b'\xf2\xde\x1f\x1ayaml:"gov_max_square_size"'
    _globals['_PARAMS']._loaded_options = None
    _globals['_PARAMS']._serialized_options = b'\x98\xa0\x1f\x00'
    _globals['_PARAMS']._serialized_start = 74
    _globals['_PARAMS']._serialized_end = 206