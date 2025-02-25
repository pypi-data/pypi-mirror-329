"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'cosmos/upgrade/v1beta1/tx.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.upgrade.v1beta1 import upgrade_pb2 as cosmos_dot_upgrade_dot_v1beta1_dot_upgrade__pb2
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fcosmos/upgrade/v1beta1/tx.proto\x12\x16cosmos.upgrade.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a$cosmos/upgrade/v1beta1/upgrade.proto\x1a\x17cosmos/msg/v1/msg.proto"\x83\x01\n\x12MsgSoftwareUpgrade\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x120\n\x04plan\x18\x02 \x01(\x0b2\x1c.cosmos.upgrade.v1beta1.PlanB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority"\x1c\n\x1aMsgSoftwareUpgradeResponse"O\n\x10MsgCancelUpgrade\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString:\x0e\x82\xe7\xb0*\tauthority"\x1a\n\x18MsgCancelUpgradeResponse2\xe5\x01\n\x03Msg\x12q\n\x0fSoftwareUpgrade\x12*.cosmos.upgrade.v1beta1.MsgSoftwareUpgrade\x1a2.cosmos.upgrade.v1beta1.MsgSoftwareUpgradeResponse\x12k\n\rCancelUpgrade\x12(.cosmos.upgrade.v1beta1.MsgCancelUpgrade\x1a0.cosmos.upgrade.v1beta1.MsgCancelUpgradeResponseB.Z,github.com/cosmos/cosmos-sdk/x/upgrade/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.upgrade.v1beta1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z,github.com/cosmos/cosmos-sdk/x/upgrade/types'
    _globals['_MSGSOFTWAREUPGRADE'].fields_by_name['authority']._loaded_options = None
    _globals['_MSGSOFTWAREUPGRADE'].fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGSOFTWAREUPGRADE'].fields_by_name['plan']._loaded_options = None
    _globals['_MSGSOFTWAREUPGRADE'].fields_by_name['plan']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_MSGSOFTWAREUPGRADE']._loaded_options = None
    _globals['_MSGSOFTWAREUPGRADE']._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _globals['_MSGCANCELUPGRADE'].fields_by_name['authority']._loaded_options = None
    _globals['_MSGCANCELUPGRADE'].fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGCANCELUPGRADE']._loaded_options = None
    _globals['_MSGCANCELUPGRADE']._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _globals['_MSGSOFTWAREUPGRADE']._serialized_start = 172
    _globals['_MSGSOFTWAREUPGRADE']._serialized_end = 303
    _globals['_MSGSOFTWAREUPGRADERESPONSE']._serialized_start = 305
    _globals['_MSGSOFTWAREUPGRADERESPONSE']._serialized_end = 333
    _globals['_MSGCANCELUPGRADE']._serialized_start = 335
    _globals['_MSGCANCELUPGRADE']._serialized_end = 414
    _globals['_MSGCANCELUPGRADERESPONSE']._serialized_start = 416
    _globals['_MSGCANCELUPGRADERESPONSE']._serialized_end = 442
    _globals['_MSG']._serialized_start = 445
    _globals['_MSG']._serialized_end = 674