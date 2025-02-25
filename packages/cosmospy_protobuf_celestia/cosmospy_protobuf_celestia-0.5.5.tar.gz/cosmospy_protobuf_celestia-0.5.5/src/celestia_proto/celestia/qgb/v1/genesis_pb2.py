"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/qgb/v1/genesis.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....celestia.qgb.v1 import types_pb2 as celestia_dot_qgb_dot_v1_dot_types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dcelestia/qgb/v1/genesis.proto\x12\x0fcelestia.qgb.v1\x1a\x14gogoproto/gogo.proto\x1a\x1bcelestia/qgb/v1/types.proto".\n\x06Params\x12\x1e\n\x16data_commitment_window\x18\x01 \x01(\x04:\x04\x80\xdc \x00"7\n\x0cGenesisState\x12\'\n\x06params\x18\x01 \x01(\x0b2\x17.celestia.qgb.v1.ParamsB8Z6github.com/celestiaorg/celestia-app/x/blobstream/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.qgb.v1.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/celestiaorg/celestia-app/x/blobstream/types'
    _globals['_PARAMS']._loaded_options = None
    _globals['_PARAMS']._serialized_options = b'\x80\xdc \x00'
    _globals['_PARAMS']._serialized_start = 101
    _globals['_PARAMS']._serialized_end = 147
    _globals['_GENESISSTATE']._serialized_start = 149
    _globals['_GENESISSTATE']._serialized_end = 204