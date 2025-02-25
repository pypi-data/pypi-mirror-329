from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ('gas_per_blob_byte', 'gov_max_square_size')
    GAS_PER_BLOB_BYTE_FIELD_NUMBER: _ClassVar[int]
    GOV_MAX_SQUARE_SIZE_FIELD_NUMBER: _ClassVar[int]
    gas_per_blob_byte: int
    gov_max_square_size: int

    def __init__(self, gas_per_blob_byte: _Optional[int]=..., gov_max_square_size: _Optional[int]=...) -> None:
        ...