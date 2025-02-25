from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class BridgeValidator(_message.Message):
    __slots__ = ('power', 'evm_address')
    POWER_FIELD_NUMBER: _ClassVar[int]
    EVM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    power: int
    evm_address: str

    def __init__(self, power: _Optional[int]=..., evm_address: _Optional[str]=...) -> None:
        ...

class Valset(_message.Message):
    __slots__ = ('nonce', 'members', 'height', 'time')
    NONCE_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    nonce: int
    members: _containers.RepeatedCompositeFieldContainer[BridgeValidator]
    height: int
    time: _timestamp_pb2.Timestamp

    def __init__(self, nonce: _Optional[int]=..., members: _Optional[_Iterable[_Union[BridgeValidator, _Mapping]]]=..., height: _Optional[int]=..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class DataCommitment(_message.Message):
    __slots__ = ('nonce', 'begin_block', 'end_block', 'time')
    NONCE_FIELD_NUMBER: _ClassVar[int]
    BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    nonce: int
    begin_block: int
    end_block: int
    time: _timestamp_pb2.Timestamp

    def __init__(self, nonce: _Optional[int]=..., begin_block: _Optional[int]=..., end_block: _Optional[int]=..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...