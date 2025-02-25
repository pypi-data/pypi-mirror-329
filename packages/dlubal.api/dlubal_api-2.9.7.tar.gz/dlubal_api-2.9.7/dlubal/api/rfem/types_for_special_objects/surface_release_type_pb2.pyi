from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceReleaseTypeLocalAxisSystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_LOCAL_AXIS_SYSTEM_TYPE_SAME_AS_ORIGINAL_SURFACE: _ClassVar[SurfaceReleaseTypeLocalAxisSystemType]
    SURFACE_RELEASE_TYPE_LOCAL_AXIS_SYSTEM_TYPE_REVERSED_TO_ORIGINAL_SURFACE: _ClassVar[SurfaceReleaseTypeLocalAxisSystemType]

class SurfaceReleaseTypeTranslationalReleaseUXNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_NONE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity]

class SurfaceReleaseTypeTranslationalReleaseUYNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_NONE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity]

class SurfaceReleaseTypeTranslationalReleaseUZNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_NONE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]
    SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: _ClassVar[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity]

class SurfaceReleaseTypeDiagramAlongXStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongXStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongXStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongXStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongXStart]

class SurfaceReleaseTypeDiagramAlongYStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongYStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongYStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongYStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongYStart]

class SurfaceReleaseTypeDiagramAlongZStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongZStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongZStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongZStart]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongZStart]

class SurfaceReleaseTypeDiagramAlongXEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongXEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongXEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongXEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongXEnd]

class SurfaceReleaseTypeDiagramAlongYEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongYEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongYEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongYEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongYEnd]

class SurfaceReleaseTypeDiagramAlongZEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[SurfaceReleaseTypeDiagramAlongZEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[SurfaceReleaseTypeDiagramAlongZEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[SurfaceReleaseTypeDiagramAlongZEnd]
    SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[SurfaceReleaseTypeDiagramAlongZEnd]
SURFACE_RELEASE_TYPE_LOCAL_AXIS_SYSTEM_TYPE_SAME_AS_ORIGINAL_SURFACE: SurfaceReleaseTypeLocalAxisSystemType
SURFACE_RELEASE_TYPE_LOCAL_AXIS_SYSTEM_TYPE_REVERSED_TO_ORIGINAL_SURFACE: SurfaceReleaseTypeLocalAxisSystemType
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_NONE: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_NONE: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_NONE: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_ALL_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FAILURE_IF_POSITIVE: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FORCE_MOMENT_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_FRICTION_DIRECTION_2: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_PARTIAL_ACTIVITY: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_TYPE_STIFFNESS_DIAGRAM: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongXStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongXStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongXStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongXStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongYStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongYStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongYStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_START_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongYStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongZStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongZStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongZStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_START_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongZStart
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongXEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongXEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongXEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongXEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongYEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongYEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongYEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Y_END_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongYEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_FAILURE: SurfaceReleaseTypeDiagramAlongZEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: SurfaceReleaseTypeDiagramAlongZEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_STOP: SurfaceReleaseTypeDiagramAlongZEnd
SURFACE_RELEASE_TYPE_DIAGRAM_ALONG_Z_END_DIAGRAM_ENDING_TYPE_YIELDING: SurfaceReleaseTypeDiagramAlongZEnd

class SurfaceReleaseType(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "surface_releases", "translational_release_u_x", "translational_release_u_y", "translational_release_u_z", "comment", "is_generated", "generating_object_info", "local_axis_system_type", "translational_release_u_x_nonlinearity", "translational_release_u_y_nonlinearity", "translational_release_u_z_nonlinearity", "diagram_along_x_symmetric", "diagram_along_y_symmetric", "diagram_along_z_symmetric", "diagram_along_x_is_sorted", "diagram_along_y_is_sorted", "diagram_along_z_is_sorted", "diagram_along_x_table", "diagram_along_y_table", "diagram_along_z_table", "diagram_along_x_start", "diagram_along_y_start", "diagram_along_z_start", "diagram_along_x_end", "diagram_along_y_end", "diagram_along_z_end", "diagram_along_x_ac_yield_minus", "diagram_along_y_ac_yield_minus", "diagram_along_z_ac_yield_minus", "diagram_along_x_ac_yield_plus", "diagram_along_y_ac_yield_plus", "diagram_along_z_ac_yield_plus", "diagram_along_x_acceptance_criteria_active", "diagram_along_y_acceptance_criteria_active", "diagram_along_z_acceptance_criteria_active", "diagram_along_x_minus_color_one", "diagram_along_y_minus_color_one", "diagram_along_z_minus_color_one", "diagram_along_x_minus_color_two", "diagram_along_y_minus_color_two", "diagram_along_z_minus_color_two", "diagram_along_x_plus_color_one", "diagram_along_y_plus_color_one", "diagram_along_z_plus_color_one", "diagram_along_x_plus_color_two", "diagram_along_y_plus_color_two", "diagram_along_z_plus_color_two", "diagram_along_x_color_table", "diagram_along_y_color_table", "diagram_along_z_color_table", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURFACE_RELEASES_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_X_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_Y_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_Z_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    LOCAL_AXIS_SYSTEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_X_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_Y_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONAL_RELEASE_U_Z_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    surface_releases: _containers.RepeatedScalarFieldContainer[int]
    translational_release_u_x: float
    translational_release_u_y: float
    translational_release_u_z: float
    comment: str
    is_generated: bool
    generating_object_info: str
    local_axis_system_type: SurfaceReleaseTypeLocalAxisSystemType
    translational_release_u_x_nonlinearity: SurfaceReleaseTypeTranslationalReleaseUXNonlinearity
    translational_release_u_y_nonlinearity: SurfaceReleaseTypeTranslationalReleaseUYNonlinearity
    translational_release_u_z_nonlinearity: SurfaceReleaseTypeTranslationalReleaseUZNonlinearity
    diagram_along_x_symmetric: bool
    diagram_along_y_symmetric: bool
    diagram_along_z_symmetric: bool
    diagram_along_x_is_sorted: bool
    diagram_along_y_is_sorted: bool
    diagram_along_z_is_sorted: bool
    diagram_along_x_table: SurfaceReleaseTypeDiagramAlongXTable
    diagram_along_y_table: SurfaceReleaseTypeDiagramAlongYTable
    diagram_along_z_table: SurfaceReleaseTypeDiagramAlongZTable
    diagram_along_x_start: SurfaceReleaseTypeDiagramAlongXStart
    diagram_along_y_start: SurfaceReleaseTypeDiagramAlongYStart
    diagram_along_z_start: SurfaceReleaseTypeDiagramAlongZStart
    diagram_along_x_end: SurfaceReleaseTypeDiagramAlongXEnd
    diagram_along_y_end: SurfaceReleaseTypeDiagramAlongYEnd
    diagram_along_z_end: SurfaceReleaseTypeDiagramAlongZEnd
    diagram_along_x_ac_yield_minus: float
    diagram_along_y_ac_yield_minus: float
    diagram_along_z_ac_yield_minus: float
    diagram_along_x_ac_yield_plus: float
    diagram_along_y_ac_yield_plus: float
    diagram_along_z_ac_yield_plus: float
    diagram_along_x_acceptance_criteria_active: bool
    diagram_along_y_acceptance_criteria_active: bool
    diagram_along_z_acceptance_criteria_active: bool
    diagram_along_x_minus_color_one: _common_pb2.Color
    diagram_along_y_minus_color_one: _common_pb2.Color
    diagram_along_z_minus_color_one: _common_pb2.Color
    diagram_along_x_minus_color_two: _common_pb2.Color
    diagram_along_y_minus_color_two: _common_pb2.Color
    diagram_along_z_minus_color_two: _common_pb2.Color
    diagram_along_x_plus_color_one: _common_pb2.Color
    diagram_along_y_plus_color_one: _common_pb2.Color
    diagram_along_z_plus_color_one: _common_pb2.Color
    diagram_along_x_plus_color_two: _common_pb2.Color
    diagram_along_y_plus_color_two: _common_pb2.Color
    diagram_along_z_plus_color_two: _common_pb2.Color
    diagram_along_x_color_table: SurfaceReleaseTypeDiagramAlongXColorTable
    diagram_along_y_color_table: SurfaceReleaseTypeDiagramAlongYColorTable
    diagram_along_z_color_table: SurfaceReleaseTypeDiagramAlongZColorTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., surface_releases: _Optional[_Iterable[int]] = ..., translational_release_u_x: _Optional[float] = ..., translational_release_u_y: _Optional[float] = ..., translational_release_u_z: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., local_axis_system_type: _Optional[_Union[SurfaceReleaseTypeLocalAxisSystemType, str]] = ..., translational_release_u_x_nonlinearity: _Optional[_Union[SurfaceReleaseTypeTranslationalReleaseUXNonlinearity, str]] = ..., translational_release_u_y_nonlinearity: _Optional[_Union[SurfaceReleaseTypeTranslationalReleaseUYNonlinearity, str]] = ..., translational_release_u_z_nonlinearity: _Optional[_Union[SurfaceReleaseTypeTranslationalReleaseUZNonlinearity, str]] = ..., diagram_along_x_symmetric: bool = ..., diagram_along_y_symmetric: bool = ..., diagram_along_z_symmetric: bool = ..., diagram_along_x_is_sorted: bool = ..., diagram_along_y_is_sorted: bool = ..., diagram_along_z_is_sorted: bool = ..., diagram_along_x_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongXTable, _Mapping]] = ..., diagram_along_y_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongYTable, _Mapping]] = ..., diagram_along_z_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongZTable, _Mapping]] = ..., diagram_along_x_start: _Optional[_Union[SurfaceReleaseTypeDiagramAlongXStart, str]] = ..., diagram_along_y_start: _Optional[_Union[SurfaceReleaseTypeDiagramAlongYStart, str]] = ..., diagram_along_z_start: _Optional[_Union[SurfaceReleaseTypeDiagramAlongZStart, str]] = ..., diagram_along_x_end: _Optional[_Union[SurfaceReleaseTypeDiagramAlongXEnd, str]] = ..., diagram_along_y_end: _Optional[_Union[SurfaceReleaseTypeDiagramAlongYEnd, str]] = ..., diagram_along_z_end: _Optional[_Union[SurfaceReleaseTypeDiagramAlongZEnd, str]] = ..., diagram_along_x_ac_yield_minus: _Optional[float] = ..., diagram_along_y_ac_yield_minus: _Optional[float] = ..., diagram_along_z_ac_yield_minus: _Optional[float] = ..., diagram_along_x_ac_yield_plus: _Optional[float] = ..., diagram_along_y_ac_yield_plus: _Optional[float] = ..., diagram_along_z_ac_yield_plus: _Optional[float] = ..., diagram_along_x_acceptance_criteria_active: bool = ..., diagram_along_y_acceptance_criteria_active: bool = ..., diagram_along_z_acceptance_criteria_active: bool = ..., diagram_along_x_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_color_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongXColorTable, _Mapping]] = ..., diagram_along_y_color_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongYColorTable, _Mapping]] = ..., diagram_along_z_color_table: _Optional[_Union[SurfaceReleaseTypeDiagramAlongZColorTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongXTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongXTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongXTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongXTableRow(_message.Message):
    __slots__ = ("no", "description", "displacement", "force", "spring", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    SPRING_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    displacement: float
    force: float
    spring: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongYTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongYTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongYTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongYTableRow(_message.Message):
    __slots__ = ("no", "description", "displacement", "force", "spring", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    SPRING_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    displacement: float
    force: float
    spring: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongZTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongZTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongZTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongZTableRow(_message.Message):
    __slots__ = ("no", "description", "displacement", "force", "spring", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    SPRING_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    displacement: float
    force: float
    spring: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongXColorTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongXColorTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongXColorTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongXColorTableRow(_message.Message):
    __slots__ = ("no", "description", "color")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    color: _common_pb2.Color
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongYColorTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongYColorTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongYColorTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongYColorTableRow(_message.Message):
    __slots__ = ("no", "description", "color")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    color: _common_pb2.Color
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongZColorTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceReleaseTypeDiagramAlongZColorTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceReleaseTypeDiagramAlongZColorTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceReleaseTypeDiagramAlongZColorTableRow(_message.Message):
    __slots__ = ("no", "description", "color")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    color: _common_pb2.Color
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
