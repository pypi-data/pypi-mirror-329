"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/mint/v1/mint.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bcelestia/mint/v1/mint.proto\x12\x10celestia.mint.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x8a\x02\n\x06Minter\x12T\n\x0einflation_rate\x18\x01 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec\x12W\n\x11annual_provisions\x18\x02 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec\x12=\n\x13previous_block_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\x12\x12\n\nbond_denom\x18\x05 \x01(\t"E\n\x0bGenesisTime\x126\n\x0cgenesis_time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01B2Z0github.com/celestiaorg/celestia-app/x/mint/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.mint.v1.mint_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/mint/types'
    _globals['_MINTER'].fields_by_name['inflation_rate']._loaded_options = None
    _globals['_MINTER'].fields_by_name['inflation_rate']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec'
    _globals['_MINTER'].fields_by_name['annual_provisions']._loaded_options = None
    _globals['_MINTER'].fields_by_name['annual_provisions']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec'
    _globals['_MINTER'].fields_by_name['previous_block_time']._loaded_options = None
    _globals['_MINTER'].fields_by_name['previous_block_time']._serialized_options = b'\x90\xdf\x1f\x01'
    _globals['_GENESISTIME'].fields_by_name['genesis_time']._loaded_options = None
    _globals['_GENESISTIME'].fields_by_name['genesis_time']._serialized_options = b'\x90\xdf\x1f\x01'
    _globals['_MINTER']._serialized_start = 132
    _globals['_MINTER']._serialized_end = 398
    _globals['_GENESISTIME']._serialized_start = 400
    _globals['_GENESISTIME']._serialized_end = 469