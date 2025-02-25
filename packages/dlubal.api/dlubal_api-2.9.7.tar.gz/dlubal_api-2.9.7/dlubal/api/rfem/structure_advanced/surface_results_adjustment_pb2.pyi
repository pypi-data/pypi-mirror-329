from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceResultsAdjustmentShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULTS_ADJUSTMENT_SHAPE_RECTANGLE: _ClassVar[SurfaceResultsAdjustmentShape]
    SURFACE_RESULTS_ADJUSTMENT_SHAPE_CIRCLE: _ClassVar[SurfaceResultsAdjustmentShape]
    SURFACE_RESULTS_ADJUSTMENT_SHAPE_ELLIPSE: _ClassVar[SurfaceResultsAdjustmentShape]
    SURFACE_RESULTS_ADJUSTMENT_SHAPE_POLYGON: _ClassVar[SurfaceResultsAdjustmentShape]

class SurfaceResultsAdjustmentAdjustmentTypeInDirectionU(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_AVERAGING_OF_MY_MXY_VY_NY_NXY: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_AVERAGING_OF_MX_MXY_VX_NX_NXY: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_CONTACT_STRESS_AREA: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_NONE: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_USER_DEFINED: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_ZERO: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU]

class SurfaceResultsAdjustmentAdjustmentTypeInDirectionV(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_AVERAGING_OF_MY_MXY_VY_NY_NXY: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_AVERAGING_OF_MX_MXY_VX_NX_NXY: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_CONTACT_STRESS_AREA: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_NONE: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_USER_DEFINED: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]
    SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_ZERO: _ClassVar[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV]

class SurfaceResultsAdjustmentResultsToAdjustContactStressAreaContactStressType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULTS_ADJUSTMENT_RESULTS_TO_ADJUST_CONTACT_STRESS_AREA_CONTACT_STRESS_TYPE_UNKNOWN: _ClassVar[SurfaceResultsAdjustmentResultsToAdjustContactStressAreaContactStressType]

class SurfaceResultsAdjustmentProjectionInDirectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_PERPENDICULAR: _ClassVar[SurfaceResultsAdjustmentProjectionInDirectionType]
    SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_X: _ClassVar[SurfaceResultsAdjustmentProjectionInDirectionType]
    SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_Y: _ClassVar[SurfaceResultsAdjustmentProjectionInDirectionType]
    SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_Z: _ClassVar[SurfaceResultsAdjustmentProjectionInDirectionType]
    SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_VECTOR: _ClassVar[SurfaceResultsAdjustmentProjectionInDirectionType]
SURFACE_RESULTS_ADJUSTMENT_SHAPE_RECTANGLE: SurfaceResultsAdjustmentShape
SURFACE_RESULTS_ADJUSTMENT_SHAPE_CIRCLE: SurfaceResultsAdjustmentShape
SURFACE_RESULTS_ADJUSTMENT_SHAPE_ELLIPSE: SurfaceResultsAdjustmentShape
SURFACE_RESULTS_ADJUSTMENT_SHAPE_POLYGON: SurfaceResultsAdjustmentShape
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_AVERAGING_OF_MY_MXY_VY_NY_NXY: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_AVERAGING_OF_MX_MXY_VX_NX_NXY: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_CONTACT_STRESS_AREA: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_NONE: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_USER_DEFINED: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_U_ZERO: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_AVERAGING_OF_MY_MXY_VY_NY_NXY: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_AVERAGING_OF_MX_MXY_VX_NX_NXY: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_CONTACT_STRESS_AREA: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_NONE: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_USER_DEFINED: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_ADJUSTMENT_TYPE_IN_DIRECTION_V_ZERO: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
SURFACE_RESULTS_ADJUSTMENT_RESULTS_TO_ADJUST_CONTACT_STRESS_AREA_CONTACT_STRESS_TYPE_UNKNOWN: SurfaceResultsAdjustmentResultsToAdjustContactStressAreaContactStressType
SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_PERPENDICULAR: SurfaceResultsAdjustmentProjectionInDirectionType
SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_X: SurfaceResultsAdjustmentProjectionInDirectionType
SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_Y: SurfaceResultsAdjustmentProjectionInDirectionType
SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_GLOBAL_IN_Z: SurfaceResultsAdjustmentProjectionInDirectionType
SURFACE_RESULTS_ADJUSTMENT_PROJECTION_IN_DIRECTION_TYPE_VECTOR: SurfaceResultsAdjustmentProjectionInDirectionType

