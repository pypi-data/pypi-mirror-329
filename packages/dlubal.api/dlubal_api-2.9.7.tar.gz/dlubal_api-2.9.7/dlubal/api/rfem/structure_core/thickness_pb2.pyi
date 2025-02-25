from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThicknessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_TYPE_UNKNOWN: _ClassVar[ThicknessType]
    THICKNESS_TYPE_BEAM_PANEL: _ClassVar[ThicknessType]
    THICKNESS_TYPE_GLASS_COMPOSITION: _ClassVar[ThicknessType]
    THICKNESS_TYPE_LAYERS: _ClassVar[ThicknessType]
    THICKNESS_TYPE_SHAPE_ORTHOTROPY: _ClassVar[ThicknessType]
    THICKNESS_TYPE_STIFFNESS_MATRIX: _ClassVar[ThicknessType]
    THICKNESS_TYPE_THICKNESS_PHASE: _ClassVar[ThicknessType]
    THICKNESS_TYPE_UNIFORM: _ClassVar[ThicknessType]
    THICKNESS_TYPE_VARIABLE_CIRCLE: _ClassVar[ThicknessType]
    THICKNESS_TYPE_VARIABLE_FOUR_SURFACE_CORNERS: _ClassVar[ThicknessType]
    THICKNESS_TYPE_VARIABLE_THREE_NODES: _ClassVar[ThicknessType]
    THICKNESS_TYPE_VARIABLE_TWO_NODES_AND_DIRECTION: _ClassVar[ThicknessType]
    THICKNESS_TYPE_WALL_SHEAR_FREE: _ClassVar[ThicknessType]
    THICKNESS_TYPE_WALL_SHEAR_FREE_IN_X: _ClassVar[ThicknessType]
    THICKNESS_TYPE_WALL_SHEAR_FREE_IN_Y: _ClassVar[ThicknessType]

class ThicknessIntegrationMethodType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_INTEGRATION_METHOD_TYPE_GAUSS_LOBATTO_QUADRATURE: _ClassVar[ThicknessIntegrationMethodType]
    THICKNESS_INTEGRATION_METHOD_TYPE_SIMPSONS_RULE: _ClassVar[ThicknessIntegrationMethodType]
    THICKNESS_INTEGRATION_METHOD_TYPE_TRAPEZOIDAL_RULE: _ClassVar[ThicknessIntegrationMethodType]

class ThicknessDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_DIRECTION_GLOBAL_IN_X: _ClassVar[ThicknessDirection]
    THICKNESS_DIRECTION_GLOBAL_IN_Y: _ClassVar[ThicknessDirection]
    THICKNESS_DIRECTION_GLOBAL_IN_Z: _ClassVar[ThicknessDirection]
    THICKNESS_DIRECTION_LOCAL_IN_X: _ClassVar[ThicknessDirection]
    THICKNESS_DIRECTION_LOCAL_IN_Y: _ClassVar[ThicknessDirection]

class ThicknessLayersReferenceTableLayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_LAYER: _ClassVar[ThicknessLayersReferenceTableLayerType]
    THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_CONTACT: _ClassVar[ThicknessLayersReferenceTableLayerType]
    THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_GAS: _ClassVar[ThicknessLayersReferenceTableLayerType]

class ThicknessFunctionDataFunctionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_CREEP_COEFFICIENT: _ClassVar[ThicknessFunctionDataFunctionType]
    THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CA: _ClassVar[ThicknessFunctionDataFunctionType]
    THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CD: _ClassVar[ThicknessFunctionDataFunctionType]
    THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CS: _ClassVar[ThicknessFunctionDataFunctionType]

class ThicknessOrthotropyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_ORTHOTROPY_TYPE_EFFECTIVE_THICKNESSES: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_BIDIRECTIONAL_RIBBED_PLATE: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_COUPLING: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_GRILLAGE: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_HOLLOW_CORE_SLAB: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_TRAPEZOIDAL_SHEET: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_UNIDIRECTIONAL_BOX_FLOOR: _ClassVar[ThicknessOrthotropyType]
    THICKNESS_ORTHOTROPY_TYPE_UNIDIRECTIONAL_RIBBED_PLATE: _ClassVar[ThicknessOrthotropyType]

class ThicknessShapeOrthotropySelfWeightDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_COMPUTED_FROM_PARAMETERS: _ClassVar[ThicknessShapeOrthotropySelfWeightDefinitionType]
    THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS: _ClassVar[ThicknessShapeOrthotropySelfWeightDefinitionType]
    THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_WEIGHT: _ClassVar[ThicknessShapeOrthotropySelfWeightDefinitionType]

class ThicknessStiffnessMatrixSelfWeightDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_AND_BULK_DENSITY: _ClassVar[ThicknessStiffnessMatrixSelfWeightDefinitionType]
    THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_BULK_DENSITY_AND_AREA_DENSITY: _ClassVar[ThicknessStiffnessMatrixSelfWeightDefinitionType]
    THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_AND_AREA_DENSITY: _ClassVar[ThicknessStiffnessMatrixSelfWeightDefinitionType]
THICKNESS_TYPE_UNKNOWN: ThicknessType
THICKNESS_TYPE_BEAM_PANEL: ThicknessType
THICKNESS_TYPE_GLASS_COMPOSITION: ThicknessType
THICKNESS_TYPE_LAYERS: ThicknessType
THICKNESS_TYPE_SHAPE_ORTHOTROPY: ThicknessType
THICKNESS_TYPE_STIFFNESS_MATRIX: ThicknessType
THICKNESS_TYPE_THICKNESS_PHASE: ThicknessType
THICKNESS_TYPE_UNIFORM: ThicknessType
THICKNESS_TYPE_VARIABLE_CIRCLE: ThicknessType
THICKNESS_TYPE_VARIABLE_FOUR_SURFACE_CORNERS: ThicknessType
THICKNESS_TYPE_VARIABLE_THREE_NODES: ThicknessType
THICKNESS_TYPE_VARIABLE_TWO_NODES_AND_DIRECTION: ThicknessType
THICKNESS_TYPE_WALL_SHEAR_FREE: ThicknessType
THICKNESS_TYPE_WALL_SHEAR_FREE_IN_X: ThicknessType
THICKNESS_TYPE_WALL_SHEAR_FREE_IN_Y: ThicknessType
THICKNESS_INTEGRATION_METHOD_TYPE_GAUSS_LOBATTO_QUADRATURE: ThicknessIntegrationMethodType
THICKNESS_INTEGRATION_METHOD_TYPE_SIMPSONS_RULE: ThicknessIntegrationMethodType
THICKNESS_INTEGRATION_METHOD_TYPE_TRAPEZOIDAL_RULE: ThicknessIntegrationMethodType
THICKNESS_DIRECTION_GLOBAL_IN_X: ThicknessDirection
THICKNESS_DIRECTION_GLOBAL_IN_Y: ThicknessDirection
THICKNESS_DIRECTION_GLOBAL_IN_Z: ThicknessDirection
THICKNESS_DIRECTION_LOCAL_IN_X: ThicknessDirection
THICKNESS_DIRECTION_LOCAL_IN_Y: ThicknessDirection
THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_LAYER: ThicknessLayersReferenceTableLayerType
THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_CONTACT: ThicknessLayersReferenceTableLayerType
THICKNESS_LAYERS_REFERENCE_TABLE_LAYER_TYPE_E_LAYER_TYPE_GAS: ThicknessLayersReferenceTableLayerType
THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_CREEP_COEFFICIENT: ThicknessFunctionDataFunctionType
THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CA: ThicknessFunctionDataFunctionType
THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CD: ThicknessFunctionDataFunctionType
THICKNESS_FUNCTION_DATA_FUNCTION_TYPE_SHRINKAGE_STRAIN_CS: ThicknessFunctionDataFunctionType
THICKNESS_ORTHOTROPY_TYPE_EFFECTIVE_THICKNESSES: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_BIDIRECTIONAL_RIBBED_PLATE: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_COUPLING: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_GRILLAGE: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_HOLLOW_CORE_SLAB: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_TRAPEZOIDAL_SHEET: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_UNIDIRECTIONAL_BOX_FLOOR: ThicknessOrthotropyType
THICKNESS_ORTHOTROPY_TYPE_UNIDIRECTIONAL_RIBBED_PLATE: ThicknessOrthotropyType
THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_COMPUTED_FROM_PARAMETERS: ThicknessShapeOrthotropySelfWeightDefinitionType
THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS: ThicknessShapeOrthotropySelfWeightDefinitionType
THICKNESS_SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_WEIGHT: ThicknessShapeOrthotropySelfWeightDefinitionType
THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_AND_BULK_DENSITY: ThicknessStiffnessMatrixSelfWeightDefinitionType
THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_BULK_DENSITY_AND_AREA_DENSITY: ThicknessStiffnessMatrixSelfWeightDefinitionType
THICKNESS_STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_DEFINED_VIA_FICTITIOUS_THICKNESS_AND_AREA_DENSITY: ThicknessStiffnessMatrixSelfWeightDefinitionType

