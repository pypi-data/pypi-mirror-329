from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreePolygonLoadLoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_POLYGON_LOAD_LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreePolygonLoadLoadProjection]
    FREE_POLYGON_LOAD_LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreePolygonLoadLoadProjection]
    FREE_POLYGON_LOAD_LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreePolygonLoadLoadProjection]

class FreePolygonLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: _ClassVar[FreePolygonLoadLoadDirection]
    FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: _ClassVar[FreePolygonLoadLoadDirection]

class FreePolygonLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[FreePolygonLoadLoadDistribution]
    FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR: _ClassVar[FreePolygonLoadLoadDistribution]
    FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR_FIRST: _ClassVar[FreePolygonLoadLoadDistribution]
    FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR_SECOND: _ClassVar[FreePolygonLoadLoadDistribution]
FREE_POLYGON_LOAD_LOAD_PROJECTION_XY_OR_UV: FreePolygonLoadLoadProjection
FREE_POLYGON_LOAD_LOAD_PROJECTION_XZ_OR_UW: FreePolygonLoadLoadProjection
FREE_POLYGON_LOAD_LOAD_PROJECTION_YZ_OR_VW: FreePolygonLoadLoadProjection
FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_X: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_Y: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_LOCAL_Z: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: FreePolygonLoadLoadDirection
FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_UNIFORM: FreePolygonLoadLoadDistribution
FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR: FreePolygonLoadLoadDistribution
FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR_FIRST: FreePolygonLoadLoadDistribution
FREE_POLYGON_LOAD_LOAD_DISTRIBUTION_LINEAR_SECOND: FreePolygonLoadLoadDistribution

class FreePolygonLoad(_message.Message):
    __slots__ = ("no", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "load_distribution", "magnitude_uniform", "magnitude_linear_1", "magnitude_linear_2", "magnitude_linear_3", "magnitude_linear_location_1", "magnitude_linear_location_2", "magnitude_linear_location_3", "load_location", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
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
    MAGNITUDE_LINEAR_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_LOCATION_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_LOCATION_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_LOCATION_3_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreePolygonLoadLoadProjection
    load_direction: FreePolygonLoadLoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    load_distribution: FreePolygonLoadLoadDistribution
    magnitude_uniform: float
    magnitude_linear_1: float
    magnitude_linear_2: float
    magnitude_linear_3: float
    magnitude_linear_location_1: int
    magnitude_linear_location_2: int
    magnitude_linear_location_3: int
    load_location: FreePolygonLoadLoadLocationTable
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreePolygonLoadLoadProjection, str]] = ..., load_direction: _Optional[_Union[FreePolygonLoadLoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., load_distribution: _Optional[_Union[FreePolygonLoadLoadDistribution, str]] = ..., magnitude_uniform: _Optional[float] = ..., magnitude_linear_1: _Optional[float] = ..., magnitude_linear_2: _Optional[float] = ..., magnitude_linear_3: _Optional[float] = ..., magnitude_linear_location_1: _Optional[int] = ..., magnitude_linear_location_2: _Optional[int] = ..., magnitude_linear_location_3: _Optional[int] = ..., load_location: _Optional[_Union[FreePolygonLoadLoadLocationTable, _Mapping]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class FreePolygonLoadLoadLocationTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[FreePolygonLoadLoadLocationRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[FreePolygonLoadLoadLocationRow, _Mapping]]] = ...) -> None: ...

class FreePolygonLoadLoadLocationRow(_message.Message):
    __slots__ = ("no", "description", "first_coordinate", "second_coordinate", "magnitude")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIRST_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SECOND_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    first_coordinate: float
    second_coordinate: float
    magnitude: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., first_coordinate: _Optional[float] = ..., second_coordinate: _Optional[float] = ..., magnitude: _Optional[float] = ...) -> None: ...