class SurfaceResultsAdjustment(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "surfaces", "shape", "dimension_1", "dimension_2", "angular_rotation", "center_position", "center_position_x", "center_position_y", "center_position_z", "polygon_points", "adjustment_type_in_direction_u", "adjustment_type_in_direction_v", "results_to_adjust_contact_stress_area", "projection_in_direction_type", "vector_of_projection_in_direction_coordinates", "vector_of_projection_in_direction_coordinates_x", "vector_of_projection_in_direction_coordinates_y", "vector_of_projection_in_direction_coordinates_z", "comment", "results_to_adjust_in_direction_u", "results_to_adjust_in_direction_v", "results_to_adjust_zero", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_1_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_2_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ROTATION_FIELD_NUMBER: _ClassVar[int]
    CENTER_POSITION_FIELD_NUMBER: _ClassVar[int]
    CENTER_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    CENTER_POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    POLYGON_POINTS_FIELD_NUMBER: _ClassVar[int]
    ADJUSTMENT_TYPE_IN_DIRECTION_U_FIELD_NUMBER: _ClassVar[int]
    ADJUSTMENT_TYPE_IN_DIRECTION_V_FIELD_NUMBER: _ClassVar[int]
    RESULTS_TO_ADJUST_CONTACT_STRESS_AREA_FIELD_NUMBER: _ClassVar[int]
    PROJECTION_IN_DIRECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_OF_PROJECTION_IN_DIRECTION_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    VECTOR_OF_PROJECTION_IN_DIRECTION_COORDINATES_X_FIELD_NUMBER: _ClassVar[int]
    VECTOR_OF_PROJECTION_IN_DIRECTION_COORDINATES_Y_FIELD_NUMBER: _ClassVar[int]
    VECTOR_OF_PROJECTION_IN_DIRECTION_COORDINATES_Z_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    RESULTS_TO_ADJUST_IN_DIRECTION_U_FIELD_NUMBER: _ClassVar[int]
    RESULTS_TO_ADJUST_IN_DIRECTION_V_FIELD_NUMBER: _ClassVar[int]
    RESULTS_TO_ADJUST_ZERO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    shape: SurfaceResultsAdjustmentShape
    dimension_1: float
    dimension_2: float
    angular_rotation: float
    center_position: _common_pb2.Vector3d
    center_position_x: float
    center_position_y: float
    center_position_z: float
    polygon_points: SurfaceResultsAdjustmentPolygonPointsTable
    adjustment_type_in_direction_u: SurfaceResultsAdjustmentAdjustmentTypeInDirectionU
    adjustment_type_in_direction_v: SurfaceResultsAdjustmentAdjustmentTypeInDirectionV
    results_to_adjust_contact_stress_area: SurfaceResultsAdjustmentResultsToAdjustContactStressAreaTable
    projection_in_direction_type: SurfaceResultsAdjustmentProjectionInDirectionType
    vector_of_projection_in_direction_coordinates: _common_pb2.Vector3d
    vector_of_projection_in_direction_coordinates_x: float
    vector_of_projection_in_direction_coordinates_y: float
    vector_of_projection_in_direction_coordinates_z: float
    comment: str
    results_to_adjust_in_direction_u: SurfaceResultsAdjustmentResultsToAdjustInDirectionUAndChildItemsTable
    results_to_adjust_in_direction_v: SurfaceResultsAdjustmentResultsToAdjustInDirectionVAndChildItemsTable
    results_to_adjust_zero: SurfaceResultsAdjustmentResultsToAdjustZeroAndChildItemsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., surfaces: _Optional[_Iterable[int]] = ..., shape: _Optional[_Union[SurfaceResultsAdjustmentShape, str]] = ..., dimension_1: _Optional[float] = ..., dimension_2: _Optional[float] = ..., angular_rotation: _Optional[float] = ..., center_position: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., center_position_x: _Optional[float] = ..., center_position_y: _Optional[float] = ..., center_position_z: _Optional[float] = ..., polygon_points: _Optional[_Union[SurfaceResultsAdjustmentPolygonPointsTable, _Mapping]] = ..., adjustment_type_in_direction_u: _Optional[_Union[SurfaceResultsAdjustmentAdjustmentTypeInDirectionU, str]] = ..., adjustment_type_in_direction_v: _Optional[_Union[SurfaceResultsAdjustmentAdjustmentTypeInDirectionV, str]] = ..., results_to_adjust_contact_stress_area: _Optional[_Union[SurfaceResultsAdjustmentResultsToAdjustContactStressAreaTable, _Mapping]] = ..., projection_in_direction_type: _Optional[_Union[SurfaceResultsAdjustmentProjectionInDirectionType, str]] = ..., vector_of_projection_in_direction_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., vector_of_projection_in_direction_coordinates_x: _Optional[float] = ..., vector_of_projection_in_direction_coordinates_y: _Optional[float] = ..., vector_of_projection_in_direction_coordinates_z: _Optional[float] = ..., comment: _Optional[str] = ..., results_to_adjust_in_direction_u: _Optional[_Union[SurfaceResultsAdjustmentResultsToAdjustInDirectionUAndChildItemsTable, _Mapping]] = ..., results_to_adjust_in_direction_v: _Optional[_Union[SurfaceResultsAdjustmentResultsToAdjustInDirectionVAndChildItemsTable, _Mapping]] = ..., results_to_adjust_zero: _Optional[_Union[SurfaceResultsAdjustmentResultsToAdjustZeroAndChildItemsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class SurfaceResultsAdjustmentPolygonPointsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceResultsAdjustmentPolygonPointsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceResultsAdjustmentPolygonPointsRow, _Mapping]]] = ...) -> None: ...

class SurfaceResultsAdjustmentPolygonPointsRow(_message.Message):
    __slots__ = ("no", "description", "x", "y", "z")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    x: float
    y: float
    z: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class SurfaceResultsAdjustmentResultsToAdjustContactStressAreaTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceResultsAdjustmentResultsToAdjustContactStressAreaRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceResultsAdjustmentResultsToAdjustContactStressAreaRow, _Mapping]]] = ...) -> None: ...

class SurfaceResultsAdjustmentResultsToAdjustContactStressAreaRow(_message.Message):
    __slots__ = ("no", "description", "contact_stress_type", "lower_limit", "upper_limit")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTACT_STRESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOWER_LIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPER_LIMIT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    contact_stress_type: SurfaceResultsAdjustmentResultsToAdjustContactStressAreaContactStressType
    lower_limit: float
    upper_limit: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., contact_stress_type: _Optional[_Union[SurfaceResultsAdjustmentResultsToAdjustContactStressAreaContactStressType, str]] = ..., lower_limit: _Optional[float] = ..., upper_limit: _Optional[float] = ...) -> None: ...

class SurfaceResultsAdjustmentResultsToAdjustInDirectionUAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SurfaceResultsAdjustmentResultsToAdjustInDirectionVAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SurfaceResultsAdjustmentResultsToAdjustZeroAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
