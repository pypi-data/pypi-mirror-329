"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/mint/v1/genesis.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ecelestia/mint/v1/genesis.proto\x12\x10celestia.mint.v1"(\n\x0cGenesisState\x12\x12\n\nbond_denom\x18\x02 \x01(\tJ\x04\x08\x01\x10\x02B2Z0github.com/celestiaorg/celestia-app/x/mint/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.mint.v1.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/mint/types'
    _globals['_GENESISSTATE']._serialized_start = 52
    _globals['_GENESISSTATE']._serialized_end = 92