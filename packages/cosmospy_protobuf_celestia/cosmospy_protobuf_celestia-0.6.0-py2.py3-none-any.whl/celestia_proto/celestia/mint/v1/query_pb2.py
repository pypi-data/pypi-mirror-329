"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/mint/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....celestia.mint.v1 import mint_pb2 as celestia_dot_mint_dot_v1_dot_mint__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccelestia/mint/v1/query.proto\x12\x10celestia.mint.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bcelestia/mint/v1/mint.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x1b\n\x19QueryInflationRateRequest"d\n\x1aQueryInflationRateResponse\x12F\n\x0einflation_rate\x18\x01 \x01(\x0cB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec"\x1e\n\x1cQueryAnnualProvisionsRequest"j\n\x1dQueryAnnualProvisionsResponse\x12I\n\x11annual_provisions\x18\x01 \x01(\x0cB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec"\x19\n\x17QueryGenesisTimeRequest"R\n\x18QueryGenesisTimeResponse\x126\n\x0cgenesis_time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x012\xd9\x03\n\x05Query\x12\x97\x01\n\rInflationRate\x12+.celestia.mint.v1.QueryInflationRateRequest\x1a,.celestia.mint.v1.QueryInflationRateResponse"+\x82\xd3\xe4\x93\x02%\x12#/cosmos/mint/v1beta1/inflation_rate\x12\xa3\x01\n\x10AnnualProvisions\x12..celestia.mint.v1.QueryAnnualProvisionsRequest\x1a/.celestia.mint.v1.QueryAnnualProvisionsResponse".\x82\xd3\xe4\x93\x02(\x12&/cosmos/mint/v1beta1/annual_provisions\x12\x8f\x01\n\x0bGenesisTime\x12).celestia.mint.v1.QueryGenesisTimeRequest\x1a*.celestia.mint.v1.QueryGenesisTimeResponse")\x82\xd3\xe4\x93\x02#\x12!/cosmos/mint/v1beta1/genesis_timeB2Z0github.com/celestiaorg/celestia-app/x/mint/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.mint.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/mint/types'
    _globals['_QUERYINFLATIONRATERESPONSE'].fields_by_name['inflation_rate']._loaded_options = None
    _globals['_QUERYINFLATIONRATERESPONSE'].fields_by_name['inflation_rate']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec'
    _globals['_QUERYANNUALPROVISIONSRESPONSE'].fields_by_name['annual_provisions']._loaded_options = None
    _globals['_QUERYANNUALPROVISIONSRESPONSE'].fields_by_name['annual_provisions']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec'
    _globals['_QUERYGENESISTIMERESPONSE'].fields_by_name['genesis_time']._loaded_options = None
    _globals['_QUERYGENESISTIMERESPONSE'].fields_by_name['genesis_time']._serialized_options = b'\x90\xdf\x1f\x01'
    _globals['_QUERY'].methods_by_name['InflationRate']._loaded_options = None
    _globals['_QUERY'].methods_by_name['InflationRate']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/cosmos/mint/v1beta1/inflation_rate'
    _globals['_QUERY'].methods_by_name['AnnualProvisions']._loaded_options = None
    _globals['_QUERY'].methods_by_name['AnnualProvisions']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/cosmos/mint/v1beta1/annual_provisions'
    _globals['_QUERY'].methods_by_name['GenesisTime']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GenesisTime']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/cosmos/mint/v1beta1/genesis_time'
    _globals['_QUERYINFLATIONRATEREQUEST']._serialized_start = 164
    _globals['_QUERYINFLATIONRATEREQUEST']._serialized_end = 191
    _globals['_QUERYINFLATIONRATERESPONSE']._serialized_start = 193
    _globals['_QUERYINFLATIONRATERESPONSE']._serialized_end = 293
    _globals['_QUERYANNUALPROVISIONSREQUEST']._serialized_start = 295
    _globals['_QUERYANNUALPROVISIONSREQUEST']._serialized_end = 325
    _globals['_QUERYANNUALPROVISIONSRESPONSE']._serialized_start = 327
    _globals['_QUERYANNUALPROVISIONSRESPONSE']._serialized_end = 433
    _globals['_QUERYGENESISTIMEREQUEST']._serialized_start = 435
    _globals['_QUERYGENESISTIMEREQUEST']._serialized_end = 460
    _globals['_QUERYGENESISTIMERESPONSE']._serialized_start = 462
    _globals['_QUERYGENESISTIMERESPONSE']._serialized_end = 544
    _globals['_QUERY']._serialized_start = 547
    _globals['_QUERY']._serialized_end = 1020