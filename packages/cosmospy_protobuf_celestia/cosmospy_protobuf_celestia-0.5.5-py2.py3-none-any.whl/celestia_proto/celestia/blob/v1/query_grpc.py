import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import celestia

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[celestia.blob.v1.query_pb2.QueryParamsRequest, celestia.blob.v1.query_pb2.QueryParamsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/celestia.blob.v1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, celestia.blob.v1.query_pb2.QueryParamsRequest, celestia.blob.v1.query_pb2.QueryParamsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/celestia.blob.v1.Query/Params', celestia.blob.v1.query_pb2.QueryParamsRequest, celestia.blob.v1.query_pb2.QueryParamsResponse)