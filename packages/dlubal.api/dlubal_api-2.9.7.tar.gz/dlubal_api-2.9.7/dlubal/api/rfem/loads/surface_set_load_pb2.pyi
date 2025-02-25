from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceSetLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_AXIAL_STRAIN: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_FORCE: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_FORM_FINDING: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_MASS: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_PONDING: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_PRECAMBER: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_ROTARY_MOTION: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_SNOW: _ClassVar[SurfaceSetLoadLoadType]
    SURFACE_SET_LOAD_LOAD_TYPE_TEMPERATURE: _ClassVar[SurfaceSetLoadLoadType]

class SurfaceSetLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_X: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Y: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Z: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_RADIAL: _ClassVar[SurfaceSetLoadLoadDistribution]
    SURFACE_SET_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: _ClassVar[SurfaceSetLoadLoadDistribution]

class SurfaceSetLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[SurfaceSetLoadLoadDirection]
    SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[SurfaceSetLoadLoadDirection]

class SurfaceSetLoadAxisDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: _ClassVar[SurfaceSetLoadAxisDefinitionType]
    SURFACE_SET_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: _ClassVar[SurfaceSetLoadAxisDefinitionType]

class SurfaceSetLoadAxisDefinitionAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_X: _ClassVar[SurfaceSetLoadAxisDefinitionAxis]
    SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_Y: _ClassVar[SurfaceSetLoadAxisDefinitionAxis]
    SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_Z: _ClassVar[SurfaceSetLoadAxisDefinitionAxis]

class SurfaceSetLoadAxisDefinitionAxisOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: _ClassVar[SurfaceSetLoadAxisDefinitionAxisOrientation]
    SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: _ClassVar[SurfaceSetLoadAxisDefinitionAxisOrientation]

class SurfaceSetLoadFormFindingDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_FORCE: _ClassVar[SurfaceSetLoadFormFindingDefinition]
    SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_SAG: _ClassVar[SurfaceSetLoadFormFindingDefinition]
    SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_STRESS: _ClassVar[SurfaceSetLoadFormFindingDefinition]

class SurfaceSetLoadFormFindingCalculationMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_FORM_FINDING_CALCULATION_METHOD_STANDARD: _ClassVar[SurfaceSetLoadFormFindingCalculationMethod]
    SURFACE_SET_LOAD_FORM_FINDING_CALCULATION_METHOD_PROJECTION: _ClassVar[SurfaceSetLoadFormFindingCalculationMethod]

