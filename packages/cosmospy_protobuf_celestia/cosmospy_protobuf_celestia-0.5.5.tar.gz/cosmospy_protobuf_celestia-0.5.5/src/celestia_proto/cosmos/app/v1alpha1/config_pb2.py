"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'cosmos/app/v1alpha1/config.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n cosmos/app/v1alpha1/config.proto\x12\x13cosmos.app.v1alpha1\x1a\x19google/protobuf/any.proto"<\n\x06Config\x122\n\x07modules\x18\x01 \x03(\x0b2!.cosmos.app.v1alpha1.ModuleConfig"B\n\x0cModuleConfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x06config\x18\x02 \x01(\x0b2\x14.google.protobuf.Anyb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.app.v1alpha1.config_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_CONFIG']._serialized_start = 84
    _globals['_CONFIG']._serialized_end = 144
    _globals['_MODULECONFIG']._serialized_start = 146
    _globals['_MODULECONFIG']._serialized_end = 212