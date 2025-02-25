from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CoordinateSystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COORDINATE_SYSTEM_TYPE_UNKNOWN: _ClassVar[CoordinateSystemType]
    COORDINATE_SYSTEM_TYPE_2_POINTS_AND_ANGLE: _ClassVar[CoordinateSystemType]
    COORDINATE_SYSTEM_TYPE_3_POINTS: _ClassVar[CoordinateSystemType]
    COORDINATE_SYSTEM_TYPE_GLOBAL_XYZ: _ClassVar[CoordinateSystemType]
    COORDINATE_SYSTEM_TYPE_OFFSET_XYZ: _ClassVar[CoordinateSystemType]
    COORDINATE_SYSTEM_TYPE_POINT_AND_3_ANGLES: _ClassVar[CoordinateSystemType]

class CoordinateSystemRotationAnglesSequence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_XYZ: _ClassVar[CoordinateSystemRotationAnglesSequence]
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_XZY: _ClassVar[CoordinateSystemRotationAnglesSequence]
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_YXZ: _ClassVar[CoordinateSystemRotationAnglesSequence]
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_YZX: _ClassVar[CoordinateSystemRotationAnglesSequence]
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_ZXY: _ClassVar[CoordinateSystemRotationAnglesSequence]
    COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_ZYX: _ClassVar[CoordinateSystemRotationAnglesSequence]
COORDINATE_SYSTEM_TYPE_UNKNOWN: CoordinateSystemType
COORDINATE_SYSTEM_TYPE_2_POINTS_AND_ANGLE: CoordinateSystemType
COORDINATE_SYSTEM_TYPE_3_POINTS: CoordinateSystemType
COORDINATE_SYSTEM_TYPE_GLOBAL_XYZ: CoordinateSystemType
COORDINATE_SYSTEM_TYPE_OFFSET_XYZ: CoordinateSystemType
COORDINATE_SYSTEM_TYPE_POINT_AND_3_ANGLES: CoordinateSystemType
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_XYZ: CoordinateSystemRotationAnglesSequence
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_XZY: CoordinateSystemRotationAnglesSequence
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_YXZ: CoordinateSystemRotationAnglesSequence
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_YZX: CoordinateSystemRotationAnglesSequence
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_ZXY: CoordinateSystemRotationAnglesSequence
COORDINATE_SYSTEM_ROTATION_ANGLES_SEQUENCE_ZYX: CoordinateSystemRotationAnglesSequence

class CoordinateSystem(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "origin_coordinates", "origin_coordinate_x", "origin_coordinate_y", "origin_coordinate_z", "u_axis_point_coordinates", "u_axis_point_coordinate_x", "u_axis_point_coordinate_y", "u_axis_point_coordinate_z", "uw_plane_point_coordinates", "uw_plane_point_coordinate_x", "uw_plane_point_coordinate_y", "uw_plane_point_coordinate_z", "uw_plane_angle", "rotation_angles_sequence", "rotation_angle_1", "rotation_angle_2", "rotation_angle_3", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    UW_PLANE_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    UW_PLANE_POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    UW_PLANE_POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    UW_PLANE_POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    UW_PLANE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLES_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_1_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_2_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_3_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: CoordinateSystemType
    user_defined_name_enabled: bool
    name: str
    origin_coordinates: _common_pb2.Vector3d
    origin_coordinate_x: float
    origin_coordinate_y: float
    origin_coordinate_z: float
    u_axis_point_coordinates: _common_pb2.Vector3d
    u_axis_point_coordinate_x: float
    u_axis_point_coordinate_y: float
    u_axis_point_coordinate_z: float
    uw_plane_point_coordinates: _common_pb2.Vector3d
    uw_plane_point_coordinate_x: float
    uw_plane_point_coordinate_y: float
    uw_plane_point_coordinate_z: float
    uw_plane_angle: float
    rotation_angles_sequence: CoordinateSystemRotationAnglesSequence
    rotation_angle_1: float
    rotation_angle_2: float
    rotation_angle_3: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[CoordinateSystemType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., origin_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., origin_coordinate_x: _Optional[float] = ..., origin_coordinate_y: _Optional[float] = ..., origin_coordinate_z: _Optional[float] = ..., u_axis_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., u_axis_point_coordinate_x: _Optional[float] = ..., u_axis_point_coordinate_y: _Optional[float] = ..., u_axis_point_coordinate_z: _Optional[float] = ..., uw_plane_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., uw_plane_point_coordinate_x: _Optional[float] = ..., uw_plane_point_coordinate_y: _Optional[float] = ..., uw_plane_point_coordinate_z: _Optional[float] = ..., uw_plane_angle: _Optional[float] = ..., rotation_angles_sequence: _Optional[_Union[CoordinateSystemRotationAnglesSequence, str]] = ..., rotation_angle_1: _Optional[float] = ..., rotation_angle_2: _Optional[float] = ..., rotation_angle_3: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
