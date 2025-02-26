from make87_messages.core import header_pb2 as _header_pb2
from make87_messages.geometry.box import box_2d_pb2 as _box_2d_pb2
from make87_messages.geometry.box import box_2d_aligned_pb2 as _box_2d_aligned_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Box2D(_message.Message):
    __slots__ = ("header", "geometry")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    geometry: _box_2d_pb2.Box2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., geometry: _Optional[_Union[_box_2d_pb2.Box2D, _Mapping]] = ...) -> None: ...

class Box2DAxisAligned(_message.Message):
    __slots__ = ("header", "geometry")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    geometry: _box_2d_aligned_pb2.Box2DAxisAligned
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., geometry: _Optional[_Union[_box_2d_aligned_pb2.Box2DAxisAligned, _Mapping]] = ...) -> None: ...
