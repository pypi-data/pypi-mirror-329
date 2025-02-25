"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from ....celestia.minfee.v1 import query_pb2 as celestia_dot_minfee_dot_v1_dot_query__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in celestia/minfee/v1/query_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NetworkMinGasPrice = channel.unary_unary('/celestia.minfee.v1.Query/NetworkMinGasPrice', request_serializer=celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPrice.SerializeToString, response_deserializer=celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPriceResponse.FromString, _registered_method=True)

class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def NetworkMinGasPrice(self, request, context):
        """NetworkMinGasPrice queries the network wide minimum gas price.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'NetworkMinGasPrice': grpc.unary_unary_rpc_method_handler(servicer.NetworkMinGasPrice, request_deserializer=celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPrice.FromString, response_serializer=celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPriceResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('celestia.minfee.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('celestia.minfee.v1.Query', rpc_method_handlers)

class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def NetworkMinGasPrice(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.minfee.v1.Query/NetworkMinGasPrice', celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPrice.SerializeToString, celestia_dot_minfee_dot_v1_dot_query__pb2.QueryNetworkMinGasPriceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)