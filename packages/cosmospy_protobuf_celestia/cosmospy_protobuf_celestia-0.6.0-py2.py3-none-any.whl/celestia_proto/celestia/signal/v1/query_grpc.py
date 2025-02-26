import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import google
from .... import celestia

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def VersionTally(self, stream: 'grpclib.server.Stream[celestia.signal.v1.query_pb2.QueryVersionTallyRequest, celestia.signal.v1.query_pb2.QueryVersionTallyResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetUpgrade(self, stream: 'grpclib.server.Stream[celestia.signal.v1.query_pb2.QueryGetUpgradeRequest, celestia.signal.v1.query_pb2.QueryGetUpgradeResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/celestia.signal.v1.Query/VersionTally': grpclib.const.Handler(self.VersionTally, grpclib.const.Cardinality.UNARY_UNARY, celestia.signal.v1.query_pb2.QueryVersionTallyRequest, celestia.signal.v1.query_pb2.QueryVersionTallyResponse), '/celestia.signal.v1.Query/GetUpgrade': grpclib.const.Handler(self.GetUpgrade, grpclib.const.Cardinality.UNARY_UNARY, celestia.signal.v1.query_pb2.QueryGetUpgradeRequest, celestia.signal.v1.query_pb2.QueryGetUpgradeResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.VersionTally = grpclib.client.UnaryUnaryMethod(channel, '/celestia.signal.v1.Query/VersionTally', celestia.signal.v1.query_pb2.QueryVersionTallyRequest, celestia.signal.v1.query_pb2.QueryVersionTallyResponse)
        self.GetUpgrade = grpclib.client.UnaryUnaryMethod(channel, '/celestia.signal.v1.Query/GetUpgrade', celestia.signal.v1.query_pb2.QueryGetUpgradeRequest, celestia.signal.v1.query_pb2.QueryGetUpgradeResponse)