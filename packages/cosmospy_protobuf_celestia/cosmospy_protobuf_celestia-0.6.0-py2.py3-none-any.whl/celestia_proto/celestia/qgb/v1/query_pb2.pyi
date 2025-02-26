from celestia.qgb.v1 import genesis_pb2 as _genesis_pb2
from celestia.qgb.v1 import types_pb2 as _types_pb2
from google.api import annotations_pb2 as _annotations_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ('params',)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _genesis_pb2.Params

    def __init__(self, params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryAttestationRequestByNonceRequest(_message.Message):
    __slots__ = ('nonce',)
    NONCE_FIELD_NUMBER: _ClassVar[int]
    nonce: int

    def __init__(self, nonce: _Optional[int]=...) -> None:
        ...

class QueryAttestationRequestByNonceResponse(_message.Message):
    __slots__ = ('attestation',)
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    attestation: _any_pb2.Any

    def __init__(self, attestation: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class QueryLatestAttestationNonceRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryLatestAttestationNonceResponse(_message.Message):
    __slots__ = ('nonce',)
    NONCE_FIELD_NUMBER: _ClassVar[int]
    nonce: int

    def __init__(self, nonce: _Optional[int]=...) -> None:
        ...

class QueryEarliestAttestationNonceRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryEarliestAttestationNonceResponse(_message.Message):
    __slots__ = ('nonce',)
    NONCE_FIELD_NUMBER: _ClassVar[int]
    nonce: int

    def __init__(self, nonce: _Optional[int]=...) -> None:
        ...

class QueryLatestValsetRequestBeforeNonceRequest(_message.Message):
    __slots__ = ('nonce',)
    NONCE_FIELD_NUMBER: _ClassVar[int]
    nonce: int

    def __init__(self, nonce: _Optional[int]=...) -> None:
        ...

class QueryLatestValsetRequestBeforeNonceResponse(_message.Message):
    __slots__ = ('valset',)
    VALSET_FIELD_NUMBER: _ClassVar[int]
    valset: _types_pb2.Valset

    def __init__(self, valset: _Optional[_Union[_types_pb2.Valset, _Mapping]]=...) -> None:
        ...

class QueryLatestUnbondingHeightRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryLatestUnbondingHeightResponse(_message.Message):
    __slots__ = ('height',)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int

    def __init__(self, height: _Optional[int]=...) -> None:
        ...

class QueryLatestDataCommitmentRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class QueryLatestDataCommitmentResponse(_message.Message):
    __slots__ = ('data_commitment',)
    DATA_COMMITMENT_FIELD_NUMBER: _ClassVar[int]
    data_commitment: _types_pb2.DataCommitment

    def __init__(self, data_commitment: _Optional[_Union[_types_pb2.DataCommitment, _Mapping]]=...) -> None:
        ...

class QueryDataCommitmentRangeForHeightRequest(_message.Message):
    __slots__ = ('height',)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int

    def __init__(self, height: _Optional[int]=...) -> None:
        ...

class QueryDataCommitmentRangeForHeightResponse(_message.Message):
    __slots__ = ('data_commitment',)
    DATA_COMMITMENT_FIELD_NUMBER: _ClassVar[int]
    data_commitment: _types_pb2.DataCommitment

    def __init__(self, data_commitment: _Optional[_Union[_types_pb2.DataCommitment, _Mapping]]=...) -> None:
        ...

class QueryEVMAddressRequest(_message.Message):
    __slots__ = ('validator_address',)
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    validator_address: str

    def __init__(self, validator_address: _Optional[str]=...) -> None:
        ...

class QueryEVMAddressResponse(_message.Message):
    __slots__ = ('evm_address',)
    EVM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    evm_address: str

    def __init__(self, evm_address: _Optional[str]=...) -> None:
        ...