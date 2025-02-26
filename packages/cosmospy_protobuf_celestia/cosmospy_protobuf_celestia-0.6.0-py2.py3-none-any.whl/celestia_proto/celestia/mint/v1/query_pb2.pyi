from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from celestia.mint.v1 import mint_pb2 as _mint_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryInflationRateRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryInflationRateResponse(_message.Message):
    __slots__ = ('inflation_rate',)
    INFLATION_RATE_FIELD_NUMBER: _ClassVar[int]
    inflation_rate: bytes

    def __init__(self, inflation_rate: _Optional[bytes]=...) -> None:
        ...

class QueryAnnualProvisionsRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryAnnualProvisionsResponse(_message.Message):
    __slots__ = ('annual_provisions',)
    ANNUAL_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    annual_provisions: bytes

    def __init__(self, annual_provisions: _Optional[bytes]=...) -> None:
        ...

class QueryGenesisTimeRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryGenesisTimeResponse(_message.Message):
    __slots__ = ('genesis_time',)
    GENESIS_TIME_FIELD_NUMBER: _ClassVar[int]
    genesis_time: _timestamp_pb2.Timestamp

    def __init__(self, genesis_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...