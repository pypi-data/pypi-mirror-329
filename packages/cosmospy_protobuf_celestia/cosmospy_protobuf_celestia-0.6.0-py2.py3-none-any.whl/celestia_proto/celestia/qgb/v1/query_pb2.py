"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/qgb/v1/query.proto')
_sym_db = _symbol_database.Default()
from ....celestia.qgb.v1 import genesis_pb2 as celestia_dot_qgb_dot_v1_dot_genesis__pb2
from ....celestia.qgb.v1 import types_pb2 as celestia_dot_qgb_dot_v1_dot_types__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bcelestia/qgb/v1/query.proto\x12\x0fcelestia.qgb.v1\x1a\x1dcelestia/qgb/v1/genesis.proto\x1a\x1bcelestia/qgb/v1/types.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x19google/protobuf/any.proto"\x14\n\x12QueryParamsRequest"D\n\x13QueryParamsResponse\x12-\n\x06params\x18\x01 \x01(\x0b2\x17.celestia.qgb.v1.ParamsB\x04\xc8\xde\x1f\x00"6\n%QueryAttestationRequestByNonceRequest\x12\r\n\x05nonce\x18\x01 \x01(\x04"l\n&QueryAttestationRequestByNonceResponse\x12B\n\x0battestation\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\x17\xca\xb4-\x13AttestationRequestI"$\n"QueryLatestAttestationNonceRequest"4\n#QueryLatestAttestationNonceResponse\x12\r\n\x05nonce\x18\x01 \x01(\x04"&\n$QueryEarliestAttestationNonceRequest"6\n%QueryEarliestAttestationNonceResponse\x12\r\n\x05nonce\x18\x01 \x01(\x04";\n*QueryLatestValsetRequestBeforeNonceRequest\x12\r\n\x05nonce\x18\x01 \x01(\x04"V\n+QueryLatestValsetRequestBeforeNonceResponse\x12\'\n\x06valset\x18\x01 \x01(\x0b2\x17.celestia.qgb.v1.Valset"#\n!QueryLatestUnbondingHeightRequest"4\n"QueryLatestUnbondingHeightResponse\x12\x0e\n\x06height\x18\x01 \x01(\x04""\n QueryLatestDataCommitmentRequest"]\n!QueryLatestDataCommitmentResponse\x128\n\x0fdata_commitment\x18\x01 \x01(\x0b2\x1f.celestia.qgb.v1.DataCommitment":\n(QueryDataCommitmentRangeForHeightRequest\x12\x0e\n\x06height\x18\x01 \x01(\x04"e\n)QueryDataCommitmentRangeForHeightResponse\x128\n\x0fdata_commitment\x18\x01 \x01(\x0b2\x1f.celestia.qgb.v1.DataCommitment"3\n\x16QueryEVMAddressRequest\x12\x19\n\x11validator_address\x18\x01 \x01(\t".\n\x17QueryEVMAddressResponse\x12\x13\n\x0bevm_address\x18\x01 \x01(\t2\xf3\x0b\n\x05Query\x12k\n\x06Params\x12#.celestia.qgb.v1.QueryParamsRequest\x1a$.celestia.qgb.v1.QueryParamsResponse"\x16\x82\xd3\xe4\x93\x02\x10\x12\x0e/qgb/v1/params\x12\xbb\x01\n\x19AttestationRequestByNonce\x126.celestia.qgb.v1.QueryAttestationRequestByNonceRequest\x1a7.celestia.qgb.v1.QueryAttestationRequestByNonceResponse"-\x82\xd3\xe4\x93\x02\'\x12%/qgb/v1/attestations/requests/{nonce}\x12\xae\x01\n\x16LatestAttestationNonce\x123.celestia.qgb.v1.QueryLatestAttestationNonceRequest\x1a4.celestia.qgb.v1.QueryLatestAttestationNonceResponse")\x82\xd3\xe4\x93\x02#\x12!/qgb/v1/attestations/nonce/latest\x12\xb6\x01\n\x18EarliestAttestationNonce\x125.celestia.qgb.v1.QueryEarliestAttestationNonceRequest\x1a6.celestia.qgb.v1.QueryEarliestAttestationNonceResponse"+\x82\xd3\xe4\x93\x02%\x12#/qgb/v1/attestations/nonce/earliest\x12\xca\x01\n\x1eLatestValsetRequestBeforeNonce\x12;.celestia.qgb.v1.QueryLatestValsetRequestBeforeNonceRequest\x1a<.celestia.qgb.v1.QueryLatestValsetRequestBeforeNonceResponse"-\x82\xd3\xe4\x93\x02\'\x12%/qgb/v1/valset/request/before/{nonce}\x12\x9b\x01\n\x15LatestUnbondingHeight\x122.celestia.qgb.v1.QueryLatestUnbondingHeightRequest\x1a3.celestia.qgb.v1.QueryLatestUnbondingHeightResponse"\x19\x82\xd3\xe4\x93\x02\x13\x12\x11/qgb/v1/unbonding\x12\xc3\x01\n\x1cDataCommitmentRangeForHeight\x129.celestia.qgb.v1.QueryDataCommitmentRangeForHeightRequest\x1a:.celestia.qgb.v1.QueryDataCommitmentRangeForHeightResponse",\x82\xd3\xe4\x93\x02&\x12$/qgb/v1/data_commitment/range/height\x12\xa5\x01\n\x14LatestDataCommitment\x121.celestia.qgb.v1.QueryLatestDataCommitmentRequest\x1a2.celestia.qgb.v1.QueryLatestDataCommitmentResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/qgb/v1/data_commitment/latest\x12|\n\nEVMAddress\x12\'.celestia.qgb.v1.QueryEVMAddressRequest\x1a(.celestia.qgb.v1.QueryEVMAddressResponse"\x1b\x82\xd3\xe4\x93\x02\x15\x12\x13/qgb/v1/evm_addressB8Z6github.com/celestiaorg/celestia-app/x/blobstream/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.qgb.v1.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/celestiaorg/celestia-app/x/blobstream/types'
    _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._loaded_options = None
    _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_QUERYATTESTATIONREQUESTBYNONCERESPONSE'].fields_by_name['attestation']._loaded_options = None
    _globals['_QUERYATTESTATIONREQUESTBYNONCERESPONSE'].fields_by_name['attestation']._serialized_options = b'\xca\xb4-\x13AttestationRequestI'
    _globals['_QUERY'].methods_by_name['Params']._loaded_options = None
    _globals['_QUERY'].methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x10\x12\x0e/qgb/v1/params'
    _globals['_QUERY'].methods_by_name['AttestationRequestByNonce']._loaded_options = None
    _globals['_QUERY'].methods_by_name['AttestationRequestByNonce']._serialized_options = b"\x82\xd3\xe4\x93\x02'\x12%/qgb/v1/attestations/requests/{nonce}"
    _globals['_QUERY'].methods_by_name['LatestAttestationNonce']._loaded_options = None
    _globals['_QUERY'].methods_by_name['LatestAttestationNonce']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/qgb/v1/attestations/nonce/latest'
    _globals['_QUERY'].methods_by_name['EarliestAttestationNonce']._loaded_options = None
    _globals['_QUERY'].methods_by_name['EarliestAttestationNonce']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/qgb/v1/attestations/nonce/earliest'
    _globals['_QUERY'].methods_by_name['LatestValsetRequestBeforeNonce']._loaded_options = None
    _globals['_QUERY'].methods_by_name['LatestValsetRequestBeforeNonce']._serialized_options = b"\x82\xd3\xe4\x93\x02'\x12%/qgb/v1/valset/request/before/{nonce}"
    _globals['_QUERY'].methods_by_name['LatestUnbondingHeight']._loaded_options = None
    _globals['_QUERY'].methods_by_name['LatestUnbondingHeight']._serialized_options = b'\x82\xd3\xe4\x93\x02\x13\x12\x11/qgb/v1/unbonding'
    _globals['_QUERY'].methods_by_name['DataCommitmentRangeForHeight']._loaded_options = None
    _globals['_QUERY'].methods_by_name['DataCommitmentRangeForHeight']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/qgb/v1/data_commitment/range/height'
    _globals['_QUERY'].methods_by_name['LatestDataCommitment']._loaded_options = None
    _globals['_QUERY'].methods_by_name['LatestDataCommitment']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/qgb/v1/data_commitment/latest'
    _globals['_QUERY'].methods_by_name['EVMAddress']._loaded_options = None
    _globals['_QUERY'].methods_by_name['EVMAddress']._serialized_options = b'\x82\xd3\xe4\x93\x02\x15\x12\x13/qgb/v1/evm_address'
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 214
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 234
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 236
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 304
    _globals['_QUERYATTESTATIONREQUESTBYNONCEREQUEST']._serialized_start = 306
    _globals['_QUERYATTESTATIONREQUESTBYNONCEREQUEST']._serialized_end = 360
    _globals['_QUERYATTESTATIONREQUESTBYNONCERESPONSE']._serialized_start = 362
    _globals['_QUERYATTESTATIONREQUESTBYNONCERESPONSE']._serialized_end = 470
    _globals['_QUERYLATESTATTESTATIONNONCEREQUEST']._serialized_start = 472
    _globals['_QUERYLATESTATTESTATIONNONCEREQUEST']._serialized_end = 508
    _globals['_QUERYLATESTATTESTATIONNONCERESPONSE']._serialized_start = 510
    _globals['_QUERYLATESTATTESTATIONNONCERESPONSE']._serialized_end = 562
    _globals['_QUERYEARLIESTATTESTATIONNONCEREQUEST']._serialized_start = 564
    _globals['_QUERYEARLIESTATTESTATIONNONCEREQUEST']._serialized_end = 602
    _globals['_QUERYEARLIESTATTESTATIONNONCERESPONSE']._serialized_start = 604
    _globals['_QUERYEARLIESTATTESTATIONNONCERESPONSE']._serialized_end = 658
    _globals['_QUERYLATESTVALSETREQUESTBEFORENONCEREQUEST']._serialized_start = 660
    _globals['_QUERYLATESTVALSETREQUESTBEFORENONCEREQUEST']._serialized_end = 719
    _globals['_QUERYLATESTVALSETREQUESTBEFORENONCERESPONSE']._serialized_start = 721
    _globals['_QUERYLATESTVALSETREQUESTBEFORENONCERESPONSE']._serialized_end = 807
    _globals['_QUERYLATESTUNBONDINGHEIGHTREQUEST']._serialized_start = 809
    _globals['_QUERYLATESTUNBONDINGHEIGHTREQUEST']._serialized_end = 844
    _globals['_QUERYLATESTUNBONDINGHEIGHTRESPONSE']._serialized_start = 846
    _globals['_QUERYLATESTUNBONDINGHEIGHTRESPONSE']._serialized_end = 898
    _globals['_QUERYLATESTDATACOMMITMENTREQUEST']._serialized_start = 900
    _globals['_QUERYLATESTDATACOMMITMENTREQUEST']._serialized_end = 934
    _globals['_QUERYLATESTDATACOMMITMENTRESPONSE']._serialized_start = 936
    _globals['_QUERYLATESTDATACOMMITMENTRESPONSE']._serialized_end = 1029
    _globals['_QUERYDATACOMMITMENTRANGEFORHEIGHTREQUEST']._serialized_start = 1031
    _globals['_QUERYDATACOMMITMENTRANGEFORHEIGHTREQUEST']._serialized_end = 1089
    _globals['_QUERYDATACOMMITMENTRANGEFORHEIGHTRESPONSE']._serialized_start = 1091
    _globals['_QUERYDATACOMMITMENTRANGEFORHEIGHTRESPONSE']._serialized_end = 1192
    _globals['_QUERYEVMADDRESSREQUEST']._serialized_start = 1194
    _globals['_QUERYEVMADDRESSREQUEST']._serialized_end = 1245
    _globals['_QUERYEVMADDRESSRESPONSE']._serialized_start = 1247
    _globals['_QUERYEVMADDRESSRESPONSE']._serialized_end = 1293
    _globals['_QUERY']._serialized_start = 1296
    _globals['_QUERY']._serialized_end = 2819