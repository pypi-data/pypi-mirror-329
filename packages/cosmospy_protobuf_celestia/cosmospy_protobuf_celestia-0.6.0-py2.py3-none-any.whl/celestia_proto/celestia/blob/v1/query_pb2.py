"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/blob/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....celestia.blob.v1 import params_pb2 as celestia_dot_blob_dot_v1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccelestia/blob/v1/query.proto\x12\x10celestia.blob.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1dcelestia/blob/v1/params.proto"\x14\n\x12QueryParamsRequest"E\n\x13QueryParamsResponse\x12.\n\x06params\x18\x01 \x01(\x0b2\x18.celestia.blob.v1.ParamsB\x04\xc8\xde\x1f\x002w\n\x05Query\x12n\n\x06Params\x12$.celestia.blob.v1.QueryParamsRequest\x1a%.celestia.blob.v1.QueryParamsResponse"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/blob/v1/paramsB2Z0github.com/celestiaorg/celestia-app/x/blob/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.blob.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/blob/types'
    _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._loaded_options = None
    _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_QUERY'].methods_by_name['Params']._loaded_options = None
    _globals['_QUERY'].methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x11\x12\x0f/blob/v1/params'
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 133
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 153
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 155
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 224
    _globals['_QUERY']._serialized_start = 226
    _globals['_QUERY']._serialized_end = 345