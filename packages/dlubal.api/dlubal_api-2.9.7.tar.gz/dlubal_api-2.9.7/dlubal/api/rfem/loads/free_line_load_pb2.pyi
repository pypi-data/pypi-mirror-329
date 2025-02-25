from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreeLineLoadLoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_LINE_LOAD_LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreeLineLoadLoadProjection]
    FREE_LINE_LOAD_LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreeLineLoadLoadProjection]
    FREE_LINE_LOAD_LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreeLineLoadLoadProjection]

class FreeLineLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: _ClassVar[FreeLineLoadLoadDirection]
    FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: _ClassVar[FreeLineLoadLoadDirection]

class FreeLineLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_LINE_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[FreeLineLoadLoadDistribution]
    FREE_LINE_LOAD_LOAD_DISTRIBUTION_LINEAR: _ClassVar[FreeLineLoadLoadDistribution]
    FREE_LINE_LOAD_LOAD_DISTRIBUTION_VARYING: _ClassVar[FreeLineLoadLoadDistribution]
FREE_LINE_LOAD_LOAD_PROJECTION_XY_OR_UV: FreeLineLoadLoadProjection
FREE_LINE_LOAD_LOAD_PROJECTION_XZ_OR_UW: FreeLineLoadLoadProjection
FREE_LINE_LOAD_LOAD_PROJECTION_YZ_OR_VW: FreeLineLoadLoadProjection
FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_X: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_Y: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_LOCAL_Z: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: FreeLineLoadLoadDirection
FREE_LINE_LOAD_LOAD_DISTRIBUTION_UNIFORM: FreeLineLoadLoadDistribution
FREE_LINE_LOAD_LOAD_DISTRIBUTION_LINEAR: FreeLineLoadLoadDistribution
FREE_LINE_LOAD_LOAD_DISTRIBUTION_VARYING: FreeLineLoadLoadDistribution

class FreeLineLoad(_message.Message):
    __slots__ = ("no", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "load_distribution", "magnitude_uniform", "magnitude_first", "magnitude_second", "load_location_first_x", "load_location_first_y", "load_location_second_x", "load_location_second_y", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_PROJECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_FROM_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_TO_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIRST_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_SECOND_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_Y_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_Y_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreeLineLoadLoadProjection
    load_direction: FreeLineLoadLoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    load_distribution: FreeLineLoadLoadDistribution
    magnitude_uniform: float
    magnitude_first: float
    magnitude_second: float
    load_location_first_x: float
    load_location_first_y: float
    load_location_second_x: float
    load_location_second_y: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreeLineLoadLoadProjection, str]] = ..., load_direction: _Optional[_Union[FreeLineLoadLoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., load_distribution: _Optional[_Union[FreeLineLoadLoadDistribution, str]] = ..., magnitude_uniform: _Optional[float] = ..., magnitude_first: _Optional[float] = ..., magnitude_second: _Optional[float] = ..., load_location_first_x: _Optional[float] = ..., load_location_first_y: _Optional[float] = ..., load_location_second_x: _Optional[float] = ..., load_location_second_y: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
