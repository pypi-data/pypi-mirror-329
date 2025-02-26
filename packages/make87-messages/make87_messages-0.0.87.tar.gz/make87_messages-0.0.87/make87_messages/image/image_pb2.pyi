from make87_messages.core import header_pb2 as _header_pb2
from make87_messages.image.uncompressed import image_gray_pb2 as _image_gray_pb2
from make87_messages.image.uncompressed import image_rgb_pb2 as _image_rgb_pb2
from make87_messages.image.uncompressed import image_rgba_pb2 as _image_rgba_pb2
from make87_messages.image.compressed import image_jpeg_pb2 as _image_jpeg_pb2
from make87_messages.image.compressed import image_png_pb2 as _image_png_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Image(_message.Message):
    __slots__ = ("header", "png", "jpeg", "gray", "rgb", "rgba")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PNG_FIELD_NUMBER: _ClassVar[int]
    JPEG_FIELD_NUMBER: _ClassVar[int]
    GRAY_FIELD_NUMBER: _ClassVar[int]
    RGB_FIELD_NUMBER: _ClassVar[int]
    RGBA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    png: _image_png_pb2.ImagePNG
    jpeg: _image_jpeg_pb2.ImageJPEG
    gray: _image_gray_pb2.ImageGray
    rgb: _image_rgb_pb2.ImageRGB
    rgba: _image_rgba_pb2.ImageRGBA
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., png: _Optional[_Union[_image_png_pb2.ImagePNG, _Mapping]] = ..., jpeg: _Optional[_Union[_image_jpeg_pb2.ImageJPEG, _Mapping]] = ..., gray: _Optional[_Union[_image_gray_pb2.ImageGray, _Mapping]] = ..., rgb: _Optional[_Union[_image_rgb_pb2.ImageRGB, _Mapping]] = ..., rgba: _Optional[_Union[_image_rgba_pb2.ImageRGBA, _Mapping]] = ...) -> None: ...
