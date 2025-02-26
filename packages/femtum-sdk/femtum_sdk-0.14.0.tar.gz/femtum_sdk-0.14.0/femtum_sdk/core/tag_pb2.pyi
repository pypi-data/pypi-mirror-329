from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Tag(_message.Message):
    __slots__ = ("Key", "Value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Key: str
    Value: str
    def __init__(self, Key: _Optional[str] = ..., Value: _Optional[str] = ...) -> None: ...
