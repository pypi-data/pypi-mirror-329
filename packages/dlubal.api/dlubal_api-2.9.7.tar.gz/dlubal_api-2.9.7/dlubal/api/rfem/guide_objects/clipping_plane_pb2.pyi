from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClippingPlaneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIPPING_PLANE_TYPE_UNKNOWN: _ClassVar[ClippingPlaneType]
    CLIPPING_PLANE_TYPE_2_POINTS_AND_ANGLE: _ClassVar[ClippingPlaneType]
    CLIPPING_PLANE_TYPE_3_POINTS: _ClassVar[ClippingPlaneType]
    CLIPPING_PLANE_TYPE_OFFSET_XYZ: _ClassVar[ClippingPlaneType]
    CLIPPING_PLANE_TYPE_POINT_AND_3_ANGLES: _ClassVar[ClippingPlaneType]

class ClippingPlaneRotationAnglesSequence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_UVW: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_UWV: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_VUW: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_VWU: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_WUV: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_WVU: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_XZY: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_YXZ: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_YZX: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_ZXY: _ClassVar[ClippingPlaneRotationAnglesSequence]
    CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_ZYX: _ClassVar[ClippingPlaneRotationAnglesSequence]

class ClippingPlaneOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_XY: _ClassVar[ClippingPlaneOrientation]
    CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_XZ: _ClassVar[ClippingPlaneOrientation]
    CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_YZ: _ClassVar[ClippingPlaneOrientation]
CLIPPING_PLANE_TYPE_UNKNOWN: ClippingPlaneType
CLIPPING_PLANE_TYPE_2_POINTS_AND_ANGLE: ClippingPlaneType
CLIPPING_PLANE_TYPE_3_POINTS: ClippingPlaneType
CLIPPING_PLANE_TYPE_OFFSET_XYZ: ClippingPlaneType
CLIPPING_PLANE_TYPE_POINT_AND_3_ANGLES: ClippingPlaneType
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_UVW: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_UWV: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_VUW: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_VWU: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_WUV: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_WVU: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_XZY: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_YXZ: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_YZX: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_ZXY: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ROTATION_ANGLES_SEQUENCE_ZYX: ClippingPlaneRotationAnglesSequence
CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_XY: ClippingPlaneOrientation
CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_XZ: ClippingPlaneOrientation
CLIPPING_PLANE_ORIENTATION_PARALLEL_TO_YZ: ClippingPlaneOrientation

class ClippingPlane(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "coordinate_system", "invert_clipping_side", "origin_coordinates", "origin_coordinate_x", "origin_coordinate_y", "origin_coordinate_z", "u_axis_point_coordinates", "u_axis_point_coordinate_x", "u_axis_point_coordinate_y", "u_axis_point_coordinate_z", "clipping_plane_point_coordinates", "clipping_plane_point_coordinate_x", "clipping_plane_point_coordinate_y", "clipping_plane_point_coordinate_z", "clipping_plane_angle", "rotation_angles_sequence", "rotation_angle_1", "rotation_angle_2", "rotation_angle_3", "orientation", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    INVERT_CLIPPING_SIDE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    U_AXIS_POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_PLANE_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_PLANE_POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_PLANE_POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_PLANE_POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_PLANE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLES_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_1_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_2_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_3_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: ClippingPlaneType
    user_defined_name_enabled: bool
    name: str
    coordinate_system: int
    invert_clipping_side: bool
    origin_coordinates: _common_pb2.Vector3d
    origin_coordinate_x: float
    origin_coordinate_y: float
    origin_coordinate_z: float
    u_axis_point_coordinates: _common_pb2.Vector3d
    u_axis_point_coordinate_x: float
    u_axis_point_coordinate_y: float
    u_axis_point_coordinate_z: float
    clipping_plane_point_coordinates: _common_pb2.Vector3d
    clipping_plane_point_coordinate_x: float
    clipping_plane_point_coordinate_y: float
    clipping_plane_point_coordinate_z: float
    clipping_plane_angle: float
    rotation_angles_sequence: ClippingPlaneRotationAnglesSequence
    rotation_angle_1: float
    rotation_angle_2: float
    rotation_angle_3: float
    orientation: ClippingPlaneOrientation
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[ClippingPlaneType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., coordinate_system: _Optional[int] = ..., invert_clipping_side: bool = ..., origin_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., origin_coordinate_x: _Optional[float] = ..., origin_coordinate_y: _Optional[float] = ..., origin_coordinate_z: _Optional[float] = ..., u_axis_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., u_axis_point_coordinate_x: _Optional[float] = ..., u_axis_point_coordinate_y: _Optional[float] = ..., u_axis_point_coordinate_z: _Optional[float] = ..., clipping_plane_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., clipping_plane_point_coordinate_x: _Optional[float] = ..., clipping_plane_point_coordinate_y: _Optional[float] = ..., clipping_plane_point_coordinate_z: _Optional[float] = ..., clipping_plane_angle: _Optional[float] = ..., rotation_angles_sequence: _Optional[_Union[ClippingPlaneRotationAnglesSequence, str]] = ..., rotation_angle_1: _Optional[float] = ..., rotation_angle_2: _Optional[float] = ..., rotation_angle_3: _Optional[float] = ..., orientation: _Optional[_Union[ClippingPlaneOrientation, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
