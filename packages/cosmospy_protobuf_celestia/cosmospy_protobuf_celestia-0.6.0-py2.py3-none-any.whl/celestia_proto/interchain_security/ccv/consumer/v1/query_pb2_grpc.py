"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....interchain_security.ccv.consumer.v1 import query_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in interchain_security/ccv/consumer/v1/query_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class QueryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryNextFeeDistribution = channel.unary_unary('/interchain_security.ccv.consumer.v1.Query/QueryNextFeeDistribution', request_serializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateResponse.FromString, _registered_method=True)
        self.QueryParams = channel.unary_unary('/interchain_security.ccv.consumer.v1.Query/QueryParams', request_serializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsResponse.FromString, _registered_method=True)

class QueryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def QueryNextFeeDistribution(self, request, context):
        """ConsumerGenesis queries the genesis state needed to start a consumer chain
        whose proposal has been accepted
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryParams(self, request, context):
        """QueryParams queries the ccv/consumer module parameters.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'QueryNextFeeDistribution': grpc.unary_unary_rpc_method_handler(servicer.QueryNextFeeDistribution, request_deserializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('interchain_security.ccv.consumer.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('interchain_security.ccv.consumer.v1.Query', rpc_method_handlers)

class Query(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def QueryNextFeeDistribution(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.consumer.v1.Query/QueryNextFeeDistribution', interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateRequest.SerializeToString, interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryNextFeeDistributionEstimateResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.consumer.v1.Query/QueryParams', interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString, interchain__security_dot_ccv_dot_consumer_dot_v1_dot_query__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)