class Thickness(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_surfaces", "type", "material", "uniform_thickness", "uniform_or_fictitious_thickness", "advanced_time_dependent_properties_of_concrete_enabled", "creep_enabled", "shrinkage_enabled", "relative_humidity", "specify_integration_method_enabled", "integration_method_type", "number_of_integration_points", "thickness_1", "node_1", "thickness_2", "node_2", "thickness_3", "node_3", "direction", "thickness_4", "node_4", "thickness_circle_center", "thickness_circle_line", "comment", "layers_reference_table", "layers_solid_model_enabled", "layers_gas_enabled", "layers_total_thickness", "layers_total_weight", "stiffness_reduction_enabled", "is_enabled_design_of_failure", "plank_width_bx", "plank_width_by", "plank_width_including_gap_enabled", "plank_width_including_gap_ex", "plank_width_including_gap_ey", "stiffness_reduction_elements_editing_enabled", "K33", "K44", "K55", "K88", "K33_note", "K44_note", "K55_note", "K88_note", "function_data_function_type", "function_data_layer_id", "function_data_age_of_concrete_at_the_considered_time", "function_data_number_of_steps", "function_data_coefficients", "parent_thickness", "parent_thickness_layers", "orthotropy_type", "orthotropy_rotation_beta", "orthotropy_fictitious_thickness", "shape_orthotropy_self_weight_definition_type", "shape_orthotropy_effective_thickness_x", "shape_orthotropy_effective_thickness_y", "shape_orthotropy_self_weight", "stiffness_matrix_self_weight_definition_type", "stiffness_matrix_bulk_density", "stiffness_matrix_area_density", "stiffness_matrix_coefficient_of_thermal_expansion", "coupling_thickness", "coupling_spacing", "coupling_width", "slab_thickness", "rib_height", "rib_spacing", "rib_width", "rib_spacing_x", "rib_spacing_y", "rib_width_x", "rib_width_y", "sheet_thickness", "total_profile_height", "top_flange_width", "bottom_flange_width", "void_spacing", "void_diameter", "rib_height_x", "rib_height_y", "D11", "D11_note", "D12", "D12_note", "D13", "D13_note", "D16", "D16_note", "D17", "D17_note", "D18", "D18_note", "D22", "D22_note", "D23", "D23_note", "D27", "D27_note", "D28", "D28_note", "D33", "D33_note", "D38", "D38_note", "D44", "D44_note", "D45", "D45_note", "D55", "D55_note", "D66", "D66_note", "D67", "D67_note", "D68", "D68_note", "D77", "D77_note", "D78", "D78_note", "D88", "D88_note", "is_generated", "generating_object_info", "time_dependent_properties", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_OR_FICTITIOUS_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ADVANCED_TIME_DEPENDENT_PROPERTIES_OF_CONCRETE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CREEP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SHRINKAGE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    SPECIFY_INTEGRATION_METHOD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_METHOD_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_INTEGRATION_POINTS_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_1_FIELD_NUMBER: _ClassVar[int]
    NODE_1_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_2_FIELD_NUMBER: _ClassVar[int]
    NODE_2_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_3_FIELD_NUMBER: _ClassVar[int]
    NODE_3_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_4_FIELD_NUMBER: _ClassVar[int]
    NODE_4_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_CIRCLE_CENTER_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_CIRCLE_LINE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    LAYERS_REFERENCE_TABLE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_SOLID_MODEL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAYERS_GAS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAYERS_TOTAL_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_TOTAL_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_REDUCTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_ENABLED_DESIGN_OF_FAILURE_FIELD_NUMBER: _ClassVar[int]
    PLANK_WIDTH_BX_FIELD_NUMBER: _ClassVar[int]
    PLANK_WIDTH_BY_FIELD_NUMBER: _ClassVar[int]
    PLANK_WIDTH_INCLUDING_GAP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PLANK_WIDTH_INCLUDING_GAP_EX_FIELD_NUMBER: _ClassVar[int]
    PLANK_WIDTH_INCLUDING_GAP_EY_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_REDUCTION_ELEMENTS_EDITING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    K33_FIELD_NUMBER: _ClassVar[int]
    K44_FIELD_NUMBER: _ClassVar[int]
    K55_FIELD_NUMBER: _ClassVar[int]
    K88_FIELD_NUMBER: _ClassVar[int]
    K33_NOTE_FIELD_NUMBER: _ClassVar[int]
    K44_NOTE_FIELD_NUMBER: _ClassVar[int]
    K55_NOTE_FIELD_NUMBER: _ClassVar[int]
    K88_NOTE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DATA_FUNCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DATA_LAYER_ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DATA_AGE_OF_CONCRETE_AT_THE_CONSIDERED_TIME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DATA_NUMBER_OF_STEPS_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DATA_COEFFICIENTS_FIELD_NUMBER: _ClassVar[int]
    PARENT_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    PARENT_THICKNESS_LAYERS_FIELD_NUMBER: _ClassVar[int]
    ORTHOTROPY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORTHOTROPY_ROTATION_BETA_FIELD_NUMBER: _ClassVar[int]
    ORTHOTROPY_FICTITIOUS_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_ORTHOTROPY_SELF_WEIGHT_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_ORTHOTROPY_EFFECTIVE_THICKNESS_X_FIELD_NUMBER: _ClassVar[int]
    SHAPE_ORTHOTROPY_EFFECTIVE_THICKNESS_Y_FIELD_NUMBER: _ClassVar[int]
    SHAPE_ORTHOTROPY_SELF_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_SELF_WEIGHT_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_BULK_DENSITY_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_AREA_DENSITY_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_COEFFICIENT_OF_THERMAL_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    COUPLING_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    COUPLING_SPACING_FIELD_NUMBER: _ClassVar[int]
    COUPLING_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SLAB_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    RIB_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RIB_SPACING_FIELD_NUMBER: _ClassVar[int]
    RIB_WIDTH_FIELD_NUMBER: _ClassVar[int]
    RIB_SPACING_X_FIELD_NUMBER: _ClassVar[int]
    RIB_SPACING_Y_FIELD_NUMBER: _ClassVar[int]
    RIB_WIDTH_X_FIELD_NUMBER: _ClassVar[int]
    RIB_WIDTH_Y_FIELD_NUMBER: _ClassVar[int]
    SHEET_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PROFILE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TOP_FLANGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FLANGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    VOID_SPACING_FIELD_NUMBER: _ClassVar[int]
    VOID_DIAMETER_FIELD_NUMBER: _ClassVar[int]
    RIB_HEIGHT_X_FIELD_NUMBER: _ClassVar[int]
    RIB_HEIGHT_Y_FIELD_NUMBER: _ClassVar[int]
    D11_FIELD_NUMBER: _ClassVar[int]
    D11_NOTE_FIELD_NUMBER: _ClassVar[int]
    D12_FIELD_NUMBER: _ClassVar[int]
    D12_NOTE_FIELD_NUMBER: _ClassVar[int]
    D13_FIELD_NUMBER: _ClassVar[int]
    D13_NOTE_FIELD_NUMBER: _ClassVar[int]
    D16_FIELD_NUMBER: _ClassVar[int]
    D16_NOTE_FIELD_NUMBER: _ClassVar[int]
    D17_FIELD_NUMBER: _ClassVar[int]
    D17_NOTE_FIELD_NUMBER: _ClassVar[int]
    D18_FIELD_NUMBER: _ClassVar[int]
    D18_NOTE_FIELD_NUMBER: _ClassVar[int]
    D22_FIELD_NUMBER: _ClassVar[int]
    D22_NOTE_FIELD_NUMBER: _ClassVar[int]
    D23_FIELD_NUMBER: _ClassVar[int]
    D23_NOTE_FIELD_NUMBER: _ClassVar[int]
    D27_FIELD_NUMBER: _ClassVar[int]
    D27_NOTE_FIELD_NUMBER: _ClassVar[int]
    D28_FIELD_NUMBER: _ClassVar[int]
    D28_NOTE_FIELD_NUMBER: _ClassVar[int]
    D33_FIELD_NUMBER: _ClassVar[int]
    D33_NOTE_FIELD_NUMBER: _ClassVar[int]
    D38_FIELD_NUMBER: _ClassVar[int]
    D38_NOTE_FIELD_NUMBER: _ClassVar[int]
    D44_FIELD_NUMBER: _ClassVar[int]
    D44_NOTE_FIELD_NUMBER: _ClassVar[int]
    D45_FIELD_NUMBER: _ClassVar[int]
    D45_NOTE_FIELD_NUMBER: _ClassVar[int]
    D55_FIELD_NUMBER: _ClassVar[int]
    D55_NOTE_FIELD_NUMBER: _ClassVar[int]
    D66_FIELD_NUMBER: _ClassVar[int]
    D66_NOTE_FIELD_NUMBER: _ClassVar[int]
    D67_FIELD_NUMBER: _ClassVar[int]
    D67_NOTE_FIELD_NUMBER: _ClassVar[int]
    D68_FIELD_NUMBER: _ClassVar[int]
    D68_NOTE_FIELD_NUMBER: _ClassVar[int]
    D77_FIELD_NUMBER: _ClassVar[int]
    D77_NOTE_FIELD_NUMBER: _ClassVar[int]
    D78_FIELD_NUMBER: _ClassVar[int]
    D78_NOTE_FIELD_NUMBER: _ClassVar[int]
    D88_FIELD_NUMBER: _ClassVar[int]
    D88_NOTE_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    TIME_DEPENDENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_to_surfaces: _containers.RepeatedScalarFieldContainer[int]
    type: ThicknessType
    material: int
    uniform_thickness: float
    uniform_or_fictitious_thickness: float
    advanced_time_dependent_properties_of_concrete_enabled: bool
    creep_enabled: bool
    shrinkage_enabled: bool
    relative_humidity: float
    specify_integration_method_enabled: bool
    integration_method_type: ThicknessIntegrationMethodType
    number_of_integration_points: int
    thickness_1: float
    node_1: int
    thickness_2: float
    node_2: int
    thickness_3: float
    node_3: int
    direction: ThicknessDirection
    thickness_4: float
    node_4: int
    thickness_circle_center: float
    thickness_circle_line: float
    comment: str
    layers_reference_table: ThicknessLayersReferenceTable
    layers_solid_model_enabled: bool
    layers_gas_enabled: bool
    layers_total_thickness: float
    layers_total_weight: float
    stiffness_reduction_enabled: bool
    is_enabled_design_of_failure: bool
    plank_width_bx: float
    plank_width_by: float
    plank_width_including_gap_enabled: bool
    plank_width_including_gap_ex: float
    plank_width_including_gap_ey: float
    stiffness_reduction_elements_editing_enabled: bool
    K33: float
    K44: float
    K55: float
    K88: float
    K33_note: str
    K44_note: str
    K55_note: str
    K88_note: str
    function_data_function_type: ThicknessFunctionDataFunctionType
    function_data_layer_id: int
    function_data_age_of_concrete_at_the_considered_time: float
    function_data_number_of_steps: int
    function_data_coefficients: ThicknessFunctionDataCoefficientsTable
    parent_thickness: int
    parent_thickness_layers: _containers.RepeatedScalarFieldContainer[int]
    orthotropy_type: ThicknessOrthotropyType
    orthotropy_rotation_beta: float
    orthotropy_fictitious_thickness: float
    shape_orthotropy_self_weight_definition_type: ThicknessShapeOrthotropySelfWeightDefinitionType
    shape_orthotropy_effective_thickness_x: float
    shape_orthotropy_effective_thickness_y: float
    shape_orthotropy_self_weight: float
    stiffness_matrix_self_weight_definition_type: ThicknessStiffnessMatrixSelfWeightDefinitionType
    stiffness_matrix_bulk_density: float
    stiffness_matrix_area_density: float
    stiffness_matrix_coefficient_of_thermal_expansion: float
    coupling_thickness: float
    coupling_spacing: float
    coupling_width: float
    slab_thickness: float
    rib_height: float
    rib_spacing: float
    rib_width: float
    rib_spacing_x: float
    rib_spacing_y: float
    rib_width_x: float
    rib_width_y: float
    sheet_thickness: float
    total_profile_height: float
    top_flange_width: float
    bottom_flange_width: float
    void_spacing: float
    void_diameter: float
    rib_height_x: float
    rib_height_y: float
    D11: float
    D11_note: str
    D12: float
    D12_note: str
    D13: float
    D13_note: str
    D16: float
    D16_note: str
    D17: float
    D17_note: str
    D18: float
    D18_note: str
    D22: float
    D22_note: str
    D23: float
    D23_note: str
    D27: float
    D27_note: str
    D28: float
    D28_note: str
    D33: float
    D33_note: str
    D38: float
    D38_note: str
    D44: float
    D44_note: str
    D45: float
    D45_note: str
    D55: float
    D55_note: str
    D66: float
    D66_note: str
    D67: float
    D67_note: str
    D68: float
    D68_note: str
    D77: float
    D77_note: str
    D78: float
    D78_note: str
    D88: float
    D88_note: str
    is_generated: bool
    generating_object_info: str
    time_dependent_properties: ThicknessTimeDependentPropertiesAndChildItemsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[ThicknessType, str]] = ..., material: _Optional[int] = ..., uniform_thickness: _Optional[float] = ..., uniform_or_fictitious_thickness: _Optional[float] = ..., advanced_time_dependent_properties_of_concrete_enabled: bool = ..., creep_enabled: bool = ..., shrinkage_enabled: bool = ..., relative_humidity: _Optional[float] = ..., specify_integration_method_enabled: bool = ..., integration_method_type: _Optional[_Union[ThicknessIntegrationMethodType, str]] = ..., number_of_integration_points: _Optional[int] = ..., thickness_1: _Optional[float] = ..., node_1: _Optional[int] = ..., thickness_2: _Optional[float] = ..., node_2: _Optional[int] = ..., thickness_3: _Optional[float] = ..., node_3: _Optional[int] = ..., direction: _Optional[_Union[ThicknessDirection, str]] = ..., thickness_4: _Optional[float] = ..., node_4: _Optional[int] = ..., thickness_circle_center: _Optional[float] = ..., thickness_circle_line: _Optional[float] = ..., comment: _Optional[str] = ..., layers_reference_table: _Optional[_Union[ThicknessLayersReferenceTable, _Mapping]] = ..., layers_solid_model_enabled: bool = ..., layers_gas_enabled: bool = ..., layers_total_thickness: _Optional[float] = ..., layers_total_weight: _Optional[float] = ..., stiffness_reduction_enabled: bool = ..., is_enabled_design_of_failure: bool = ..., plank_width_bx: _Optional[float] = ..., plank_width_by: _Optional[float] = ..., plank_width_including_gap_enabled: bool = ..., plank_width_including_gap_ex: _Optional[float] = ..., plank_width_including_gap_ey: _Optional[float] = ..., stiffness_reduction_elements_editing_enabled: bool = ..., K33: _Optional[float] = ..., K44: _Optional[float] = ..., K55: _Optional[float] = ..., K88: _Optional[float] = ..., K33_note: _Optional[str] = ..., K44_note: _Optional[str] = ..., K55_note: _Optional[str] = ..., K88_note: _Optional[str] = ..., function_data_function_type: _Optional[_Union[ThicknessFunctionDataFunctionType, str]] = ..., function_data_layer_id: _Optional[int] = ..., function_data_age_of_concrete_at_the_considered_time: _Optional[float] = ..., function_data_number_of_steps: _Optional[int] = ..., function_data_coefficients: _Optional[_Union[ThicknessFunctionDataCoefficientsTable, _Mapping]] = ..., parent_thickness: _Optional[int] = ..., parent_thickness_layers: _Optional[_Iterable[int]] = ..., orthotropy_type: _Optional[_Union[ThicknessOrthotropyType, str]] = ..., orthotropy_rotation_beta: _Optional[float] = ..., orthotropy_fictitious_thickness: _Optional[float] = ..., shape_orthotropy_self_weight_definition_type: _Optional[_Union[ThicknessShapeOrthotropySelfWeightDefinitionType, str]] = ..., shape_orthotropy_effective_thickness_x: _Optional[float] = ..., shape_orthotropy_effective_thickness_y: _Optional[float] = ..., shape_orthotropy_self_weight: _Optional[float] = ..., stiffness_matrix_self_weight_definition_type: _Optional[_Union[ThicknessStiffnessMatrixSelfWeightDefinitionType, str]] = ..., stiffness_matrix_bulk_density: _Optional[float] = ..., stiffness_matrix_area_density: _Optional[float] = ..., stiffness_matrix_coefficient_of_thermal_expansion: _Optional[float] = ..., coupling_thickness: _Optional[float] = ..., coupling_spacing: _Optional[float] = ..., coupling_width: _Optional[float] = ..., slab_thickness: _Optional[float] = ..., rib_height: _Optional[float] = ..., rib_spacing: _Optional[float] = ..., rib_width: _Optional[float] = ..., rib_spacing_x: _Optional[float] = ..., rib_spacing_y: _Optional[float] = ..., rib_width_x: _Optional[float] = ..., rib_width_y: _Optional[float] = ..., sheet_thickness: _Optional[float] = ..., total_profile_height: _Optional[float] = ..., top_flange_width: _Optional[float] = ..., bottom_flange_width: _Optional[float] = ..., void_spacing: _Optional[float] = ..., void_diameter: _Optional[float] = ..., rib_height_x: _Optional[float] = ..., rib_height_y: _Optional[float] = ..., D11: _Optional[float] = ..., D11_note: _Optional[str] = ..., D12: _Optional[float] = ..., D12_note: _Optional[str] = ..., D13: _Optional[float] = ..., D13_note: _Optional[str] = ..., D16: _Optional[float] = ..., D16_note: _Optional[str] = ..., D17: _Optional[float] = ..., D17_note: _Optional[str] = ..., D18: _Optional[float] = ..., D18_note: _Optional[str] = ..., D22: _Optional[float] = ..., D22_note: _Optional[str] = ..., D23: _Optional[float] = ..., D23_note: _Optional[str] = ..., D27: _Optional[float] = ..., D27_note: _Optional[str] = ..., D28: _Optional[float] = ..., D28_note: _Optional[str] = ..., D33: _Optional[float] = ..., D33_note: _Optional[str] = ..., D38: _Optional[float] = ..., D38_note: _Optional[str] = ..., D44: _Optional[float] = ..., D44_note: _Optional[str] = ..., D45: _Optional[float] = ..., D45_note: _Optional[str] = ..., D55: _Optional[float] = ..., D55_note: _Optional[str] = ..., D66: _Optional[float] = ..., D66_note: _Optional[str] = ..., D67: _Optional[float] = ..., D67_note: _Optional[str] = ..., D68: _Optional[float] = ..., D68_note: _Optional[str] = ..., D77: _Optional[float] = ..., D77_note: _Optional[str] = ..., D78: _Optional[float] = ..., D78_note: _Optional[str] = ..., D88: _Optional[float] = ..., D88_note: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., time_dependent_properties: _Optional[_Union[ThicknessTimeDependentPropertiesAndChildItemsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class ThicknessLayersReferenceTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ThicknessLayersReferenceTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ThicknessLayersReferenceTableRow, _Mapping]]] = ...) -> None: ...

