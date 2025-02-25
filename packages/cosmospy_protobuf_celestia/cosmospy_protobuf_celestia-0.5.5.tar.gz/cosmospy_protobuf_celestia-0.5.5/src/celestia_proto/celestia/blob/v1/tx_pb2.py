"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/blob/v1/tx.proto')
_sym_db = _symbol_database.Default()
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19celestia/blob/v1/tx.proto\x12\x10celestia.blob.v1\x1a\x1cgoogle/api/annotations.proto"{\n\x0eMsgPayForBlobs\x12\x0e\n\x06signer\x18\x01 \x01(\t\x12\x12\n\nnamespaces\x18\x02 \x03(\x0c\x12\x12\n\nblob_sizes\x18\x03 \x03(\r\x12\x19\n\x11share_commitments\x18\x04 \x03(\x0c\x12\x16\n\x0eshare_versions\x18\x08 \x03(\r"\x18\n\x16MsgPayForBlobsResponse2\x81\x01\n\x03Msg\x12z\n\x0bPayForBlobs\x12 .celestia.blob.v1.MsgPayForBlobs\x1a(.celestia.blob.v1.MsgPayForBlobsResponse"\x1f\x82\xd3\xe4\x93\x02\x19"\x14/blob/v1/payforblobs:\x01*B2Z0github.com/celestiaorg/celestia-app/x/blob/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.blob.v1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/celestiaorg/celestia-app/x/blob/types'
    _globals['_MSG'].methods_by_name['PayForBlobs']._loaded_options = None
    _globals['_MSG'].methods_by_name['PayForBlobs']._serialized_options = b'\x82\xd3\xe4\x93\x02\x19"\x14/blob/v1/payforblobs:\x01*'
    _globals['_MSGPAYFORBLOBS']._serialized_start = 77
    _globals['_MSGPAYFORBLOBS']._serialized_end = 200
    _globals['_MSGPAYFORBLOBSRESPONSE']._serialized_start = 202
    _globals['_MSGPAYFORBLOBSRESPONSE']._serialized_end = 226
    _globals['_MSG']._serialized_start = 229
    _globals['_MSG']._serialized_end = 358