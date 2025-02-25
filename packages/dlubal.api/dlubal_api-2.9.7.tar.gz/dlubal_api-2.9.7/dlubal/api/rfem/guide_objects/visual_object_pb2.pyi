from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VisualObjectInsertPoint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VISUAL_OBJECT_INSERT_POINT_CENTER: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MX: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MXMYMZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MXMYPZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MXPYMZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MXPYPZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MY: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_MZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PX: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PXMYMZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PXMYPZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PXPYMZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PXPYPZ: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PY: _ClassVar[VisualObjectInsertPoint]
    VISUAL_OBJECT_INSERT_POINT_PZ: _ClassVar[VisualObjectInsertPoint]

class VisualObjectRotationAnglesSequence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_UVW: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_UWV: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_VUW: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_VWU: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_WUV: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_WVU: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_XZY: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_YXZ: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_YZX: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_ZXY: _ClassVar[VisualObjectRotationAnglesSequence]
    VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_ZYX: _ClassVar[VisualObjectRotationAnglesSequence]
VISUAL_OBJECT_INSERT_POINT_CENTER: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MX: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MXMYMZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MXMYPZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MXPYMZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MXPYPZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MY: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_MZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PX: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PXMYMZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PXMYPZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PXPYMZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PXPYPZ: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PY: VisualObjectInsertPoint
VISUAL_OBJECT_INSERT_POINT_PZ: VisualObjectInsertPoint
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_UVW: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_UWV: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_VUW: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_VWU: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_WUV: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_WVU: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_XZY: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_YXZ: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_YZX: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_ZXY: VisualObjectRotationAnglesSequence
VISUAL_OBJECT_ROTATION_ANGLES_SEQUENCE_ZYX: VisualObjectRotationAnglesSequence

class VisualObject(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "file_path", "file_name", "coordinate_system", "insert_point", "origin_coordinates", "origin_coordinate_x", "origin_coordinate_y", "origin_coordinate_z", "rotation_angles_sequence", "rotation_angle_1", "rotation_angle_2", "rotation_angle_3", "scale_is_nonuniform", "scale_is_defined_as_relative", "scale_absolute", "scale_relative", "scale_absolute_x", "scale_absolute_y", "scale_absolute_z", "scale_relative_x", "scale_relative_y", "scale_relative_z", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    INSERT_POINT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLES_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_1_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_2_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_3_FIELD_NUMBER: _ClassVar[int]
    SCALE_IS_NONUNIFORM_FIELD_NUMBER: _ClassVar[int]
    SCALE_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    SCALE_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    SCALE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    SCALE_ABSOLUTE_X_FIELD_NUMBER: _ClassVar[int]
    SCALE_ABSOLUTE_Y_FIELD_NUMBER: _ClassVar[int]
    SCALE_ABSOLUTE_Z_FIELD_NUMBER: _ClassVar[int]
    SCALE_RELATIVE_X_FIELD_NUMBER: _ClassVar[int]
    SCALE_RELATIVE_Y_FIELD_NUMBER: _ClassVar[int]
    SCALE_RELATIVE_Z_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    file_path: str
    file_name: str
    coordinate_system: int
    insert_point: VisualObjectInsertPoint
    origin_coordinates: _common_pb2.Vector3d
    origin_coordinate_x: float
    origin_coordinate_y: float
    origin_coordinate_z: float
    rotation_angles_sequence: VisualObjectRotationAnglesSequence
    rotation_angle_1: float
    rotation_angle_2: float
    rotation_angle_3: float
    scale_is_nonuniform: bool
    scale_is_defined_as_relative: bool
    scale_absolute: float
    scale_relative: float
    scale_absolute_x: float
    scale_absolute_y: float
    scale_absolute_z: float
    scale_relative_x: float
    scale_relative_y: float
    scale_relative_z: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., file_path: _Optional[str] = ..., file_name: _Optional[str] = ..., coordinate_system: _Optional[int] = ..., insert_point: _Optional[_Union[VisualObjectInsertPoint, str]] = ..., origin_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., origin_coordinate_x: _Optional[float] = ..., origin_coordinate_y: _Optional[float] = ..., origin_coordinate_z: _Optional[float] = ..., rotation_angles_sequence: _Optional[_Union[VisualObjectRotationAnglesSequence, str]] = ..., rotation_angle_1: _Optional[float] = ..., rotation_angle_2: _Optional[float] = ..., rotation_angle_3: _Optional[float] = ..., scale_is_nonuniform: bool = ..., scale_is_defined_as_relative: bool = ..., scale_absolute: _Optional[float] = ..., scale_relative: _Optional[float] = ..., scale_absolute_x: _Optional[float] = ..., scale_absolute_y: _Optional[float] = ..., scale_absolute_z: _Optional[float] = ..., scale_relative_x: _Optional[float] = ..., scale_relative_y: _Optional[float] = ..., scale_relative_z: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
