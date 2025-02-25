"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from ....celestia.qgb.v1 import query_pb2 as celestia_dot_qgb_dot_v1_dot_query__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in celestia/qgb/v1/query_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary('/celestia.qgb.v1.Query/Params', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsResponse.FromString, _registered_method=True)
        self.AttestationRequestByNonce = channel.unary_unary('/celestia.qgb.v1.Query/AttestationRequestByNonce', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceResponse.FromString, _registered_method=True)
        self.LatestAttestationNonce = channel.unary_unary('/celestia.qgb.v1.Query/LatestAttestationNonce', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceResponse.FromString, _registered_method=True)
        self.EarliestAttestationNonce = channel.unary_unary('/celestia.qgb.v1.Query/EarliestAttestationNonce', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceResponse.FromString, _registered_method=True)
        self.LatestValsetRequestBeforeNonce = channel.unary_unary('/celestia.qgb.v1.Query/LatestValsetRequestBeforeNonce', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceResponse.FromString, _registered_method=True)
        self.LatestUnbondingHeight = channel.unary_unary('/celestia.qgb.v1.Query/LatestUnbondingHeight', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightResponse.FromString, _registered_method=True)
        self.DataCommitmentRangeForHeight = channel.unary_unary('/celestia.qgb.v1.Query/DataCommitmentRangeForHeight', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightResponse.FromString, _registered_method=True)
        self.LatestDataCommitment = channel.unary_unary('/celestia.qgb.v1.Query/LatestDataCommitment', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentResponse.FromString, _registered_method=True)
        self.EVMAddress = channel.unary_unary('/celestia.qgb.v1.Query/EVMAddress', request_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressRequest.SerializeToString, response_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressResponse.FromString, _registered_method=True)

class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Params(self, request, context):
        """Params queries the current parameters for the blobstream module
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AttestationRequestByNonce(self, request, context):
        """queries for attestations requests waiting to be signed by an orchestrator

        AttestationRequestByNonce queries attestation request by nonce.
        Returns nil if not found.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LatestAttestationNonce(self, request, context):
        """LatestAttestationNonce queries latest attestation nonce.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EarliestAttestationNonce(self, request, context):
        """EarliestAttestationNonce queries the earliest attestation nonce.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LatestValsetRequestBeforeNonce(self, request, context):
        """LatestValsetRequestBeforeNonce Queries latest Valset request before nonce.
        And, even if the current nonce is a valset, it will return the previous
        one.
        If the provided nonce is 1, it will return an error, because, there is
        no valset before nonce 1.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LatestUnbondingHeight(self, request, context):
        """misc

        LatestUnbondingHeight returns the latest unbonding height
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DataCommitmentRangeForHeight(self, request, context):
        """DataCommitmentRangeForHeight returns the data commitment window
        that includes the provided height
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LatestDataCommitment(self, request, context):
        """LatestDataCommitment returns the latest data commitment in store
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EVMAddress(self, request, context):
        """EVMAddress returns the evm address associated with a supplied
        validator address
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'Params': grpc.unary_unary_rpc_method_handler(servicer.Params, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsResponse.SerializeToString), 'AttestationRequestByNonce': grpc.unary_unary_rpc_method_handler(servicer.AttestationRequestByNonce, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceResponse.SerializeToString), 'LatestAttestationNonce': grpc.unary_unary_rpc_method_handler(servicer.LatestAttestationNonce, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceResponse.SerializeToString), 'EarliestAttestationNonce': grpc.unary_unary_rpc_method_handler(servicer.EarliestAttestationNonce, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceResponse.SerializeToString), 'LatestValsetRequestBeforeNonce': grpc.unary_unary_rpc_method_handler(servicer.LatestValsetRequestBeforeNonce, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceResponse.SerializeToString), 'LatestUnbondingHeight': grpc.unary_unary_rpc_method_handler(servicer.LatestUnbondingHeight, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightResponse.SerializeToString), 'DataCommitmentRangeForHeight': grpc.unary_unary_rpc_method_handler(servicer.DataCommitmentRangeForHeight, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightResponse.SerializeToString), 'LatestDataCommitment': grpc.unary_unary_rpc_method_handler(servicer.LatestDataCommitment, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentResponse.SerializeToString), 'EVMAddress': grpc.unary_unary_rpc_method_handler(servicer.EVMAddress, request_deserializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressRequest.FromString, response_serializer=celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('celestia.qgb.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('celestia.qgb.v1.Query', rpc_method_handlers)

class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def Params(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/Params', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def AttestationRequestByNonce(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/AttestationRequestByNonce', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryAttestationRequestByNonceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def LatestAttestationNonce(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/LatestAttestationNonce', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestAttestationNonceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def EarliestAttestationNonce(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/EarliestAttestationNonce', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEarliestAttestationNonceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def LatestValsetRequestBeforeNonce(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/LatestValsetRequestBeforeNonce', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestValsetRequestBeforeNonceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def LatestUnbondingHeight(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/LatestUnbondingHeight', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestUnbondingHeightResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DataCommitmentRangeForHeight(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/DataCommitmentRangeForHeight', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryDataCommitmentRangeForHeightResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def LatestDataCommitment(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/LatestDataCommitment', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryLatestDataCommitmentResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def EVMAddress(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/celestia.qgb.v1.Query/EVMAddress', celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressRequest.SerializeToString, celestia_dot_qgb_dot_v1_dot_query__pb2.QueryEVMAddressResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)