class ThicknessLayersReferenceTableRow(_message.Message):
    __slots__ = ("no", "description", "layer_no", "layer_type", "thickness_type_or_id", "material", "thickness", "angle", "integration_points", "connection_with_other_topological_elements", "comment", "specific_weight", "weight")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LAYER_NO_FIELD_NUMBER: _ClassVar[int]
    LAYER_TYPE_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_TYPE_OR_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_WITH_OTHER_TOPOLOGICAL_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    layer_no: int
    layer_type: ThicknessLayersReferenceTableLayerType
    thickness_type_or_id: str
    material: int
    thickness: float
    angle: float
    integration_points: int
    connection_with_other_topological_elements: bool
    comment: str
    specific_weight: float
    weight: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., layer_no: _Optional[int] = ..., layer_type: _Optional[_Union[ThicknessLayersReferenceTableLayerType, str]] = ..., thickness_type_or_id: _Optional[str] = ..., material: _Optional[int] = ..., thickness: _Optional[float] = ..., angle: _Optional[float] = ..., integration_points: _Optional[int] = ..., connection_with_other_topological_elements: bool = ..., comment: _Optional[str] = ..., specific_weight: _Optional[float] = ..., weight: _Optional[float] = ...) -> None: ...

class ThicknessFunctionDataCoefficientsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ThicknessFunctionDataCoefficientsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ThicknessFunctionDataCoefficientsRow, _Mapping]]] = ...) -> None: ...

class ThicknessFunctionDataCoefficientsRow(_message.Message):
    __slots__ = ("no", "description", "time", "coefficient")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    time: float
    coefficient: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., time: _Optional[float] = ..., coefficient: _Optional[float] = ...) -> None: ...

class ThicknessTimeDependentPropertiesAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
