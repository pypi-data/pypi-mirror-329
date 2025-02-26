from google.api import annotations_pb2 as _annotations_pb2
from celestia.signal.v1 import upgrade_pb2 as _upgrade_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryVersionTallyRequest(_message.Message):
    __slots__ = ('version',)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int

    def __init__(self, version: _Optional[int]=...) -> None:
        ...

class QueryVersionTallyResponse(_message.Message):
    __slots__ = ('voting_power', 'threshold_power', 'total_voting_power')
    VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_POWER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    voting_power: int
    threshold_power: int
    total_voting_power: int

    def __init__(self, voting_power: _Optional[int]=..., threshold_power: _Optional[int]=..., total_voting_power: _Optional[int]=...) -> None:
        ...

class QueryGetUpgradeRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryGetUpgradeResponse(_message.Message):
    __slots__ = ('upgrade',)
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    upgrade: _upgrade_pb2.Upgrade

    def __init__(self, upgrade: _Optional[_Union[_upgrade_pb2.Upgrade, _Mapping]]=...) -> None:
        ...