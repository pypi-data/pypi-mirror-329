"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'proto/blob/v1/blob.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18proto/blob/v1/blob.proto\x12\rproto.blob.v1"q\n\tBlobProto\x12\x14\n\x0cnamespace_id\x18\x01 \x01(\x0c\x12\x0c\n\x04data\x18\x02 \x01(\x0c\x12\x15\n\rshare_version\x18\x03 \x01(\r\x12\x19\n\x11namespace_version\x18\x04 \x01(\r\x12\x0e\n\x06signer\x18\x05 \x01(\x0c"N\n\x06BlobTx\x12\n\n\x02tx\x18\x01 \x01(\x0c\x12\'\n\x05blobs\x18\x02 \x03(\x0b2\x18.proto.blob.v1.BlobProto\x12\x0f\n\x07type_id\x18\x03 \x01(\t"B\n\x0cIndexWrapper\x12\n\n\x02tx\x18\x01 \x01(\x0c\x12\x15\n\rshare_indexes\x18\x02 \x03(\r\x12\x0f\n\x07type_id\x18\x03 \x01(\tB3Z1github.com/celestiaorg/go-square/v2/proto/blob/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.blob.v1.blob_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z1github.com/celestiaorg/go-square/v2/proto/blob/v1'
    _globals['_BLOBPROTO']._serialized_start = 43
    _globals['_BLOBPROTO']._serialized_end = 156
    _globals['_BLOBTX']._serialized_start = 158
    _globals['_BLOBTX']._serialized_end = 236
    _globals['_INDEXWRAPPER']._serialized_start = 238
    _globals['_INDEXWRAPPER']._serialized_end = 304