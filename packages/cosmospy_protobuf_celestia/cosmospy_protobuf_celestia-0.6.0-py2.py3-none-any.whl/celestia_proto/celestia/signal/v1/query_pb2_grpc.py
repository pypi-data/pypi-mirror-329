"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from ....celestia.signal.v1 import query_pb2 as celestia_dot_signal_dot_v1_dot_query__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in celestia/signal/v1/query_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class QueryStub(object):
    """Query defines the signal Query service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VersionTally = channel.unary_unary('/celestia.signal.v1.Query/VersionTally', request_serializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyRequest.SerializeToString, response_deserializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyResponse.FromString, _registered_method=True)
        self.GetUpgrade = channel.unary_unary('/celestia.signal.v1.Query/GetUpgrade', request_serializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeRequest.SerializeToString, response_deserializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeResponse.FromString, _registered_method=True)

class QueryServicer(object):
    """Query defines the signal Query service.
    """

    def VersionTally(self, request, context):
        """VersionTally enables a client to query for the tally of voting power that
        has signalled for a particular version.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUpgrade(self, request, context):
        """GetUpgrade enables a client to query for upgrade information if an upgrade is pending.
        The response will be empty if no upgrade is pending.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'VersionTally': grpc.unary_unary_rpc_method_handler(servicer.VersionTally, request_deserializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyRequest.FromString, response_serializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyResponse.SerializeToString), 'GetUpgrade': grpc.unary_unary_rpc_method_handler(servicer.GetUpgrade, request_deserializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeRequest.FromString, response_serializer=celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('celestia.signal.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('celestia.signal.v1.Query', rpc_method_handlers)

class Query(object):
    """Query defines the signal Query service.
    """

    @staticmethod
    def VersionTally(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.signal.v1.Query/VersionTally', celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyRequest.SerializeToString, celestia_dot_signal_dot_v1_dot_query__pb2.QueryVersionTallyResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetUpgrade(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.signal.v1.Query/GetUpgrade', celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeRequest.SerializeToString, celestia_dot_signal_dot_v1_dot_query__pb2.QueryGetUpgradeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)