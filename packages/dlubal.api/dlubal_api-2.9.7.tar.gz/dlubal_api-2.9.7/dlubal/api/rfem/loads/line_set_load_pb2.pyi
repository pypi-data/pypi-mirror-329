from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LineSetLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINE_SET_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[LineSetLoadLoadType]
    LINE_SET_LOAD_LOAD_TYPE_E_TYPE_MASS: _ClassVar[LineSetLoadLoadType]
    LINE_SET_LOAD_LOAD_TYPE_LOAD_TYPE_FORCE: _ClassVar[LineSetLoadLoadType]
    LINE_SET_LOAD_LOAD_TYPE_LOAD_TYPE_MOMENT: _ClassVar[LineSetLoadLoadType]

class LineSetLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_1: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2_2: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_N: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_VARYING: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_PARABOLIC: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_TAPERED: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_TRAPEZOIDAL: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM_TOTAL: _ClassVar[LineSetLoadLoadDistribution]
    LINE_SET_LOAD_LOAD_DISTRIBUTION_VARYING: _ClassVar[LineSetLoadLoadDistribution]

class LineSetLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[LineSetLoadLoadDirection]
    LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[LineSetLoadLoadDirection]

class LineSetLoadLoadDirectionOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINE_SET_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: _ClassVar[LineSetLoadLoadDirectionOrientation]
    LINE_SET_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: _ClassVar[LineSetLoadLoadDirectionOrientation]
LINE_SET_LOAD_LOAD_TYPE_UNKNOWN: LineSetLoadLoadType
LINE_SET_LOAD_LOAD_TYPE_E_TYPE_MASS: LineSetLoadLoadType
LINE_SET_LOAD_LOAD_TYPE_LOAD_TYPE_FORCE: LineSetLoadLoadType
LINE_SET_LOAD_LOAD_TYPE_LOAD_TYPE_MOMENT: LineSetLoadLoadType
LINE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_1: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2_2: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_N: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_VARYING: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_PARABOLIC: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_TAPERED: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_TRAPEZOIDAL: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM_TOTAL: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DISTRIBUTION_VARYING: LineSetLoadLoadDistribution
LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_X: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_Y: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_LOCAL_Z: LineSetLoadLoadDirection
LINE_SET_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: LineSetLoadLoadDirectionOrientation
LINE_SET_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: LineSetLoadLoadDirectionOrientation

class LineSetLoad(_message.Message):
    __slots__ = ("no", "load_type", "line_sets", "load_case", "coordinate_system", "load_distribution", "load_direction", "load_direction_orientation", "magnitude", "magnitude_1", "magnitude_2", "magnitude_3", "mass_global", "mass_x", "mass_y", "mass_z", "count_n", "varying_load_parameters_are_defined_as_relative", "varying_load_parameters", "varying_load_parameters_sorted", "distance_a_is_defined_as_relative", "distance_a_absolute", "distance_a_relative", "distance_b_is_defined_as_relative", "distance_b_absolute", "distance_b_relative", "distance_c_is_defined_as_relative", "distance_c_absolute", "distance_c_relative", "reference_to_list_of_line_sets", "distance_from_line_set_end", "load_is_over_total_length", "individual_mass_components", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINE_SETS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_3_FIELD_NUMBER: _ClassVar[int]
    MASS_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    MASS_X_FIELD_NUMBER: _ClassVar[int]
    MASS_Y_FIELD_NUMBER: _ClassVar[int]
    MASS_Z_FIELD_NUMBER: _ClassVar[int]
    COUNT_N_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_ARE_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TO_LIST_OF_LINE_SETS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FROM_LINE_SET_END_FIELD_NUMBER: _ClassVar[int]
    LOAD_IS_OVER_TOTAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_MASS_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: LineSetLoadLoadType
    line_sets: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: str
    load_distribution: LineSetLoadLoadDistribution
    load_direction: LineSetLoadLoadDirection
    load_direction_orientation: LineSetLoadLoadDirectionOrientation
    magnitude: float
    magnitude_1: float
    magnitude_2: float
    magnitude_3: float
    mass_global: float
    mass_x: float
    mass_y: float
    mass_z: float
    count_n: int
    varying_load_parameters_are_defined_as_relative: bool
    varying_load_parameters: LineSetLoadVaryingLoadParametersTable
    varying_load_parameters_sorted: bool
    distance_a_is_defined_as_relative: bool
    distance_a_absolute: float
    distance_a_relative: float
    distance_b_is_defined_as_relative: bool
    distance_b_absolute: float
    distance_b_relative: float
    distance_c_is_defined_as_relative: bool
    distance_c_absolute: float
    distance_c_relative: float
    reference_to_list_of_line_sets: bool
    distance_from_line_set_end: bool
    load_is_over_total_length: bool
    individual_mass_components: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[LineSetLoadLoadType, str]] = ..., line_sets: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[str] = ..., load_distribution: _Optional[_Union[LineSetLoadLoadDistribution, str]] = ..., load_direction: _Optional[_Union[LineSetLoadLoadDirection, str]] = ..., load_direction_orientation: _Optional[_Union[LineSetLoadLoadDirectionOrientation, str]] = ..., magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., magnitude_3: _Optional[float] = ..., mass_global: _Optional[float] = ..., mass_x: _Optional[float] = ..., mass_y: _Optional[float] = ..., mass_z: _Optional[float] = ..., count_n: _Optional[int] = ..., varying_load_parameters_are_defined_as_relative: bool = ..., varying_load_parameters: _Optional[_Union[LineSetLoadVaryingLoadParametersTable, _Mapping]] = ..., varying_load_parameters_sorted: bool = ..., distance_a_is_defined_as_relative: bool = ..., distance_a_absolute: _Optional[float] = ..., distance_a_relative: _Optional[float] = ..., distance_b_is_defined_as_relative: bool = ..., distance_b_absolute: _Optional[float] = ..., distance_b_relative: _Optional[float] = ..., distance_c_is_defined_as_relative: bool = ..., distance_c_absolute: _Optional[float] = ..., distance_c_relative: _Optional[float] = ..., reference_to_list_of_line_sets: bool = ..., distance_from_line_set_end: bool = ..., load_is_over_total_length: bool = ..., individual_mass_components: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class LineSetLoadVaryingLoadParametersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[LineSetLoadVaryingLoadParametersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[LineSetLoadVaryingLoadParametersRow, _Mapping]]] = ...) -> None: ...

class LineSetLoadVaryingLoadParametersRow(_message.Message):
    __slots__ = ("no", "description", "distance", "delta_distance", "magnitude", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DELTA_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    distance: float
    delta_distance: float
    magnitude: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., delta_distance: _Optional[float] = ..., magnitude: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
