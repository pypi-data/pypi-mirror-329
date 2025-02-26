import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import celestia
from .... import google
from .... import gogoproto
from .... import cosmos_proto
import google.protobuf.any_pb2

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryParamsRequest, celestia.qgb.v1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AttestationRequestByNonce(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceRequest, celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LatestAttestationNonce(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EarliestAttestationNonce(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LatestValsetRequestBeforeNonce(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LatestUnbondingHeight(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightRequest, celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DataCommitmentRangeForHeight(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightRequest, celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LatestDataCommitment(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentRequest, celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EVMAddress(self, stream: 'grpclib.server.Stream[celestia.qgb.v1.query_pb2.QueryEVMAddressRequest, celestia.qgb.v1.query_pb2.QueryEVMAddressResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/celestia.qgb.v1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryParamsRequest, celestia.qgb.v1.query_pb2.QueryParamsResponse), '/celestia.qgb.v1.Query/AttestationRequestByNonce': grpclib.const.Handler(self.AttestationRequestByNonce, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceRequest, celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceResponse), '/celestia.qgb.v1.Query/LatestAttestationNonce': grpclib.const.Handler(self.LatestAttestationNonce, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceResponse), '/celestia.qgb.v1.Query/EarliestAttestationNonce': grpclib.const.Handler(self.EarliestAttestationNonce, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceResponse), '/celestia.qgb.v1.Query/LatestValsetRequestBeforeNonce': grpclib.const.Handler(self.LatestValsetRequestBeforeNonce, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceResponse), '/celestia.qgb.v1.Query/LatestUnbondingHeight': grpclib.const.Handler(self.LatestUnbondingHeight, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightRequest, celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightResponse), '/celestia.qgb.v1.Query/DataCommitmentRangeForHeight': grpclib.const.Handler(self.DataCommitmentRangeForHeight, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightRequest, celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightResponse), '/celestia.qgb.v1.Query/LatestDataCommitment': grpclib.const.Handler(self.LatestDataCommitment, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentRequest, celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentResponse), '/celestia.qgb.v1.Query/EVMAddress': grpclib.const.Handler(self.EVMAddress, grpclib.const.Cardinality.UNARY_UNARY, celestia.qgb.v1.query_pb2.QueryEVMAddressRequest, celestia.qgb.v1.query_pb2.QueryEVMAddressResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/Params', celestia.qgb.v1.query_pb2.QueryParamsRequest, celestia.qgb.v1.query_pb2.QueryParamsResponse)
        self.AttestationRequestByNonce = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/AttestationRequestByNonce', celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceRequest, celestia.qgb.v1.query_pb2.QueryAttestationRequestByNonceResponse)
        self.LatestAttestationNonce = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/LatestAttestationNonce', celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestAttestationNonceResponse)
        self.EarliestAttestationNonce = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/EarliestAttestationNonce', celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceRequest, celestia.qgb.v1.query_pb2.QueryEarliestAttestationNonceResponse)
        self.LatestValsetRequestBeforeNonce = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/LatestValsetRequestBeforeNonce', celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceRequest, celestia.qgb.v1.query_pb2.QueryLatestValsetRequestBeforeNonceResponse)
        self.LatestUnbondingHeight = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/LatestUnbondingHeight', celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightRequest, celestia.qgb.v1.query_pb2.QueryLatestUnbondingHeightResponse)
        self.DataCommitmentRangeForHeight = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/DataCommitmentRangeForHeight', celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightRequest, celestia.qgb.v1.query_pb2.QueryDataCommitmentRangeForHeightResponse)
        self.LatestDataCommitment = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/LatestDataCommitment', celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentRequest, celestia.qgb.v1.query_pb2.QueryLatestDataCommitmentResponse)
        self.EVMAddress = grpclib.client.UnaryUnaryMethod(channel, '/celestia.qgb.v1.Query/EVMAddress', celestia.qgb.v1.query_pb2.QueryEVMAddressRequest, celestia.qgb.v1.query_pb2.QueryEVMAddressResponse)