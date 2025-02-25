from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreeConcentratedLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_CONCENTRATED_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[FreeConcentratedLoadLoadType]
    FREE_CONCENTRATED_LOAD_LOAD_TYPE_FORCE: _ClassVar[FreeConcentratedLoadLoadType]
    FREE_CONCENTRATED_LOAD_LOAD_TYPE_MOMENT: _ClassVar[FreeConcentratedLoadLoadType]

class FreeConcentratedLoadLoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreeConcentratedLoadLoadProjection]
    FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreeConcentratedLoadLoadProjection]
    FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreeConcentratedLoadLoadProjection]

class FreeConcentratedLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_X: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_Y: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_Z: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_U: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_V: _ClassVar[FreeConcentratedLoadLoadDirection]
    FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_W: _ClassVar[FreeConcentratedLoadLoadDirection]
FREE_CONCENTRATED_LOAD_LOAD_TYPE_UNKNOWN: FreeConcentratedLoadLoadType
FREE_CONCENTRATED_LOAD_LOAD_TYPE_FORCE: FreeConcentratedLoadLoadType
FREE_CONCENTRATED_LOAD_LOAD_TYPE_MOMENT: FreeConcentratedLoadLoadType
FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_XY_OR_UV: FreeConcentratedLoadLoadProjection
FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_XZ_OR_UW: FreeConcentratedLoadLoadProjection
FREE_CONCENTRATED_LOAD_LOAD_PROJECTION_YZ_OR_VW: FreeConcentratedLoadLoadProjection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_X: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_X: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_Y: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_GLOBAL_Z: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_Y: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_LOCAL_Z: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_U: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_V: FreeConcentratedLoadLoadDirection
FREE_CONCENTRATED_LOAD_LOAD_DIRECTION_USER_DEFINED_W: FreeConcentratedLoadLoadDirection

class FreeConcentratedLoad(_message.Message):
    __slots__ = ("no", "load_type", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "magnitude", "load_location_x", "load_location_y", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_PROJECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_FROM_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_TO_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_Y_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: FreeConcentratedLoadLoadType
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreeConcentratedLoadLoadProjection
    load_direction: FreeConcentratedLoadLoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    magnitude: float
    load_location_x: float
    load_location_y: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[FreeConcentratedLoadLoadType, str]] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreeConcentratedLoadLoadProjection, str]] = ..., load_direction: _Optional[_Union[FreeConcentratedLoadLoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., magnitude: _Optional[float] = ..., load_location_x: _Optional[float] = ..., load_location_y: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
