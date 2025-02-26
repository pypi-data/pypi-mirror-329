import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import cosmos_proto
from .... import celestia

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def NetworkMinGasPrice(self, stream: 'grpclib.server.Stream[celestia.minfee.v1.query_pb2.QueryNetworkMinGasPrice, celestia.minfee.v1.query_pb2.QueryNetworkMinGasPriceResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/celestia.minfee.v1.Query/NetworkMinGasPrice': grpclib.const.Handler(self.NetworkMinGasPrice, grpclib.const.Cardinality.UNARY_UNARY, celestia.minfee.v1.query_pb2.QueryNetworkMinGasPrice, celestia.minfee.v1.query_pb2.QueryNetworkMinGasPriceResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.NetworkMinGasPrice = grpclib.client.UnaryUnaryMethod(channel, '/celestia.minfee.v1.Query/NetworkMinGasPrice', celestia.minfee.v1.query_pb2.QueryNetworkMinGasPrice, celestia.minfee.v1.query_pb2.QueryNetworkMinGasPriceResponse)