class SurfaceSetLoadFormFindingSagRelatedToObject(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_BASE: _ClassVar[SurfaceSetLoadFormFindingSagRelatedToObject]
    SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_CS: _ClassVar[SurfaceSetLoadFormFindingSagRelatedToObject]
    SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_SURFACE: _ClassVar[SurfaceSetLoadFormFindingSagRelatedToObject]
SURFACE_SET_LOAD_LOAD_TYPE_UNKNOWN: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_AXIAL_STRAIN: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_FORCE: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_FORM_FINDING: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_MASS: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_PONDING: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_PRECAMBER: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_ROTARY_MOTION: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_SNOW: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_TYPE_TEMPERATURE: SurfaceSetLoadLoadType
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_UNIFORM: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_X: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Y: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Z: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_RADIAL: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: SurfaceSetLoadLoadDistribution
SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_X: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_Y: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_LOAD_DIRECTION_LOCAL_Z: SurfaceSetLoadLoadDirection
SURFACE_SET_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: SurfaceSetLoadAxisDefinitionType
SURFACE_SET_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: SurfaceSetLoadAxisDefinitionType
SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_X: SurfaceSetLoadAxisDefinitionAxis
SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_Y: SurfaceSetLoadAxisDefinitionAxis
SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_Z: SurfaceSetLoadAxisDefinitionAxis
SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: SurfaceSetLoadAxisDefinitionAxisOrientation
SURFACE_SET_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: SurfaceSetLoadAxisDefinitionAxisOrientation
SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_FORCE: SurfaceSetLoadFormFindingDefinition
SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_SAG: SurfaceSetLoadFormFindingDefinition
SURFACE_SET_LOAD_FORM_FINDING_DEFINITION_STRESS: SurfaceSetLoadFormFindingDefinition
SURFACE_SET_LOAD_FORM_FINDING_CALCULATION_METHOD_STANDARD: SurfaceSetLoadFormFindingCalculationMethod
SURFACE_SET_LOAD_FORM_FINDING_CALCULATION_METHOD_PROJECTION: SurfaceSetLoadFormFindingCalculationMethod
SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_BASE: SurfaceSetLoadFormFindingSagRelatedToObject
SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_CS: SurfaceSetLoadFormFindingSagRelatedToObject
SURFACE_SET_LOAD_FORM_FINDING_SAG_RELATED_TO_OBJECT_SURFACE: SurfaceSetLoadFormFindingSagRelatedToObject

class SurfaceSetLoad(_message.Message):
    __slots__ = ("no", "load_type", "surface_sets", "load_case", "coordinate_system", "load_distribution", "load_direction", "individual_mass_components", "uniform_magnitude", "magnitude_1", "magnitude_2", "magnitude_3", "uniform_magnitude_t_c", "magnitude_t_c_1", "magnitude_t_c_2", "magnitude_t_c_3", "uniform_magnitude_delta_t", "magnitude_delta_t_1", "magnitude_delta_t_2", "magnitude_delta_t_3", "magnitude_axial_strain_x", "magnitude_axial_strain_y", "magnitude_axial_strain_1x", "magnitude_axial_strain_1y", "magnitude_axial_strain_2x", "magnitude_axial_strain_2y", "magnitude_axial_strain_3x", "magnitude_axial_strain_3y", "angular_velocity", "angular_acceleration", "node_1", "node_2", "node_3", "axis_definition_type", "axis_definition_p1", "axis_definition_p1_x", "axis_definition_p1_y", "axis_definition_p1_z", "axis_definition_p2", "axis_definition_p2_x", "axis_definition_p2_y", "axis_definition_p2_z", "axis_definition_axis", "axis_definition_axis_orientation", "varying_load_parameters", "varying_load_parameters_sorted", "form_finding_definition", "magnitude_force_u", "magnitude_force_v", "magnitude_force_r", "magnitude_force_t", "magnitude_mass_x", "magnitude_mass_y", "magnitude_mass_z", "magnitude_stress_u", "magnitude_stress_v", "magnitude_stress_r", "magnitude_stress_t", "magnitude_sag", "magnitude_force_scale_x", "magnitude_force_scale_y", "form_finding_calculation_method", "form_finding_sag_related_to_object", "form_finding_sag_related_to_surface", "magnitude_mass_global", "ponding_magnitude_specific_weight", "ponding_magnitude_amount_precipitation", "ponding_amount_precipitation", "comment", "is_generated", "generating_object_info", "magnitude_orthogonal_force_x", "magnitude_orthogonal_force_y", "magnitude_orthogonal_stress_x", "magnitude_orthogonal_stress_y", "magnitude_uniform_force_x", "magnitude_uniform_force_y", "magnitude_uniform_stress_x", "magnitude_uniform_stress_y", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_SETS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_MASS_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_3_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_MAGNITUDE_T_C_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_3_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_MAGNITUDE_DELTA_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_1X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_1Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_2X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_2Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_3X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_AXIAL_STRAIN_3Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    NODE_1_FIELD_NUMBER: _ClassVar[int]
    NODE_2_FIELD_NUMBER: _ClassVar[int]
    NODE_3_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_U_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_V_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_R_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_MASS_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_MASS_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_MASS_Z_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_STRESS_U_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_STRESS_V_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_STRESS_R_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_STRESS_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_SAG_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_SCALE_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FORCE_SCALE_Y_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_CALCULATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_SAG_RELATED_TO_OBJECT_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_SAG_RELATED_TO_SURFACE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_MASS_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    PONDING_MAGNITUDE_SPECIFIC_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    PONDING_MAGNITUDE_AMOUNT_PRECIPITATION_FIELD_NUMBER: _ClassVar[int]
    PONDING_AMOUNT_PRECIPITATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_ORTHOGONAL_FORCE_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_ORTHOGONAL_FORCE_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_ORTHOGONAL_STRESS_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_ORTHOGONAL_STRESS_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_FORCE_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_FORCE_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_STRESS_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_STRESS_Y_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: SurfaceSetLoadLoadType
    surface_sets: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: str
    load_distribution: SurfaceSetLoadLoadDistribution
    load_direction: SurfaceSetLoadLoadDirection
    individual_mass_components: bool
    uniform_magnitude: float
    magnitude_1: float
    magnitude_2: float
    magnitude_3: float
    uniform_magnitude_t_c: float
    magnitude_t_c_1: float
    magnitude_t_c_2: float
    magnitude_t_c_3: float
    uniform_magnitude_delta_t: float
    magnitude_delta_t_1: float
    magnitude_delta_t_2: float
    magnitude_delta_t_3: float
    magnitude_axial_strain_x: float
    magnitude_axial_strain_y: float
    magnitude_axial_strain_1x: float
    magnitude_axial_strain_1y: float
    magnitude_axial_strain_2x: float
    magnitude_axial_strain_2y: float
    magnitude_axial_strain_3x: float
    magnitude_axial_strain_3y: float
    angular_velocity: float
    angular_acceleration: float
    node_1: int
    node_2: int
    node_3: int
    axis_definition_type: SurfaceSetLoadAxisDefinitionType
    axis_definition_p1: _common_pb2.Vector3d
    axis_definition_p1_x: float
    axis_definition_p1_y: float
    axis_definition_p1_z: float
    axis_definition_p2: _common_pb2.Vector3d
    axis_definition_p2_x: float
    axis_definition_p2_y: float
    axis_definition_p2_z: float
    axis_definition_axis: SurfaceSetLoadAxisDefinitionAxis
    axis_definition_axis_orientation: SurfaceSetLoadAxisDefinitionAxisOrientation
    varying_load_parameters: SurfaceSetLoadVaryingLoadParametersTable
    varying_load_parameters_sorted: bool
    form_finding_definition: SurfaceSetLoadFormFindingDefinition
    magnitude_force_u: float
    magnitude_force_v: float
    magnitude_force_r: float
    magnitude_force_t: float
    magnitude_mass_x: float
    magnitude_mass_y: float
    magnitude_mass_z: float
    magnitude_stress_u: float
    magnitude_stress_v: float
    magnitude_stress_r: float
    magnitude_stress_t: float
    magnitude_sag: float
    magnitude_force_scale_x: float
    magnitude_force_scale_y: float
    form_finding_calculation_method: SurfaceSetLoadFormFindingCalculationMethod
    form_finding_sag_related_to_object: SurfaceSetLoadFormFindingSagRelatedToObject
    form_finding_sag_related_to_surface: int
    magnitude_mass_global: float
    ponding_magnitude_specific_weight: float
    ponding_magnitude_amount_precipitation: float
    ponding_amount_precipitation: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    magnitude_orthogonal_force_x: float
    magnitude_orthogonal_force_y: float
    magnitude_orthogonal_stress_x: float
    magnitude_orthogonal_stress_y: float
    magnitude_uniform_force_x: float
    magnitude_uniform_force_y: float
    magnitude_uniform_stress_x: float
    magnitude_uniform_stress_y: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[SurfaceSetLoadLoadType, str]] = ..., surface_sets: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[str] = ..., load_distribution: _Optional[_Union[SurfaceSetLoadLoadDistribution, str]] = ..., load_direction: _Optional[_Union[SurfaceSetLoadLoadDirection, str]] = ..., individual_mass_components: bool = ..., uniform_magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., magnitude_3: _Optional[float] = ..., uniform_magnitude_t_c: _Optional[float] = ..., magnitude_t_c_1: _Optional[float] = ..., magnitude_t_c_2: _Optional[float] = ..., magnitude_t_c_3: _Optional[float] = ..., uniform_magnitude_delta_t: _Optional[float] = ..., magnitude_delta_t_1: _Optional[float] = ..., magnitude_delta_t_2: _Optional[float] = ..., magnitude_delta_t_3: _Optional[float] = ..., magnitude_axial_strain_x: _Optional[float] = ..., magnitude_axial_strain_y: _Optional[float] = ..., magnitude_axial_strain_1x: _Optional[float] = ..., magnitude_axial_strain_1y: _Optional[float] = ..., magnitude_axial_strain_2x: _Optional[float] = ..., magnitude_axial_strain_2y: _Optional[float] = ..., magnitude_axial_strain_3x: _Optional[float] = ..., magnitude_axial_strain_3y: _Optional[float] = ..., angular_velocity: _Optional[float] = ..., angular_acceleration: _Optional[float] = ..., node_1: _Optional[int] = ..., node_2: _Optional[int] = ..., node_3: _Optional[int] = ..., axis_definition_type: _Optional[_Union[SurfaceSetLoadAxisDefinitionType, str]] = ..., axis_definition_p1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p1_x: _Optional[float] = ..., axis_definition_p1_y: _Optional[float] = ..., axis_definition_p1_z: _Optional[float] = ..., axis_definition_p2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p2_x: _Optional[float] = ..., axis_definition_p2_y: _Optional[float] = ..., axis_definition_p2_z: _Optional[float] = ..., axis_definition_axis: _Optional[_Union[SurfaceSetLoadAxisDefinitionAxis, str]] = ..., axis_definition_axis_orientation: _Optional[_Union[SurfaceSetLoadAxisDefinitionAxisOrientation, str]] = ..., varying_load_parameters: _Optional[_Union[SurfaceSetLoadVaryingLoadParametersTable, _Mapping]] = ..., varying_load_parameters_sorted: bool = ..., form_finding_definition: _Optional[_Union[SurfaceSetLoadFormFindingDefinition, str]] = ..., magnitude_force_u: _Optional[float] = ..., magnitude_force_v: _Optional[float] = ..., magnitude_force_r: _Optional[float] = ..., magnitude_force_t: _Optional[float] = ..., magnitude_mass_x: _Optional[float] = ..., magnitude_mass_y: _Optional[float] = ..., magnitude_mass_z: _Optional[float] = ..., magnitude_stress_u: _Optional[float] = ..., magnitude_stress_v: _Optional[float] = ..., magnitude_stress_r: _Optional[float] = ..., magnitude_stress_t: _Optional[float] = ..., magnitude_sag: _Optional[float] = ..., magnitude_force_scale_x: _Optional[float] = ..., magnitude_force_scale_y: _Optional[float] = ..., form_finding_calculation_method: _Optional[_Union[SurfaceSetLoadFormFindingCalculationMethod, str]] = ..., form_finding_sag_related_to_object: _Optional[_Union[SurfaceSetLoadFormFindingSagRelatedToObject, str]] = ..., form_finding_sag_related_to_surface: _Optional[int] = ..., magnitude_mass_global: _Optional[float] = ..., ponding_magnitude_specific_weight: _Optional[float] = ..., ponding_magnitude_amount_precipitation: _Optional[float] = ..., ponding_amount_precipitation: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., magnitude_orthogonal_force_x: _Optional[float] = ..., magnitude_orthogonal_force_y: _Optional[float] = ..., magnitude_orthogonal_stress_x: _Optional[float] = ..., magnitude_orthogonal_stress_y: _Optional[float] = ..., magnitude_uniform_force_x: _Optional[float] = ..., magnitude_uniform_force_y: _Optional[float] = ..., magnitude_uniform_stress_x: _Optional[float] = ..., magnitude_uniform_stress_y: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class SurfaceSetLoadVaryingLoadParametersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceSetLoadVaryingLoadParametersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceSetLoadVaryingLoadParametersRow, _Mapping]]] = ...) -> None: ...

class SurfaceSetLoadVaryingLoadParametersRow(_message.Message):
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
