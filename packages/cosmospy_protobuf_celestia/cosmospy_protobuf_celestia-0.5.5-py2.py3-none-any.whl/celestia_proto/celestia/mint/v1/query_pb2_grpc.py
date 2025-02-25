"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from ....celestia.mint.v1 import query_pb2 as celestia_dot_mint_dot_v1_dot_query__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in celestia/mint/v1/query_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InflationRate = channel.unary_unary('/celestia.mint.v1.Query/InflationRate', request_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateRequest.SerializeToString, response_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateResponse.FromString, _registered_method=True)
        self.AnnualProvisions = channel.unary_unary('/celestia.mint.v1.Query/AnnualProvisions', request_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsRequest.SerializeToString, response_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsResponse.FromString, _registered_method=True)
        self.GenesisTime = channel.unary_unary('/celestia.mint.v1.Query/GenesisTime', request_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeRequest.SerializeToString, response_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeResponse.FromString, _registered_method=True)

class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def InflationRate(self, request, context):
        """InflationRate returns the current inflation rate.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnnualProvisions(self, request, context):
        """AnnualProvisions returns the current annual provisions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenesisTime(self, request, context):
        """GenesisTime returns the genesis time.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'InflationRate': grpc.unary_unary_rpc_method_handler(servicer.InflationRate, request_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateRequest.FromString, response_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateResponse.SerializeToString), 'AnnualProvisions': grpc.unary_unary_rpc_method_handler(servicer.AnnualProvisions, request_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsRequest.FromString, response_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsResponse.SerializeToString), 'GenesisTime': grpc.unary_unary_rpc_method_handler(servicer.GenesisTime, request_deserializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeRequest.FromString, response_serializer=celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('celestia.mint.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('celestia.mint.v1.Query', rpc_method_handlers)

class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def InflationRate(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.mint.v1.Query/InflationRate', celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateRequest.SerializeToString, celestia_dot_mint_dot_v1_dot_query__pb2.QueryInflationRateResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def AnnualProvisions(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.mint.v1.Query/AnnualProvisions', celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsRequest.SerializeToString, celestia_dot_mint_dot_v1_dot_query__pb2.QueryAnnualProvisionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GenesisTime(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.mint.v1.Query/GenesisTime', celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeRequest.SerializeToString, celestia_dot_mint_dot_v1_dot_query__pb2.QueryGenesisTimeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)