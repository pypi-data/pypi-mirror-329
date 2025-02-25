from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreeRectangularLoadLoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreeRectangularLoadLoadProjection]
    FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreeRectangularLoadLoadProjection]
    FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreeRectangularLoadLoadProjection]

class FreeRectangularLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: _ClassVar[FreeRectangularLoadLoadDirection]
    FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: _ClassVar[FreeRectangularLoadLoadDirection]

class FreeRectangularLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[FreeRectangularLoadLoadDistribution]
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_LINEAR_FIRST: _ClassVar[FreeRectangularLoadLoadDistribution]
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_LINEAR_SECOND: _ClassVar[FreeRectangularLoadLoadDistribution]
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER: _ClassVar[FreeRectangularLoadLoadDistribution]
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: _ClassVar[FreeRectangularLoadLoadDistribution]
    FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER: _ClassVar[FreeRectangularLoadLoadDistribution]

class FreeRectangularLoadLoadLocationRectangle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE_RECTANGULAR_LOAD_LOAD_LOCATION_RECTANGLE_CORNER_POINTS: _ClassVar[FreeRectangularLoadLoadLocationRectangle]
    FREE_RECTANGULAR_LOAD_LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES: _ClassVar[FreeRectangularLoadLoadLocationRectangle]
FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_XY_OR_UV: FreeRectangularLoadLoadProjection
FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_XZ_OR_UW: FreeRectangularLoadLoadProjection
FREE_RECTANGULAR_LOAD_LOAD_PROJECTION_YZ_OR_VW: FreeRectangularLoadLoadProjection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_X: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_X_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_X_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Y_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Y_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Z_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_GLOBAL_Z_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_Y: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_LOCAL_Z: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_U_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_U_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_V_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_V_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_W_PROJECTED: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DIRECTION_USER_DEFINED_W_TRUE: FreeRectangularLoadLoadDirection
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_UNIFORM: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_LINEAR_FIRST: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_LINEAR_SECOND: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER: FreeRectangularLoadLoadDistribution
FREE_RECTANGULAR_LOAD_LOAD_LOCATION_RECTANGLE_CORNER_POINTS: FreeRectangularLoadLoadLocationRectangle
FREE_RECTANGULAR_LOAD_LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES: FreeRectangularLoadLoadLocationRectangle

