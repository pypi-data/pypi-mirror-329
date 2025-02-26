"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/qgb/v1/tx.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18celestia/qgb/v1/tx.proto\x12\x0fcelestia.qgb.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1cgoogle/api/annotations.proto"a\n\x15MsgRegisterEVMAddress\x123\n\x11validator_address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\x13\n\x0bevm_address\x18\x02 \x01(\t"\x1f\n\x1dMsgRegisterEVMAddressResponse2\x9a\x01\n\x03Msg\x12\x92\x01\n\x12RegisterEVMAddress\x12&.celestia.qgb.v1.MsgRegisterEVMAddress\x1a..celestia.qgb.v1.MsgRegisterEVMAddressResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/qgb/v1/register_evm_addressB8Z6github.com/celestiaorg/celestia-app/x/blobstream/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.qgb.v1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/celestiaorg/celestia-app/x/blobstream/types'
    _globals['_MSGREGISTEREVMADDRESS'].fields_by_name['validator_address']._loaded_options = None
    _globals['_MSGREGISTEREVMADDRESS'].fields_by_name['validator_address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSG'].methods_by_name['RegisterEVMAddress']._loaded_options = None
    _globals['_MSG'].methods_by_name['RegisterEVMAddress']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/qgb/v1/register_evm_address'
    _globals['_MSGREGISTEREVMADDRESS']._serialized_start = 124
    _globals['_MSGREGISTEREVMADDRESS']._serialized_end = 221
    _globals['_MSGREGISTEREVMADDRESSRESPONSE']._serialized_start = 223
    _globals['_MSGREGISTEREVMADDRESSRESPONSE']._serialized_end = 254
    _globals['_MSG']._serialized_start = 257
    _globals['_MSG']._serialized_end = 411