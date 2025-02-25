import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import celestia
import google.protobuf.timestamp_pb2

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def InflationRate(self, stream: 'grpclib.server.Stream[celestia.mint.v1.query_pb2.QueryInflationRateRequest, celestia.mint.v1.query_pb2.QueryInflationRateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AnnualProvisions(self, stream: 'grpclib.server.Stream[celestia.mint.v1.query_pb2.QueryAnnualProvisionsRequest, celestia.mint.v1.query_pb2.QueryAnnualProvisionsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GenesisTime(self, stream: 'grpclib.server.Stream[celestia.mint.v1.query_pb2.QueryGenesisTimeRequest, celestia.mint.v1.query_pb2.QueryGenesisTimeResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/celestia.mint.v1.Query/InflationRate': grpclib.const.Handler(self.InflationRate, grpclib.const.Cardinality.UNARY_UNARY, celestia.mint.v1.query_pb2.QueryInflationRateRequest, celestia.mint.v1.query_pb2.QueryInflationRateResponse), '/celestia.mint.v1.Query/AnnualProvisions': grpclib.const.Handler(self.AnnualProvisions, grpclib.const.Cardinality.UNARY_UNARY, celestia.mint.v1.query_pb2.QueryAnnualProvisionsRequest, celestia.mint.v1.query_pb2.QueryAnnualProvisionsResponse), '/celestia.mint.v1.Query/GenesisTime': grpclib.const.Handler(self.GenesisTime, grpclib.const.Cardinality.UNARY_UNARY, celestia.mint.v1.query_pb2.QueryGenesisTimeRequest, celestia.mint.v1.query_pb2.QueryGenesisTimeResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.InflationRate = grpclib.client.UnaryUnaryMethod(channel, '/celestia.mint.v1.Query/InflationRate', celestia.mint.v1.query_pb2.QueryInflationRateRequest, celestia.mint.v1.query_pb2.QueryInflationRateResponse)
        self.AnnualProvisions = grpclib.client.UnaryUnaryMethod(channel, '/celestia.mint.v1.Query/AnnualProvisions', celestia.mint.v1.query_pb2.QueryAnnualProvisionsRequest, celestia.mint.v1.query_pb2.QueryAnnualProvisionsResponse)
        self.GenesisTime = grpclib.client.UnaryUnaryMethod(channel, '/celestia.mint.v1.Query/GenesisTime', celestia.mint.v1.query_pb2.QueryGenesisTimeRequest, celestia.mint.v1.query_pb2.QueryGenesisTimeResponse)