"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/minfee/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ecelestia/minfee/v1/query.proto\x12\x12celestia.minfee.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19cosmos_proto/cosmos.proto"\x19\n\x17QueryNetworkMinGasPrice"~\n\x1fQueryNetworkMinGasPriceResponse\x12[\n\x15network_min_gas_price\x18\x01 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec2\xab\x01\n\x05Query\x12\xa1\x01\n\x12NetworkMinGasPrice\x12+.celestia.minfee.v1.QueryNetworkMinGasPrice\x1a3.celestia.minfee.v1.QueryNetworkMinGasPriceResponse")\x82\xd3\xe4\x93\x02#\x12!/celestia/minfee/v1/min_gas_priceB.Z,github.com/celestiaorg/celestia-app/x/minfeeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.minfee.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z,github.com/celestiaorg/celestia-app/x/minfee'
    _globals['_QUERYNETWORKMINGASPRICERESPONSE'].fields_by_name['network_min_gas_price']._loaded_options = None
    _globals['_QUERYNETWORKMINGASPRICERESPONSE'].fields_by_name['network_min_gas_price']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xd2\xb4-\ncosmos.Dec'
    _globals['_QUERY'].methods_by_name['NetworkMinGasPrice']._loaded_options = None
    _globals['_QUERY'].methods_by_name['NetworkMinGasPrice']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/celestia/minfee/v1/min_gas_price'
    _globals['_QUERYNETWORKMINGASPRICE']._serialized_start = 133
    _globals['_QUERYNETWORKMINGASPRICE']._serialized_end = 158
    _globals['_QUERYNETWORKMINGASPRICERESPONSE']._serialized_start = 160
    _globals['_QUERYNETWORKMINGASPRICERESPONSE']._serialized_end = 286
    _globals['_QUERY']._serialized_start = 289
    _globals['_QUERY']._serialized_end = 460