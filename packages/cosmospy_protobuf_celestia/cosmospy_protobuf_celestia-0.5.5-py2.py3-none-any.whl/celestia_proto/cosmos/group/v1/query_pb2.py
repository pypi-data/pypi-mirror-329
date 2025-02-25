"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'cosmos/group/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.group.v1 import types_pb2 as cosmos_dot_group_dot_v1_dot_types__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bcosmos/group/v1/query.proto\x12\x0fcosmos.group.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bcosmos/group/v1/types.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x19cosmos_proto/cosmos.proto")\n\x15QueryGroupInfoRequest\x12\x10\n\x08group_id\x18\x01 \x01(\x04"B\n\x16QueryGroupInfoResponse\x12(\n\x04info\x18\x01 \x01(\x0b2\x1a.cosmos.group.v1.GroupInfo"H\n\x1bQueryGroupPolicyInfoRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString"N\n\x1cQueryGroupPolicyInfoResponse\x12.\n\x04info\x18\x01 \x01(\x0b2 .cosmos.group.v1.GroupPolicyInfo"h\n\x18QueryGroupMembersRequest\x12\x10\n\x08group_id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x87\x01\n\x19QueryGroupMembersResponse\x12-\n\x07members\x18\x01 \x03(\x0b2\x1c.cosmos.group.v1.GroupMember\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x80\x01\n\x19QueryGroupsByAdminRequest\x12\'\n\x05admin\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x85\x01\n\x1aQueryGroupsByAdminResponse\x12*\n\x06groups\x18\x01 \x03(\x0b2\x1a.cosmos.group.v1.GroupInfo\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"p\n QueryGroupPoliciesByGroupRequest\x12\x10\n\x08group_id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x9a\x01\n!QueryGroupPoliciesByGroupResponse\x128\n\x0egroup_policies\x18\x01 \x03(\x0b2 .cosmos.group.v1.GroupPolicyInfo\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x87\x01\n QueryGroupPoliciesByAdminRequest\x12\'\n\x05admin\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x9a\x01\n!QueryGroupPoliciesByAdminResponse\x128\n\x0egroup_policies\x18\x01 \x03(\x0b2 .cosmos.group.v1.GroupPolicyInfo\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"+\n\x14QueryProposalRequest\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04"D\n\x15QueryProposalResponse\x12+\n\x08proposal\x18\x01 \x01(\x0b2\x19.cosmos.group.v1.Proposal"\x8b\x01\n"QueryProposalsByGroupPolicyRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x90\x01\n#QueryProposalsByGroupPolicyResponse\x12,\n\tproposals\x18\x01 \x03(\x0b2\x19.cosmos.group.v1.Proposal\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"_\n\x1fQueryVoteByProposalVoterRequest\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04\x12\'\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString"G\n QueryVoteByProposalVoterResponse\x12#\n\x04vote\x18\x01 \x01(\x0b2\x15.cosmos.group.v1.Vote"n\n\x1bQueryVotesByProposalRequest\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x81\x01\n\x1cQueryVotesByProposalResponse\x12$\n\x05votes\x18\x01 \x03(\x0b2\x15.cosmos.group.v1.Vote\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x7f\n\x18QueryVotesByVoterRequest\x12\'\n\x05voter\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"~\n\x19QueryVotesByVoterResponse\x12$\n\x05votes\x18\x01 \x03(\x0b2\x15.cosmos.group.v1.Vote\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x83\x01\n\x1aQueryGroupsByMemberRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x86\x01\n\x1bQueryGroupsByMemberResponse\x12*\n\x06groups\x18\x01 \x03(\x0b2\x1a.cosmos.group.v1.GroupInfo\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse".\n\x17QueryTallyResultRequest\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04"M\n\x18QueryTallyResultResponse\x121\n\x05tally\x18\x01 \x01(\x0b2\x1c.cosmos.group.v1.TallyResultB\x04\xc8\xde\x1f\x00"P\n\x12QueryGroupsRequest\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"~\n\x13QueryGroupsResponse\x12*\n\x06groups\x18\x01 \x03(\x0b2\x1a.cosmos.group.v1.GroupInfo\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse2\xfb\x11\n\x05Query\x12\x8c\x01\n\tGroupInfo\x12&.cosmos.group.v1.QueryGroupInfoRequest\x1a\'.cosmos.group.v1.QueryGroupInfoResponse".\x82\xd3\xe4\x93\x02(\x12&/cosmos/group/v1/group_info/{group_id}\x12\xa4\x01\n\x0fGroupPolicyInfo\x12,.cosmos.group.v1.QueryGroupPolicyInfoRequest\x1a-.cosmos.group.v1.QueryGroupPolicyInfoResponse"4\x82\xd3\xe4\x93\x02.\x12,/cosmos/group/v1/group_policy_info/{address}\x12\x98\x01\n\x0cGroupMembers\x12).cosmos.group.v1.QueryGroupMembersRequest\x1a*.cosmos.group.v1.QueryGroupMembersResponse"1\x82\xd3\xe4\x93\x02+\x12)/cosmos/group/v1/group_members/{group_id}\x12\x9a\x01\n\rGroupsByAdmin\x12*.cosmos.group.v1.QueryGroupsByAdminRequest\x1a+.cosmos.group.v1.QueryGroupsByAdminResponse"0\x82\xd3\xe4\x93\x02*\x12(/cosmos/group/v1/groups_by_admin/{admin}\x12\xba\x01\n\x14GroupPoliciesByGroup\x121.cosmos.group.v1.QueryGroupPoliciesByGroupRequest\x1a2.cosmos.group.v1.QueryGroupPoliciesByGroupResponse";\x82\xd3\xe4\x93\x025\x123/cosmos/group/v1/group_policies_by_group/{group_id}\x12\xb7\x01\n\x14GroupPoliciesByAdmin\x121.cosmos.group.v1.QueryGroupPoliciesByAdminRequest\x1a2.cosmos.group.v1.QueryGroupPoliciesByAdminResponse"8\x82\xd3\xe4\x93\x022\x120/cosmos/group/v1/group_policies_by_admin/{admin}\x12\x8a\x01\n\x08Proposal\x12%.cosmos.group.v1.QueryProposalRequest\x1a&.cosmos.group.v1.QueryProposalResponse"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/group/v1/proposal/{proposal_id}\x12\xc1\x01\n\x16ProposalsByGroupPolicy\x123.cosmos.group.v1.QueryProposalsByGroupPolicyRequest\x1a4.cosmos.group.v1.QueryProposalsByGroupPolicyResponse"<\x82\xd3\xe4\x93\x026\x124/cosmos/group/v1/proposals_by_group_policy/{address}\x12\xc1\x01\n\x13VoteByProposalVoter\x120.cosmos.group.v1.QueryVoteByProposalVoterRequest\x1a1.cosmos.group.v1.QueryVoteByProposalVoterResponse"E\x82\xd3\xe4\x93\x02?\x12=/cosmos/group/v1/vote_by_proposal_voter/{proposal_id}/{voter}\x12\xa8\x01\n\x0fVotesByProposal\x12,.cosmos.group.v1.QueryVotesByProposalRequest\x1a-.cosmos.group.v1.QueryVotesByProposalResponse"8\x82\xd3\xe4\x93\x022\x120/cosmos/group/v1/votes_by_proposal/{proposal_id}\x12\x96\x01\n\x0cVotesByVoter\x12).cosmos.group.v1.QueryVotesByVoterRequest\x1a*.cosmos.group.v1.QueryVotesByVoterResponse"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/group/v1/votes_by_voter/{voter}\x12\xa0\x01\n\x0eGroupsByMember\x12+.cosmos.group.v1.QueryGroupsByMemberRequest\x1a,.cosmos.group.v1.QueryGroupsByMemberResponse"3\x82\xd3\xe4\x93\x02-\x12+/cosmos/group/v1/groups_by_member/{address}\x12\x9a\x01\n\x0bTallyResult\x12(.cosmos.group.v1.QueryTallyResultRequest\x1a).cosmos.group.v1.QueryTallyResultResponse"6\x82\xd3\xe4\x93\x020\x12./cosmos/group/v1/proposals/{proposal_id}/tally\x12t\n\x06Groups\x12#.cosmos.group.v1.QueryGroupsRequest\x1a$.cosmos.group.v1.QueryGroupsResponse"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/cosmos/group/v1/groupsB&Z$github.com/cosmos/cosmos-sdk/x/groupb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.group.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z$github.com/cosmos/cosmos-sdk/x/group'
    _globals['_QUERYGROUPPOLICYINFOREQUEST'].fields_by_name['address']._loaded_options = None
    _globals['_QUERYGROUPPOLICYINFOREQUEST'].fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYGROUPSBYADMINREQUEST'].fields_by_name['admin']._loaded_options = None
    _globals['_QUERYGROUPSBYADMINREQUEST'].fields_by_name['admin']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYGROUPPOLICIESBYADMINREQUEST'].fields_by_name['admin']._loaded_options = None
    _globals['_QUERYGROUPPOLICIESBYADMINREQUEST'].fields_by_name['admin']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYPROPOSALSBYGROUPPOLICYREQUEST'].fields_by_name['address']._loaded_options = None
    _globals['_QUERYPROPOSALSBYGROUPPOLICYREQUEST'].fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYVOTEBYPROPOSALVOTERREQUEST'].fields_by_name['voter']._loaded_options = None
    _globals['_QUERYVOTEBYPROPOSALVOTERREQUEST'].fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYVOTESBYVOTERREQUEST'].fields_by_name['voter']._loaded_options = None
    _globals['_QUERYVOTESBYVOTERREQUEST'].fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYGROUPSBYMEMBERREQUEST'].fields_by_name['address']._loaded_options = None
    _globals['_QUERYGROUPSBYMEMBERREQUEST'].fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_QUERYTALLYRESULTRESPONSE'].fields_by_name['tally']._loaded_options = None
    _globals['_QUERYTALLYRESULTRESPONSE'].fields_by_name['tally']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_QUERY'].methods_by_name['GroupInfo']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupInfo']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/cosmos/group/v1/group_info/{group_id}'
    _globals['_QUERY'].methods_by_name['GroupPolicyInfo']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupPolicyInfo']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/cosmos/group/v1/group_policy_info/{address}'
    _globals['_QUERY'].methods_by_name['GroupMembers']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupMembers']._serialized_options = b'\x82\xd3\xe4\x93\x02+\x12)/cosmos/group/v1/group_members/{group_id}'
    _globals['_QUERY'].methods_by_name['GroupsByAdmin']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupsByAdmin']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/cosmos/group/v1/groups_by_admin/{admin}'
    _globals['_QUERY'].methods_by_name['GroupPoliciesByGroup']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupPoliciesByGroup']._serialized_options = b'\x82\xd3\xe4\x93\x025\x123/cosmos/group/v1/group_policies_by_group/{group_id}'
    _globals['_QUERY'].methods_by_name['GroupPoliciesByAdmin']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupPoliciesByAdmin']._serialized_options = b'\x82\xd3\xe4\x93\x022\x120/cosmos/group/v1/group_policies_by_admin/{admin}'
    _globals['_QUERY'].methods_by_name['Proposal']._loaded_options = None
    _globals['_QUERY'].methods_by_name['Proposal']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/cosmos/group/v1/proposal/{proposal_id}"
    _globals['_QUERY'].methods_by_name['ProposalsByGroupPolicy']._loaded_options = None
    _globals['_QUERY'].methods_by_name['ProposalsByGroupPolicy']._serialized_options = b'\x82\xd3\xe4\x93\x026\x124/cosmos/group/v1/proposals_by_group_policy/{address}'
    _globals['_QUERY'].methods_by_name['VoteByProposalVoter']._loaded_options = None
    _globals['_QUERY'].methods_by_name['VoteByProposalVoter']._serialized_options = b'\x82\xd3\xe4\x93\x02?\x12=/cosmos/group/v1/vote_by_proposal_voter/{proposal_id}/{voter}'
    _globals['_QUERY'].methods_by_name['VotesByProposal']._loaded_options = None
    _globals['_QUERY'].methods_by_name['VotesByProposal']._serialized_options = b'\x82\xd3\xe4\x93\x022\x120/cosmos/group/v1/votes_by_proposal/{proposal_id}'
    _globals['_QUERY'].methods_by_name['VotesByVoter']._loaded_options = None
    _globals['_QUERY'].methods_by_name['VotesByVoter']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/cosmos/group/v1/votes_by_voter/{voter}"
    _globals['_QUERY'].methods_by_name['GroupsByMember']._loaded_options = None
    _globals['_QUERY'].methods_by_name['GroupsByMember']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/cosmos/group/v1/groups_by_member/{address}'
    _globals['_QUERY'].methods_by_name['TallyResult']._loaded_options = None
    _globals['_QUERY'].methods_by_name['TallyResult']._serialized_options = b'\x82\xd3\xe4\x93\x020\x12./cosmos/group/v1/proposals/{proposal_id}/tally'
    _globals['_QUERY'].methods_by_name['Groups']._loaded_options = None
    _globals['_QUERY'].methods_by_name['Groups']._serialized_options = b'\x82\xd3\xe4\x93\x02\x19\x12\x17/cosmos/group/v1/groups'
    _globals['_QUERYGROUPINFOREQUEST']._serialized_start = 200
    _globals['_QUERYGROUPINFOREQUEST']._serialized_end = 241
    _globals['_QUERYGROUPINFORESPONSE']._serialized_start = 243
    _globals['_QUERYGROUPINFORESPONSE']._serialized_end = 309
    _globals['_QUERYGROUPPOLICYINFOREQUEST']._serialized_start = 311
    _globals['_QUERYGROUPPOLICYINFOREQUEST']._serialized_end = 383
    _globals['_QUERYGROUPPOLICYINFORESPONSE']._serialized_start = 385
    _globals['_QUERYGROUPPOLICYINFORESPONSE']._serialized_end = 463
    _globals['_QUERYGROUPMEMBERSREQUEST']._serialized_start = 465
    _globals['_QUERYGROUPMEMBERSREQUEST']._serialized_end = 569
    _globals['_QUERYGROUPMEMBERSRESPONSE']._serialized_start = 572
    _globals['_QUERYGROUPMEMBERSRESPONSE']._serialized_end = 707
    _globals['_QUERYGROUPSBYADMINREQUEST']._serialized_start = 710
    _globals['_QUERYGROUPSBYADMINREQUEST']._serialized_end = 838
    _globals['_QUERYGROUPSBYADMINRESPONSE']._serialized_start = 841
    _globals['_QUERYGROUPSBYADMINRESPONSE']._serialized_end = 974
    _globals['_QUERYGROUPPOLICIESBYGROUPREQUEST']._serialized_start = 976
    _globals['_QUERYGROUPPOLICIESBYGROUPREQUEST']._serialized_end = 1088
    _globals['_QUERYGROUPPOLICIESBYGROUPRESPONSE']._serialized_start = 1091
    _globals['_QUERYGROUPPOLICIESBYGROUPRESPONSE']._serialized_end = 1245
    _globals['_QUERYGROUPPOLICIESBYADMINREQUEST']._serialized_start = 1248
    _globals['_QUERYGROUPPOLICIESBYADMINREQUEST']._serialized_end = 1383
    _globals['_QUERYGROUPPOLICIESBYADMINRESPONSE']._serialized_start = 1386
    _globals['_QUERYGROUPPOLICIESBYADMINRESPONSE']._serialized_end = 1540
    _globals['_QUERYPROPOSALREQUEST']._serialized_start = 1542
    _globals['_QUERYPROPOSALREQUEST']._serialized_end = 1585
    _globals['_QUERYPROPOSALRESPONSE']._serialized_start = 1587
    _globals['_QUERYPROPOSALRESPONSE']._serialized_end = 1655
    _globals['_QUERYPROPOSALSBYGROUPPOLICYREQUEST']._serialized_start = 1658
    _globals['_QUERYPROPOSALSBYGROUPPOLICYREQUEST']._serialized_end = 1797
    _globals['_QUERYPROPOSALSBYGROUPPOLICYRESPONSE']._serialized_start = 1800
    _globals['_QUERYPROPOSALSBYGROUPPOLICYRESPONSE']._serialized_end = 1944
    _globals['_QUERYVOTEBYPROPOSALVOTERREQUEST']._serialized_start = 1946
    _globals['_QUERYVOTEBYPROPOSALVOTERREQUEST']._serialized_end = 2041
    _globals['_QUERYVOTEBYPROPOSALVOTERRESPONSE']._serialized_start = 2043
    _globals['_QUERYVOTEBYPROPOSALVOTERRESPONSE']._serialized_end = 2114
    _globals['_QUERYVOTESBYPROPOSALREQUEST']._serialized_start = 2116
    _globals['_QUERYVOTESBYPROPOSALREQUEST']._serialized_end = 2226
    _globals['_QUERYVOTESBYPROPOSALRESPONSE']._serialized_start = 2229
    _globals['_QUERYVOTESBYPROPOSALRESPONSE']._serialized_end = 2358
    _globals['_QUERYVOTESBYVOTERREQUEST']._serialized_start = 2360
    _globals['_QUERYVOTESBYVOTERREQUEST']._serialized_end = 2487
    _globals['_QUERYVOTESBYVOTERRESPONSE']._serialized_start = 2489
    _globals['_QUERYVOTESBYVOTERRESPONSE']._serialized_end = 2615
    _globals['_QUERYGROUPSBYMEMBERREQUEST']._serialized_start = 2618
    _globals['_QUERYGROUPSBYMEMBERREQUEST']._serialized_end = 2749
    _globals['_QUERYGROUPSBYMEMBERRESPONSE']._serialized_start = 2752
    _globals['_QUERYGROUPSBYMEMBERRESPONSE']._serialized_end = 2886
    _globals['_QUERYTALLYRESULTREQUEST']._serialized_start = 2888
    _globals['_QUERYTALLYRESULTREQUEST']._serialized_end = 2934
    _globals['_QUERYTALLYRESULTRESPONSE']._serialized_start = 2936
    _globals['_QUERYTALLYRESULTRESPONSE']._serialized_end = 3013
    _globals['_QUERYGROUPSREQUEST']._serialized_start = 3015
    _globals['_QUERYGROUPSREQUEST']._serialized_end = 3095
    _globals['_QUERYGROUPSRESPONSE']._serialized_start = 3097
    _globals['_QUERYGROUPSRESPONSE']._serialized_end = 3223
    _globals['_QUERY']._serialized_start = 3226
    _globals['_QUERY']._serialized_end = 5525