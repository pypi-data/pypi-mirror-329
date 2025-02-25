from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NoteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTE_TYPE_UNKNOWN: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_LINE: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_MEMBER: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_NODE: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_POINT: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_SOLID: _ClassVar[NoteType]
    NOTE_TYPE_NOTE_TYPE_SURFACE: _ClassVar[NoteType]

class NoteMemberReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTE_MEMBER_REFERENCE_TYPE_L: _ClassVar[NoteMemberReferenceType]
    NOTE_MEMBER_REFERENCE_TYPE_XY: _ClassVar[NoteMemberReferenceType]
    NOTE_MEMBER_REFERENCE_TYPE_XZ: _ClassVar[NoteMemberReferenceType]
    NOTE_MEMBER_REFERENCE_TYPE_YZ: _ClassVar[NoteMemberReferenceType]

class NoteSurfaceReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTE_SURFACE_REFERENCE_TYPE_UNKNOWN: _ClassVar[NoteSurfaceReferenceType]
    NOTE_SURFACE_REFERENCE_TYPE_XY: _ClassVar[NoteSurfaceReferenceType]
    NOTE_SURFACE_REFERENCE_TYPE_XZ: _ClassVar[NoteSurfaceReferenceType]
    NOTE_SURFACE_REFERENCE_TYPE_YZ: _ClassVar[NoteSurfaceReferenceType]

class NoteOffsetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTE_OFFSET_TYPE_XYZ: _ClassVar[NoteOffsetType]
    NOTE_OFFSET_TYPE_XY: _ClassVar[NoteOffsetType]
    NOTE_OFFSET_TYPE_XZ: _ClassVar[NoteOffsetType]
    NOTE_OFFSET_TYPE_YZ: _ClassVar[NoteOffsetType]
NOTE_TYPE_UNKNOWN: NoteType
NOTE_TYPE_NOTE_TYPE_LINE: NoteType
NOTE_TYPE_NOTE_TYPE_MEMBER: NoteType
NOTE_TYPE_NOTE_TYPE_NODE: NoteType
NOTE_TYPE_NOTE_TYPE_POINT: NoteType
NOTE_TYPE_NOTE_TYPE_SOLID: NoteType
NOTE_TYPE_NOTE_TYPE_SURFACE: NoteType
NOTE_MEMBER_REFERENCE_TYPE_L: NoteMemberReferenceType
NOTE_MEMBER_REFERENCE_TYPE_XY: NoteMemberReferenceType
NOTE_MEMBER_REFERENCE_TYPE_XZ: NoteMemberReferenceType
NOTE_MEMBER_REFERENCE_TYPE_YZ: NoteMemberReferenceType
NOTE_SURFACE_REFERENCE_TYPE_UNKNOWN: NoteSurfaceReferenceType
NOTE_SURFACE_REFERENCE_TYPE_XY: NoteSurfaceReferenceType
NOTE_SURFACE_REFERENCE_TYPE_XZ: NoteSurfaceReferenceType
NOTE_SURFACE_REFERENCE_TYPE_YZ: NoteSurfaceReferenceType
NOTE_OFFSET_TYPE_XYZ: NoteOffsetType
NOTE_OFFSET_TYPE_XY: NoteOffsetType
NOTE_OFFSET_TYPE_XZ: NoteOffsetType
NOTE_OFFSET_TYPE_YZ: NoteOffsetType

class Note(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "text", "point_coordinates", "point_coordinate_x", "point_coordinate_y", "point_coordinate_z", "node", "member", "member_reference_type", "member_length", "member_distance_is_defined_as_relative", "member_distance_relative", "member_distance_absolute", "line", "line_length", "surface", "surface_reference_type", "surface_first_coordinate", "surface_second_coordinate", "offset", "offset_type", "offset_coordinate", "offset_coordinate_x", "offset_coordinate_y", "offset_coordinate_z", "rotation", "show_comment", "display_properties_index", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    MEMBER_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    LINE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_FIRST_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_SECOND_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OFFSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SHOW_COMMENT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTIES_INDEX_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: NoteType
    user_defined_name_enabled: bool
    name: str
    text: str
    point_coordinates: _common_pb2.Vector3d
    point_coordinate_x: float
    point_coordinate_y: float
    point_coordinate_z: float
    node: int
    member: int
    member_reference_type: NoteMemberReferenceType
    member_length: float
    member_distance_is_defined_as_relative: bool
    member_distance_relative: float
    member_distance_absolute: float
    line: int
    line_length: float
    surface: int
    surface_reference_type: NoteSurfaceReferenceType
    surface_first_coordinate: float
    surface_second_coordinate: float
    offset: bool
    offset_type: NoteOffsetType
    offset_coordinate: _common_pb2.Vector3d
    offset_coordinate_x: float
    offset_coordinate_y: float
    offset_coordinate_z: float
    rotation: float
    show_comment: bool
    display_properties_index: int
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[NoteType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., text: _Optional[str] = ..., point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., point_coordinate_x: _Optional[float] = ..., point_coordinate_y: _Optional[float] = ..., point_coordinate_z: _Optional[float] = ..., node: _Optional[int] = ..., member: _Optional[int] = ..., member_reference_type: _Optional[_Union[NoteMemberReferenceType, str]] = ..., member_length: _Optional[float] = ..., member_distance_is_defined_as_relative: bool = ..., member_distance_relative: _Optional[float] = ..., member_distance_absolute: _Optional[float] = ..., line: _Optional[int] = ..., line_length: _Optional[float] = ..., surface: _Optional[int] = ..., surface_reference_type: _Optional[_Union[NoteSurfaceReferenceType, str]] = ..., surface_first_coordinate: _Optional[float] = ..., surface_second_coordinate: _Optional[float] = ..., offset: bool = ..., offset_type: _Optional[_Union[NoteOffsetType, str]] = ..., offset_coordinate: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., offset_coordinate_x: _Optional[float] = ..., offset_coordinate_y: _Optional[float] = ..., offset_coordinate_z: _Optional[float] = ..., rotation: _Optional[float] = ..., show_comment: bool = ..., display_properties_index: _Optional[int] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