class FreeRectangularLoad(_message.Message):
    __slots__ = ("no", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "load_distribution", "magnitude_uniform", "magnitude_linear_first", "magnitude_linear_second", "load_location_first_x", "load_location_first_y", "load_location_second_x", "load_location_second_y", "load_location_rectangle", "load_location_center_x", "load_location_center_y", "load_location_center_side_a", "load_location_center_side_b", "load_location_rotation", "load_varying_in_z_parameters", "load_varying_along_perimeter_parameters", "load_varying_in_z_parameters_sorted", "load_varying_along_perimeter_parameters_sorted", "load_varying_along_perimeter_z_index", "axis_definition_p1", "axis_definition_p1_x", "axis_definition_p1_y", "axis_definition_p1_z", "axis_definition_p2", "axis_definition_p2_x", "axis_definition_p2_y", "axis_definition_p2_z", "axis_start_angle", "comment", "generating_object_info", "is_generated", "id_for_export_import", "metadata_for_export_import")
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
    MAGNITUDE_LINEAR_FIRST_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_LINEAR_SECOND_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_Y_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_Y_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_CENTER_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_CENTER_SIDE_A_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_CENTER_SIDE_B_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_ROTATION_FIELD_NUMBER: _ClassVar[int]
    LOAD_VARYING_IN_Z_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LOAD_VARYING_ALONG_PERIMETER_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LOAD_VARYING_IN_Z_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    LOAD_VARYING_ALONG_PERIMETER_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    LOAD_VARYING_ALONG_PERIMETER_Z_INDEX_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreeRectangularLoadLoadProjection
    load_direction: FreeRectangularLoadLoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    load_distribution: FreeRectangularLoadLoadDistribution
    magnitude_uniform: float
    magnitude_linear_first: float
    magnitude_linear_second: float
    load_location_first_x: float
    load_location_first_y: float
    load_location_second_x: float
    load_location_second_y: float
    load_location_rectangle: FreeRectangularLoadLoadLocationRectangle
    load_location_center_x: float
    load_location_center_y: float
    load_location_center_side_a: float
    load_location_center_side_b: float
    load_location_rotation: float
    load_varying_in_z_parameters: FreeRectangularLoadLoadVaryingInZParametersTable
    load_varying_along_perimeter_parameters: FreeRectangularLoadLoadVaryingAlongPerimeterParametersTable
    load_varying_in_z_parameters_sorted: bool
    load_varying_along_perimeter_parameters_sorted: bool
    load_varying_along_perimeter_z_index: int
    axis_definition_p1: _common_pb2.Vector3d
    axis_definition_p1_x: float
    axis_definition_p1_y: float
    axis_definition_p1_z: float
    axis_definition_p2: _common_pb2.Vector3d
    axis_definition_p2_x: float
    axis_definition_p2_y: float
    axis_definition_p2_z: float
    axis_start_angle: float
    comment: str
    generating_object_info: str
    is_generated: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreeRectangularLoadLoadProjection, str]] = ..., load_direction: _Optional[_Union[FreeRectangularLoadLoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., load_distribution: _Optional[_Union[FreeRectangularLoadLoadDistribution, str]] = ..., magnitude_uniform: _Optional[float] = ..., magnitude_linear_first: _Optional[float] = ..., magnitude_linear_second: _Optional[float] = ..., load_location_first_x: _Optional[float] = ..., load_location_first_y: _Optional[float] = ..., load_location_second_x: _Optional[float] = ..., load_location_second_y: _Optional[float] = ..., load_location_rectangle: _Optional[_Union[FreeRectangularLoadLoadLocationRectangle, str]] = ..., load_location_center_x: _Optional[float] = ..., load_location_center_y: _Optional[float] = ..., load_location_center_side_a: _Optional[float] = ..., load_location_center_side_b: _Optional[float] = ..., load_location_rotation: _Optional[float] = ..., load_varying_in_z_parameters: _Optional[_Union[FreeRectangularLoadLoadVaryingInZParametersTable, _Mapping]] = ..., load_varying_along_perimeter_parameters: _Optional[_Union[FreeRectangularLoadLoadVaryingAlongPerimeterParametersTable, _Mapping]] = ..., load_varying_in_z_parameters_sorted: bool = ..., load_varying_along_perimeter_parameters_sorted: bool = ..., load_varying_along_perimeter_z_index: _Optional[int] = ..., axis_definition_p1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p1_x: _Optional[float] = ..., axis_definition_p1_y: _Optional[float] = ..., axis_definition_p1_z: _Optional[float] = ..., axis_definition_p2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p2_x: _Optional[float] = ..., axis_definition_p2_y: _Optional[float] = ..., axis_definition_p2_z: _Optional[float] = ..., axis_start_angle: _Optional[float] = ..., comment: _Optional[str] = ..., generating_object_info: _Optional[str] = ..., is_generated: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class FreeRectangularLoadLoadVaryingInZParametersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[FreeRectangularLoadLoadVaryingInZParametersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[FreeRectangularLoadLoadVaryingInZParametersRow, _Mapping]]] = ...) -> None: ...

class FreeRectangularLoadLoadVaryingInZParametersRow(_message.Message):
    __slots__ = ("no", "description", "distance", "recalculated_magnitude", "factor", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    RECALCULATED_MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    distance: float
    recalculated_magnitude: float
    factor: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., recalculated_magnitude: _Optional[float] = ..., factor: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...

class FreeRectangularLoadLoadVaryingAlongPerimeterParametersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[FreeRectangularLoadLoadVaryingAlongPerimeterParametersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[FreeRectangularLoadLoadVaryingAlongPerimeterParametersRow, _Mapping]]] = ...) -> None: ...

class FreeRectangularLoadLoadVaryingAlongPerimeterParametersRow(_message.Message):
    __slots__ = ("no", "description", "alpha", "recalculated_magnitude", "factor", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    RECALCULATED_MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    alpha: float
    recalculated_magnitude: float
    factor: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., alpha: _Optional[float] = ..., recalculated_magnitude: _Optional[float] = ..., factor: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
