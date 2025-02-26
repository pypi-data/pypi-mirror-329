from google.api import annotations_pb2 as _annotations_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class TxPriority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TX_PRIORITY_UNSPECIFIED: _ClassVar[TxPriority]
    TX_PRIORITY_LOW: _ClassVar[TxPriority]
    TX_PRIORITY_MEDIUM: _ClassVar[TxPriority]
    TX_PRIORITY_HIGH: _ClassVar[TxPriority]
TX_PRIORITY_UNSPECIFIED: TxPriority
TX_PRIORITY_LOW: TxPriority
TX_PRIORITY_MEDIUM: TxPriority
TX_PRIORITY_HIGH: TxPriority

class EstimateGasPriceRequest(_message.Message):
    __slots__ = ('tx_priority',)
    TX_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    tx_priority: TxPriority

    def __init__(self, tx_priority: _Optional[_Union[TxPriority, str]]=...) -> None:
        ...

class EstimateGasPriceResponse(_message.Message):
    __slots__ = ('estimated_gas_price',)
    ESTIMATED_GAS_PRICE_FIELD_NUMBER: _ClassVar[int]
    estimated_gas_price: float

    def __init__(self, estimated_gas_price: _Optional[float]=...) -> None:
        ...

class EstimateGasPriceAndUsageRequest(_message.Message):
    __slots__ = ('tx_priority', 'tx_bytes')
    TX_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TX_BYTES_FIELD_NUMBER: _ClassVar[int]
    tx_priority: TxPriority
    tx_bytes: bytes

    def __init__(self, tx_priority: _Optional[_Union[TxPriority, str]]=..., tx_bytes: _Optional[bytes]=...) -> None:
        ...

class EstimateGasPriceAndUsageResponse(_message.Message):
    __slots__ = ('estimated_gas_price', 'estimated_gas_used')
    ESTIMATED_GAS_PRICE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_GAS_USED_FIELD_NUMBER: _ClassVar[int]
    estimated_gas_price: float
    estimated_gas_used: int

    def __init__(self, estimated_gas_price: _Optional[float]=..., estimated_gas_used: _Optional[int]=...) -> None:
        ...