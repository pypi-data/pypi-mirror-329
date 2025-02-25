from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class QueryNetworkMinGasPrice(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryNetworkMinGasPriceResponse(_message.Message):
    __slots__ = ('network_min_gas_price',)
    NETWORK_MIN_GAS_PRICE_FIELD_NUMBER: _ClassVar[int]
    network_min_gas_price: str

    def __init__(self, network_min_gas_price: _Optional[str]=...) -> None:
        ...