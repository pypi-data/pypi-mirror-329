"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/signal/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....celestia.signal.v1 import upgrade_pb2 as celestia_dot_signal_dot_v1_dot_upgrade__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ecelestia/signal/v1/query.proto\x12\x12celestia.signal.v1\x1a\x1cgoogle/api/annotations.proto\x1a celestia/signal/v1/upgrade.proto"+\n\x18QueryVersionTallyRequest\x12\x0f\n\x07version\x18\x01 \x01(\x04"f\n\x19QueryVersionTallyResponse\x12\x14\n\x0cvoting_power\x18\x01 \x01(\x04\x12\x17\n\x0fthreshold_power\x18\x02 \x01(\x04\x12\x1a\n\x12total_voting_power\x18\x03 \x01(\x04"\x18\n\x16QueryGetUpgradeRequest"G\n\x17QueryGetUpgradeResponse\x12,\n\x07upgrade\x18\x01 \x01(\x0b2\x1b.celestia.signal.v1.Upgrade2\x9d\x02\n\x05Query\x12\x8f\x01\n\x0cVersionTally\x12,.celestia.signal.v1.QueryVersionTallyRequest\x1a-.celestia.signal.v1.QueryVersionTallyResponse""\x82\xd3\xe4\x93\x02\x1c\x12\x1a/signal/v1/tally/{version}\x12\x81\x01\n\nGetUpgrade\x12*.celestia.signal.v1.QueryGetUpgradeRequest\x1a+.celestia.signal.v1.QueryGetUpgradeResponse"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/signal/v1/upgradeB4Z2github.com/celestiaorg/celestia-app/x/signal/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.signal.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/celestiaorg/celestia-app/x/signal/types'
    _globals['_QUERY'].methods_by_name['VersionTally']._loaded_options = None
    _globals['_QUERY'].methods_by_name['VersionTally']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c\x12\x1a/signal/v1/tally/{version}'
    _globals['_QUERY'].methods_by_name['GetUpgrade']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GetUpgrade']._serialized_options = b'\x82\xd3\xe4\x93\x02\x14\x12\x12/signal/v1/upgrade'
    _globals['_QUERYVERSIONTALLYREQUEST']._serialized_start = 118
    _globals['_QUERYVERSIONTALLYREQUEST']._serialized_end = 161
    _globals['_QUERYVERSIONTALLYRESPONSE']._serialized_start = 163
    _globals['_QUERYVERSIONTALLYRESPONSE']._serialized_end = 265
    _globals['_QUERYGETUPGRADEREQUEST']._serialized_start = 267
    _globals['_QUERYGETUPGRADEREQUEST']._serialized_end = 291
    _globals['_QUERYGETUPGRADERESPONSE']._serialized_start = 293
    _globals['_QUERYGETUPGRADERESPONSE']._serialized_end = 364
    _globals['_QUERY']._serialized_start = 367
    _globals['_QUERY']._serialized_end = 652