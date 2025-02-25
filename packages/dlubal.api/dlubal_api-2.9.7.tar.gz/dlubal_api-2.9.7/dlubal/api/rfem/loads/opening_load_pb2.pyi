from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpeningLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPENING_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[OpeningLoadLoadType]
    OPENING_LOAD_LOAD_TYPE_FORCE: _ClassVar[OpeningLoadLoadType]

class OpeningLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPENING_LOAD_LOAD_DIRECTION_UNKNOWN: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[OpeningLoadLoadDirection]
    OPENING_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[OpeningLoadLoadDirection]

class OpeningLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPENING_LOAD_LOAD_DISTRIBUTION_UNIFORM_TRAPEZOIDAL: _ClassVar[OpeningLoadLoadDistribution]
    OPENING_LOAD_LOAD_DISTRIBUTION_LINEAR_TRAPEZOIDAL: _ClassVar[OpeningLoadLoadDistribution]
OPENING_LOAD_LOAD_TYPE_UNKNOWN: OpeningLoadLoadType
OPENING_LOAD_LOAD_TYPE_FORCE: OpeningLoadLoadType
OPENING_LOAD_LOAD_DIRECTION_UNKNOWN: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DIRECTION_LOCAL_Z: OpeningLoadLoadDirection
OPENING_LOAD_LOAD_DISTRIBUTION_UNIFORM_TRAPEZOIDAL: OpeningLoadLoadDistribution
OPENING_LOAD_LOAD_DISTRIBUTION_LINEAR_TRAPEZOIDAL: OpeningLoadLoadDistribution

class OpeningLoad(_message.Message):
    __slots__ = ("no", "load_type", "openings", "load_case", "coordinate_system", "load_direction", "load_distribution", "magnitude", "magnitude_1", "magnitude_2", "magnitude_3", "node_1", "node_2", "node_3", "smooth_punctual_load_enabled", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPENINGS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_3_FIELD_NUMBER: _ClassVar[int]
    NODE_1_FIELD_NUMBER: _ClassVar[int]
    NODE_2_FIELD_NUMBER: _ClassVar[int]
    NODE_3_FIELD_NUMBER: _ClassVar[int]
    SMOOTH_PUNCTUAL_LOAD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: OpeningLoadLoadType
    openings: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: str
    load_direction: OpeningLoadLoadDirection
    load_distribution: OpeningLoadLoadDistribution
    magnitude: float
    magnitude_1: float
    magnitude_2: float
    magnitude_3: float
    node_1: int
    node_2: int
    node_3: int
    smooth_punctual_load_enabled: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[OpeningLoadLoadType, str]] = ..., openings: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[str] = ..., load_direction: _Optional[_Union[OpeningLoadLoadDirection, str]] = ..., load_distribution: _Optional[_Union[OpeningLoadLoadDistribution, str]] = ..., magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., magnitude_3: _Optional[float] = ..., node_1: _Optional[int] = ..., node_2: _Optional[int] = ..., node_3: _Optional[int] = ..., smooth_punctual_load_enabled: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
