from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResultSectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_SECTION_TYPE_UNKNOWN: _ClassVar[ResultSectionType]
    RESULT_SECTION_TYPE_2_POINTS_AND_VECTOR: _ClassVar[ResultSectionType]
    RESULT_SECTION_TYPE_LINE: _ClassVar[ResultSectionType]

class ResultSectionShowResultsInDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_PLUS_Z: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_X: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_Y: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_Z: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_X: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_Y: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_Z: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_MINUS_Z: _ClassVar[ResultSectionShowResultsInDirection]
    RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_PLUS_Y: _ClassVar[ResultSectionShowResultsInDirection]

class ResultSectionProjectionInDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_X: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_Y: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_Z: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_U: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_V: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_W: _ClassVar[ResultSectionProjectionInDirection]
    RESULT_SECTION_PROJECTION_IN_DIRECTION_VECTOR: _ClassVar[ResultSectionProjectionInDirection]
RESULT_SECTION_TYPE_UNKNOWN: ResultSectionType
RESULT_SECTION_TYPE_2_POINTS_AND_VECTOR: ResultSectionType
RESULT_SECTION_TYPE_LINE: ResultSectionType
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_PLUS_Z: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_X: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_Y: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_MINUS_Z: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_X: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_Y: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_GLOBAL_PLUS_Z: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_MINUS_Z: ResultSectionShowResultsInDirection
RESULT_SECTION_SHOW_RESULTS_IN_DIRECTION_LOCAL_PLUS_Y: ResultSectionShowResultsInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_X: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_Y: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_GLOBAL_Z: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_U: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_V: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_USER_DEFINED_W: ResultSectionProjectionInDirection
RESULT_SECTION_PROJECTION_IN_DIRECTION_VECTOR: ResultSectionProjectionInDirection

class ResultSection(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "assigned_to_all_surfaces", "assigned_to_surfaces", "assigned_to_all_solids", "assigned_to_solids", "show_results_in_direction", "coordinate_system", "show_values_on_isolines_enabled", "lines", "first_point", "first_point_coordinate_1", "first_point_coordinate_2", "first_point_coordinate_3", "second_point", "second_point_coordinate_1", "second_point_coordinate_2", "second_point_coordinate_3", "projection_in_direction", "vector", "vector_coordinate_1", "vector_coordinate_2", "vector_coordinate_3", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    SHOW_RESULTS_IN_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    SHOW_VALUES_ON_ISOLINES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    FIRST_POINT_FIELD_NUMBER: _ClassVar[int]
    FIRST_POINT_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    FIRST_POINT_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    FIRST_POINT_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    SECOND_POINT_FIELD_NUMBER: _ClassVar[int]
    SECOND_POINT_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    SECOND_POINT_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    SECOND_POINT_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    PROJECTION_IN_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: ResultSectionType
    user_defined_name_enabled: bool
    name: str
    assigned_to_all_surfaces: bool
    assigned_to_surfaces: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_solids: bool
    assigned_to_solids: _containers.RepeatedScalarFieldContainer[int]
    show_results_in_direction: ResultSectionShowResultsInDirection
    coordinate_system: int
    show_values_on_isolines_enabled: bool
    lines: _containers.RepeatedScalarFieldContainer[int]
    first_point: _common_pb2.Vector3d
    first_point_coordinate_1: float
    first_point_coordinate_2: float
    first_point_coordinate_3: float
    second_point: _common_pb2.Vector3d
    second_point_coordinate_1: float
    second_point_coordinate_2: float
    second_point_coordinate_3: float
    projection_in_direction: ResultSectionProjectionInDirection
    vector: _common_pb2.Vector3d
    vector_coordinate_1: float
    vector_coordinate_2: float
    vector_coordinate_3: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[ResultSectionType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_surfaces: bool = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., assigned_to_all_solids: bool = ..., assigned_to_solids: _Optional[_Iterable[int]] = ..., show_results_in_direction: _Optional[_Union[ResultSectionShowResultsInDirection, str]] = ..., coordinate_system: _Optional[int] = ..., show_values_on_isolines_enabled: bool = ..., lines: _Optional[_Iterable[int]] = ..., first_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., first_point_coordinate_1: _Optional[float] = ..., first_point_coordinate_2: _Optional[float] = ..., first_point_coordinate_3: _Optional[float] = ..., second_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., second_point_coordinate_1: _Optional[float] = ..., second_point_coordinate_2: _Optional[float] = ..., second_point_coordinate_3: _Optional[float] = ..., projection_in_direction: _Optional[_Union[ResultSectionProjectionInDirection, str]] = ..., vector: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., vector_coordinate_1: _Optional[float] = ..., vector_coordinate_2: _Optional[float] = ..., vector_coordinate_3: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
