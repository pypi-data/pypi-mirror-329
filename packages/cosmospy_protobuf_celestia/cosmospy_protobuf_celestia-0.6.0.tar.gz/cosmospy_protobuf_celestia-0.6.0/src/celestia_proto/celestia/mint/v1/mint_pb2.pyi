from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Minter(_message.Message):
    __slots__ = ('inflation_rate', 'annual_provisions', 'previous_block_time', 'bond_denom')
    INFLATION_RATE_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_BLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    BOND_DENOM_FIELD_NUMBER: _ClassVar[int]
    inflation_rate: str
    annual_provisions: str
    previous_block_time: _timestamp_pb2.Timestamp
    bond_denom: str

    def __init__(self, inflation_rate: _Optional[str]=..., annual_provisions: _Optional[str]=..., previous_block_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., bond_denom: _Optional[str]=...) -> None:
        ...

class GenesisTime(_message.Message):
    __slots__ = ('genesis_time',)
    GENESIS_TIME_FIELD_NUMBER: _ClassVar[int]
    genesis_time: _timestamp_pb2.Timestamp

    def __init__(self, genesis_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...