from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Upgrade(_message.Message):
    __slots__ = ('app_version', 'upgrade_height')
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    app_version: int
    upgrade_height: int

    def __init__(self, app_version: _Optional[int]=..., upgrade_height: _Optional[int]=...) -> None:
        ...