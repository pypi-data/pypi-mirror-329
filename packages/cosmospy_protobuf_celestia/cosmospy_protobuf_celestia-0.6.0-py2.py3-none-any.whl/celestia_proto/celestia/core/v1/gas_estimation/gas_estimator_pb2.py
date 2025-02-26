"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/core/v1/gas_estimation/gas_estimator.proto')
_sym_db = _symbol_database.Default()
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3celestia/core/v1/gas_estimation/gas_estimator.proto\x12\x1fcelestia.core.v1.gas_estimation\x1a\x1cgoogle/api/annotations.proto\x1a\x19cosmos_proto/cosmos.proto"[\n\x17EstimateGasPriceRequest\x12@\n\x0btx_priority\x18\x01 \x01(\x0e2+.celestia.core.v1.gas_estimation.TxPriority"7\n\x18EstimateGasPriceResponse\x12\x1b\n\x13estimated_gas_price\x18\x01 \x01(\x01"u\n\x1fEstimateGasPriceAndUsageRequest\x12@\n\x0btx_priority\x18\x01 \x01(\x0e2+.celestia.core.v1.gas_estimation.TxPriority\x12\x10\n\x08tx_bytes\x18\x02 \x01(\x0c"[\n EstimateGasPriceAndUsageResponse\x12\x1b\n\x13estimated_gas_price\x18\x01 \x01(\x01\x12\x1a\n\x12estimated_gas_used\x18\x02 \x01(\x04*l\n\nTxPriority\x12\x1b\n\x17TX_PRIORITY_UNSPECIFIED\x10\x00\x12\x13\n\x0fTX_PRIORITY_LOW\x10\x01\x12\x16\n\x12TX_PRIORITY_MEDIUM\x10\x02\x12\x14\n\x10TX_PRIORITY_HIGH\x10\x032\xbe\x02\n\x0cGasEstimator\x12\x89\x01\n\x10EstimateGasPrice\x128.celestia.core.v1.gas_estimation.EstimateGasPriceRequest\x1a9.celestia.core.v1.gas_estimation.EstimateGasPriceResponse"\x00\x12\xa1\x01\n\x18EstimateGasPriceAndUsage\x12@.celestia.core.v1.gas_estimation.EstimateGasPriceAndUsageRequest\x1aA.celestia.core.v1.gas_estimation.EstimateGasPriceAndUsageResponse"\x00B<Z:github.com/celestiaorg/celestia-app/app/grpc/gasestimationb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.core.v1.gas_estimation.gas_estimator_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z:github.com/celestiaorg/celestia-app/app/grpc/gasestimation'
    _globals['_TXPRIORITY']._serialized_start = 507
    _globals['_TXPRIORITY']._serialized_end = 615
    _globals['_ESTIMATEGASPRICEREQUEST']._serialized_start = 145
    _globals['_ESTIMATEGASPRICEREQUEST']._serialized_end = 236
    _globals['_ESTIMATEGASPRICERESPONSE']._serialized_start = 238
    _globals['_ESTIMATEGASPRICERESPONSE']._serialized_end = 293
    _globals['_ESTIMATEGASPRICEANDUSAGEREQUEST']._serialized_start = 295
    _globals['_ESTIMATEGASPRICEANDUSAGEREQUEST']._serialized_end = 412
    _globals['_ESTIMATEGASPRICEANDUSAGERESPONSE']._serialized_start = 414
    _globals['_ESTIMATEGASPRICEANDUSAGERESPONSE']._serialized_end = 505
    _globals['_GASESTIMATOR']._serialized_start = 618
    _globals['_GASESTIMATOR']._serialized_end = 936