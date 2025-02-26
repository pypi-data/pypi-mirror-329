from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ('bond_denom',)
    BOND_DENOM_FIELD_NUMBER: _ClassVar[int]
    bond_denom: str

    def __init__(self, bond_denom: _Optional[str]=...) -> None:
        ...