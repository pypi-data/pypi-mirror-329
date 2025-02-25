from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SubscribeRequest(_message.Message):
    __slots__ = ("organization_id",)
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    def __init__(self, organization_id: _Optional[str] = ...) -> None: ...

class SubscribeResponse(_message.Message):
    __slots__ = ("payment_url",)
    PAYMENT_URL_FIELD_NUMBER: _ClassVar[int]
    payment_url: str
    def __init__(self, payment_url: _Optional[str] = ...) -> None: ...
