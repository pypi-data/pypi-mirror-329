from gogoproto import gogo_pb2 as _gogo_pb2
from celestia.qgb.v1 import types_pb2 as _types_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ('data_commitment_window',)
    DATA_COMMITMENT_WINDOW_FIELD_NUMBER: _ClassVar[int]
    data_commitment_window: int

    def __init__(self, data_commitment_window: _Optional[int]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ('params',)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: Params

    def __init__(self, params: _Optional[_Union[Params, _Mapping]]=...) -> None:
        ...