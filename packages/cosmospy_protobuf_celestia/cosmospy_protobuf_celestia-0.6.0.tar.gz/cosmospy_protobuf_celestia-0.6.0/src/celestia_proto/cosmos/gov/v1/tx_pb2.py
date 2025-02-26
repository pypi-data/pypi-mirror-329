"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'cosmos/gov/v1/tx.proto')
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.gov.v1 import gov_pb2 as cosmos_dot_gov_dot_v1_dot_gov__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16cosmos/gov/v1/tx.proto\x12\rcosmos.gov.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x17cosmos/gov/v1/gov.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x19google/protobuf/any.proto\x1a\x17cosmos/msg/v1/msg.proto"\xc2\x01\n\x11MsgSubmitProposal\x12&\n\x08messages\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x128\n\x0finitial_deposit\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12*\n\x08proposer\x18\x03 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\x10\n\x08metadata\x18\x04 \x01(\t:\r\x82\xe7\xb0*\x08proposer"0\n\x19MsgSubmitProposalResponse\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04"m\n\x14MsgExecLegacyContent\x122\n\x07content\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\x0b\xca\xb4-\x07Content\x12\x11\n\tauthority\x18\x02 \x01(\t:\x0e\x82\xe7\xb0*\tauthority"\x1e\n\x1cMsgExecLegacyContentResponse"\xa1\x01\n\x07MsgVote\x12$\n\x0bproposal_id\x18\x01 \x01(\x04B\x0f\xea\xde\x1f\x0bproposal_id\x12\'\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12)\n\x06option\x18\x03 \x01(\x0e2\x19.cosmos.gov.v1.VoteOption\x12\x10\n\x08metadata\x18\x04 \x01(\t:\n\x82\xe7\xb0*\x05voter"\x11\n\x0fMsgVoteResponse"\xb2\x01\n\x0fMsgVoteWeighted\x12$\n\x0bproposal_id\x18\x01 \x01(\x04B\x0f\xea\xde\x1f\x0bproposal_id\x12\'\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x122\n\x07options\x18\x03 \x03(\x0b2!.cosmos.gov.v1.WeightedVoteOption\x12\x10\n\x08metadata\x18\x04 \x01(\t:\n\x82\xe7\xb0*\x05voter"\x19\n\x17MsgVoteWeightedResponse"\xa0\x01\n\nMsgDeposit\x12$\n\x0bproposal_id\x18\x01 \x01(\x04B\x0f\xea\xde\x1f\x0bproposal_id\x12+\n\tdepositor\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12/\n\x06amount\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tdepositor"\x14\n\x12MsgDepositResponse2\xab\x03\n\x03Msg\x12\\\n\x0eSubmitProposal\x12 .cosmos.gov.v1.MsgSubmitProposal\x1a(.cosmos.gov.v1.MsgSubmitProposalResponse\x12e\n\x11ExecLegacyContent\x12#.cosmos.gov.v1.MsgExecLegacyContent\x1a+.cosmos.gov.v1.MsgExecLegacyContentResponse\x12>\n\x04Vote\x12\x16.cosmos.gov.v1.MsgVote\x1a\x1e.cosmos.gov.v1.MsgVoteResponse\x12V\n\x0cVoteWeighted\x12\x1e.cosmos.gov.v1.MsgVoteWeighted\x1a&.cosmos.gov.v1.MsgVoteWeightedResponse\x12G\n\x07Deposit\x12\x19.cosmos.gov.v1.MsgDeposit\x1a!.cosmos.gov.v1.MsgDepositResponseB-Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.gov.v1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1'
    _globals['_MSGSUBMITPROPOSAL'].fields_by_name['initial_deposit']._loaded_options = None
    _globals['_MSGSUBMITPROPOSAL'].fields_by_name['initial_deposit']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_MSGSUBMITPROPOSAL'].fields_by_name['proposer']._loaded_options = None
    _globals['_MSGSUBMITPROPOSAL'].fields_by_name['proposer']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGSUBMITPROPOSAL']._loaded_options = None
    _globals['_MSGSUBMITPROPOSAL']._serialized_options = b'\x82\xe7\xb0*\x08proposer'
    _globals['_MSGEXECLEGACYCONTENT'].fields_by_name['content']._loaded_options = None
    _globals['_MSGEXECLEGACYCONTENT'].fields_by_name['content']._serialized_options = b'\xca\xb4-\x07Content'
    _globals['_MSGEXECLEGACYCONTENT']._loaded_options = None
    _globals['_MSGEXECLEGACYCONTENT']._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _globals['_MSGVOTE'].fields_by_name['proposal_id']._loaded_options = None
    _globals['_MSGVOTE'].fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id'
    _globals['_MSGVOTE'].fields_by_name['voter']._loaded_options = None
    _globals['_MSGVOTE'].fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGVOTE']._loaded_options = None
    _globals['_MSGVOTE']._serialized_options = b'\x82\xe7\xb0*\x05voter'
    _globals['_MSGVOTEWEIGHTED'].fields_by_name['proposal_id']._loaded_options = None
    _globals['_MSGVOTEWEIGHTED'].fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id'
    _globals['_MSGVOTEWEIGHTED'].fields_by_name['voter']._loaded_options = None
    _globals['_MSGVOTEWEIGHTED'].fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGVOTEWEIGHTED']._loaded_options = None
    _globals['_MSGVOTEWEIGHTED']._serialized_options = b'\x82\xe7\xb0*\x05voter'
    _globals['_MSGDEPOSIT'].fields_by_name['proposal_id']._loaded_options = None
    _globals['_MSGDEPOSIT'].fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id'
    _globals['_MSGDEPOSIT'].fields_by_name['depositor']._loaded_options = None
    _globals['_MSGDEPOSIT'].fields_by_name['depositor']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_MSGDEPOSIT'].fields_by_name['amount']._loaded_options = None
    _globals['_MSGDEPOSIT'].fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_MSGDEPOSIT']._loaded_options = None
    _globals['_MSGDEPOSIT']._serialized_options = b'\x82\xe7\xb0*\tdepositor'
    _globals['_MSGSUBMITPROPOSAL']._serialized_start = 200
    _globals['_MSGSUBMITPROPOSAL']._serialized_end = 394
    _globals['_MSGSUBMITPROPOSALRESPONSE']._serialized_start = 396
    _globals['_MSGSUBMITPROPOSALRESPONSE']._serialized_end = 444
    _globals['_MSGEXECLEGACYCONTENT']._serialized_start = 446
    _globals['_MSGEXECLEGACYCONTENT']._serialized_end = 555
    _globals['_MSGEXECLEGACYCONTENTRESPONSE']._serialized_start = 557
    _globals['_MSGEXECLEGACYCONTENTRESPONSE']._serialized_end = 587
    _globals['_MSGVOTE']._serialized_start = 590
    _globals['_MSGVOTE']._serialized_end = 751
    _globals['_MSGVOTERESPONSE']._serialized_start = 753
    _globals['_MSGVOTERESPONSE']._serialized_end = 770
    _globals['_MSGVOTEWEIGHTED']._serialized_start = 773
    _globals['_MSGVOTEWEIGHTED']._serialized_end = 951
    _globals['_MSGVOTEWEIGHTEDRESPONSE']._serialized_start = 953
    _globals['_MSGVOTEWEIGHTEDRESPONSE']._serialized_end = 978
    _globals['_MSGDEPOSIT']._serialized_start = 981
    _globals['_MSGDEPOSIT']._serialized_end = 1141
    _globals['_MSGDEPOSITRESPONSE']._serialized_start = 1143
    _globals['_MSGDEPOSITRESPONSE']._serialized_end = 1163
    _globals['_MSG']._serialized_start = 1166
    _globals['_MSG']._serialized_end = 1593