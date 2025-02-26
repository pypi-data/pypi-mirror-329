"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/minfee/v1/genesis.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n celestia/minfee/v1/genesis.proto\x12\x12celestia.minfee.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto"k\n\x0cGenesisState\x12[\n\x15network_min_gas_price\x18\x01 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.DecB.Z,github.com/celestiaorg/celestia-app/x/minfeeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.minfee.v1.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z,github.com/celestiaorg/celestia-app/x/minfee'
    _globals['_GENESISSTATE'].fields_by_name['network_min_gas_price']._loaded_options = None
    _globals['_GENESISSTATE'].fields_by_name['network_min_gas_price']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec'
    _globals['_GENESISSTATE']._serialized_start = 105
    _globals['_GENESISSTATE']._serialized_end = 212