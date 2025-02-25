from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadCombinationAnalysisType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_ANALYSIS_TYPE_UNKNOWN: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_HARMONIC_RESPONSE_ANALYSIS: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_PUSHOVER: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_STATIC: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_STATIC_CREEP_AND_SHRINKAGE: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_STATIC_TIME_DEPENDENCE: _ClassVar[LoadCombinationAnalysisType]
    LOAD_COMBINATION_ANALYSIS_TYPE_TIME_HISTORY_TIME_DIAGRAM: _ClassVar[LoadCombinationAnalysisType]

class LoadCombinationItemsAmplitudeFunctionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_CONSTANT: _ClassVar[LoadCombinationItemsAmplitudeFunctionType]
    LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_LINEAR: _ClassVar[LoadCombinationItemsAmplitudeFunctionType]
    LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_QUADRATIC: _ClassVar[LoadCombinationItemsAmplitudeFunctionType]

class LoadCombinationInitialStateDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_FINAL_STATE: _ClassVar[LoadCombinationInitialStateDefinitionType]
    LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STIFFNESS: _ClassVar[LoadCombinationInitialStateDefinitionType]
    LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS: _ClassVar[LoadCombinationInitialStateDefinitionType]
    LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS_WITH_USER_DEFINED_FACTORS: _ClassVar[LoadCombinationInitialStateDefinitionType]

class LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_HINGE: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER_HINGE: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType]

class LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALL: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_X: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Y: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Z: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_X: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Y: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]
    LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Z: _ClassVar[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType]

class LoadCombinationPushoverDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_PUSHOVER_DIRECTION_X: _ClassVar[LoadCombinationPushoverDirection]
    LOAD_COMBINATION_PUSHOVER_DIRECTION_MINUS_X: _ClassVar[LoadCombinationPushoverDirection]
    LOAD_COMBINATION_PUSHOVER_DIRECTION_MINUS_Y: _ClassVar[LoadCombinationPushoverDirection]
    LOAD_COMBINATION_PUSHOVER_DIRECTION_Y: _ClassVar[LoadCombinationPushoverDirection]

class LoadCombinationPushoverNormalizedDisplacements(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_UNIFORM: _ClassVar[LoadCombinationPushoverNormalizedDisplacements]
    LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_MODAL_AUTOMATIC_MODAL_SHAPE: _ClassVar[LoadCombinationPushoverNormalizedDisplacements]
    LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_MODAL_USER_SELECTED_MODAL_SHAPE: _ClassVar[LoadCombinationPushoverNormalizedDisplacements]
LOAD_COMBINATION_ANALYSIS_TYPE_UNKNOWN: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_HARMONIC_RESPONSE_ANALYSIS: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_PUSHOVER: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_STATIC: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_STATIC_CREEP_AND_SHRINKAGE: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_STATIC_TIME_DEPENDENCE: LoadCombinationAnalysisType
LOAD_COMBINATION_ANALYSIS_TYPE_TIME_HISTORY_TIME_DIAGRAM: LoadCombinationAnalysisType
LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_CONSTANT: LoadCombinationItemsAmplitudeFunctionType
LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_LINEAR: LoadCombinationItemsAmplitudeFunctionType
LOAD_COMBINATION_ITEMS_AMPLITUDE_FUNCTION_TYPE_QUADRATIC: LoadCombinationItemsAmplitudeFunctionType
LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_FINAL_STATE: LoadCombinationInitialStateDefinitionType
LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STIFFNESS: LoadCombinationInitialStateDefinitionType
LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS: LoadCombinationInitialStateDefinitionType
LOAD_COMBINATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS_WITH_USER_DEFINED_FACTORS: LoadCombinationInitialStateDefinitionType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_HINGE: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER_HINGE: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALL: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_X: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Y: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Z: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_X: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Y: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Z: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
LOAD_COMBINATION_PUSHOVER_DIRECTION_X: LoadCombinationPushoverDirection
LOAD_COMBINATION_PUSHOVER_DIRECTION_MINUS_X: LoadCombinationPushoverDirection
LOAD_COMBINATION_PUSHOVER_DIRECTION_MINUS_Y: LoadCombinationPushoverDirection
LOAD_COMBINATION_PUSHOVER_DIRECTION_Y: LoadCombinationPushoverDirection
LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_UNIFORM: LoadCombinationPushoverNormalizedDisplacements
LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_MODAL_AUTOMATIC_MODAL_SHAPE: LoadCombinationPushoverNormalizedDisplacements
LOAD_COMBINATION_PUSHOVER_NORMALIZED_DISPLACEMENTS_MODAL_USER_SELECTED_MODAL_SHAPE: LoadCombinationPushoverNormalizedDisplacements

class LoadCombination(_message.Message):
    __slots__ = ("no", "analysis_type", "design_situation", "user_defined_name_enabled", "name", "static_analysis_settings", "import_modal_analysis_load_case", "calculate_critical_load", "stability_analysis_settings", "consider_imperfection", "imperfection_case", "consider_initial_state", "initial_state_case", "consider_construction_stage", "construction_stage", "creep_loading_case", "sustained_load_enabled", "sustained_load", "sway_load_enabled", "sway_load", "structure_modification_enabled", "structure_modification", "to_solve", "comment", "load_duration", "items", "combination_rule_str", "loading_start", "time_being_investigated", "is_generated", "generating_object_info", "initial_state_definition_type", "individual_factors_of_selected_objects_table", "geotechnical_analysis_reset_small_strain_history", "pushover_vertical_loads_case", "pushover_modal_analysis_from_load_case", "pushover_direction", "pushover_normalized_displacements", "pushover_mode_shape_number", "pushover_response_spectrum", "pushover_response_spectrum_scale_factor", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SITUATION_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATIC_ANALYSIS_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_MODAL_ANALYSIS_LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    CALCULATE_CRITICAL_LOAD_FIELD_NUMBER: _ClassVar[int]
    STABILITY_ANALYSIS_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IMPERFECTION_FIELD_NUMBER: _ClassVar[int]
    IMPERFECTION_CASE_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_INITIAL_STATE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATE_CASE_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_CONSTRUCTION_STAGE_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTION_STAGE_FIELD_NUMBER: _ClassVar[int]
    CREEP_LOADING_CASE_FIELD_NUMBER: _ClassVar[int]
    SUSTAINED_LOAD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUSTAINED_LOAD_FIELD_NUMBER: _ClassVar[int]
    SWAY_LOAD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SWAY_LOAD_FIELD_NUMBER: _ClassVar[int]
    STRUCTURE_MODIFICATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STRUCTURE_MODIFICATION_FIELD_NUMBER: _ClassVar[int]
    TO_SOLVE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    LOAD_DURATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_STR_FIELD_NUMBER: _ClassVar[int]
    LOADING_START_FIELD_NUMBER: _ClassVar[int]
    TIME_BEING_INVESTIGATED_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATE_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    GEOTECHNICAL_ANALYSIS_RESET_SMALL_STRAIN_HISTORY_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_VERTICAL_LOADS_CASE_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_MODAL_ANALYSIS_FROM_LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_NORMALIZED_DISPLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_MODE_SHAPE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_RESPONSE_SPECTRUM_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_RESPONSE_SPECTRUM_SCALE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    analysis_type: LoadCombinationAnalysisType
    design_situation: int
    user_defined_name_enabled: bool
    name: str
    static_analysis_settings: int
    import_modal_analysis_load_case: int
    calculate_critical_load: bool
    stability_analysis_settings: int
    consider_imperfection: bool
    imperfection_case: int
    consider_initial_state: bool
    initial_state_case: int
    consider_construction_stage: bool
    construction_stage: int
    creep_loading_case: int
    sustained_load_enabled: bool
    sustained_load: int
    sway_load_enabled: bool
    sway_load: int
    structure_modification_enabled: bool
    structure_modification: int
    to_solve: bool
    comment: str
    load_duration: str
    items: LoadCombinationItemsTable
    combination_rule_str: str
    loading_start: float
    time_being_investigated: float
    is_generated: bool
    generating_object_info: str
    initial_state_definition_type: LoadCombinationInitialStateDefinitionType
    individual_factors_of_selected_objects_table: LoadCombinationIndividualFactorsOfSelectedObjectsTable
    geotechnical_analysis_reset_small_strain_history: bool
    pushover_vertical_loads_case: int
    pushover_modal_analysis_from_load_case: int
    pushover_direction: LoadCombinationPushoverDirection
    pushover_normalized_displacements: LoadCombinationPushoverNormalizedDisplacements
    pushover_mode_shape_number: int
    pushover_response_spectrum: int
    pushover_response_spectrum_scale_factor: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., analysis_type: _Optional[_Union[LoadCombinationAnalysisType, str]] = ..., design_situation: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., static_analysis_settings: _Optional[int] = ..., import_modal_analysis_load_case: _Optional[int] = ..., calculate_critical_load: bool = ..., stability_analysis_settings: _Optional[int] = ..., consider_imperfection: bool = ..., imperfection_case: _Optional[int] = ..., consider_initial_state: bool = ..., initial_state_case: _Optional[int] = ..., consider_construction_stage: bool = ..., construction_stage: _Optional[int] = ..., creep_loading_case: _Optional[int] = ..., sustained_load_enabled: bool = ..., sustained_load: _Optional[int] = ..., sway_load_enabled: bool = ..., sway_load: _Optional[int] = ..., structure_modification_enabled: bool = ..., structure_modification: _Optional[int] = ..., to_solve: bool = ..., comment: _Optional[str] = ..., load_duration: _Optional[str] = ..., items: _Optional[_Union[LoadCombinationItemsTable, _Mapping]] = ..., combination_rule_str: _Optional[str] = ..., loading_start: _Optional[float] = ..., time_being_investigated: _Optional[float] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., initial_state_definition_type: _Optional[_Union[LoadCombinationInitialStateDefinitionType, str]] = ..., individual_factors_of_selected_objects_table: _Optional[_Union[LoadCombinationIndividualFactorsOfSelectedObjectsTable, _Mapping]] = ..., geotechnical_analysis_reset_small_strain_history: bool = ..., pushover_vertical_loads_case: _Optional[int] = ..., pushover_modal_analysis_from_load_case: _Optional[int] = ..., pushover_direction: _Optional[_Union[LoadCombinationPushoverDirection, str]] = ..., pushover_normalized_displacements: _Optional[_Union[LoadCombinationPushoverNormalizedDisplacements, str]] = ..., pushover_mode_shape_number: _Optional[int] = ..., pushover_response_spectrum: _Optional[int] = ..., pushover_response_spectrum_scale_factor: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class LoadCombinationItemsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[LoadCombinationItemsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[LoadCombinationItemsRow, _Mapping]]] = ...) -> None: ...

class LoadCombinationItemsRow(_message.Message):
    __slots__ = ("no", "description", "factor", "load_case", "action", "is_leading", "gamma", "psi", "xi", "k_fi", "c_esl", "k_def", "psi_0", "psi_1", "psi_2", "fi", "gamma_0", "alfa", "k_f", "phi", "rho", "omega_0", "gamma_l_1", "k_creep", "gamma_n", "j_2", "omega_m", "omega_n", "d1", "d2", "shift", "amplitude_function_type", "time_diagram", "time_slip")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    IS_LEADING_FIELD_NUMBER: _ClassVar[int]
    GAMMA_FIELD_NUMBER: _ClassVar[int]
    PSI_FIELD_NUMBER: _ClassVar[int]
    XI_FIELD_NUMBER: _ClassVar[int]
    K_FI_FIELD_NUMBER: _ClassVar[int]
    C_ESL_FIELD_NUMBER: _ClassVar[int]
    K_DEF_FIELD_NUMBER: _ClassVar[int]
    PSI_0_FIELD_NUMBER: _ClassVar[int]
    PSI_1_FIELD_NUMBER: _ClassVar[int]
    PSI_2_FIELD_NUMBER: _ClassVar[int]
    FI_FIELD_NUMBER: _ClassVar[int]
    GAMMA_0_FIELD_NUMBER: _ClassVar[int]
    ALFA_FIELD_NUMBER: _ClassVar[int]
    K_F_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    RHO_FIELD_NUMBER: _ClassVar[int]
    OMEGA_0_FIELD_NUMBER: _ClassVar[int]
    GAMMA_L_1_FIELD_NUMBER: _ClassVar[int]
    K_CREEP_FIELD_NUMBER: _ClassVar[int]
    GAMMA_N_FIELD_NUMBER: _ClassVar[int]
    J_2_FIELD_NUMBER: _ClassVar[int]
    OMEGA_M_FIELD_NUMBER: _ClassVar[int]
    OMEGA_N_FIELD_NUMBER: _ClassVar[int]
    D1_FIELD_NUMBER: _ClassVar[int]
    D2_FIELD_NUMBER: _ClassVar[int]
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FUNCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_DIAGRAM_FIELD_NUMBER: _ClassVar[int]
    TIME_SLIP_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    factor: float
    load_case: int
    action: int
    is_leading: bool
    gamma: float
    psi: float
    xi: float
    k_fi: float
    c_esl: float
    k_def: float
    psi_0: float
    psi_1: float
    psi_2: float
    fi: float
    gamma_0: float
    alfa: float
    k_f: float
    phi: float
    rho: float
    omega_0: float
    gamma_l_1: float
    k_creep: float
    gamma_n: float
    j_2: float
    omega_m: float
    omega_n: float
    d1: float
    d2: float
    shift: float
    amplitude_function_type: LoadCombinationItemsAmplitudeFunctionType
    time_diagram: int
    time_slip: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., factor: _Optional[float] = ..., load_case: _Optional[int] = ..., action: _Optional[int] = ..., is_leading: bool = ..., gamma: _Optional[float] = ..., psi: _Optional[float] = ..., xi: _Optional[float] = ..., k_fi: _Optional[float] = ..., c_esl: _Optional[float] = ..., k_def: _Optional[float] = ..., psi_0: _Optional[float] = ..., psi_1: _Optional[float] = ..., psi_2: _Optional[float] = ..., fi: _Optional[float] = ..., gamma_0: _Optional[float] = ..., alfa: _Optional[float] = ..., k_f: _Optional[float] = ..., phi: _Optional[float] = ..., rho: _Optional[float] = ..., omega_0: _Optional[float] = ..., gamma_l_1: _Optional[float] = ..., k_creep: _Optional[float] = ..., gamma_n: _Optional[float] = ..., j_2: _Optional[float] = ..., omega_m: _Optional[float] = ..., omega_n: _Optional[float] = ..., d1: _Optional[float] = ..., d2: _Optional[float] = ..., shift: _Optional[float] = ..., amplitude_function_type: _Optional[_Union[LoadCombinationItemsAmplitudeFunctionType, str]] = ..., time_diagram: _Optional[int] = ..., time_slip: _Optional[float] = ...) -> None: ...

class LoadCombinationIndividualFactorsOfSelectedObjectsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[LoadCombinationIndividualFactorsOfSelectedObjectsTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[LoadCombinationIndividualFactorsOfSelectedObjectsTableRow, _Mapping]]] = ...) -> None: ...

class LoadCombinationIndividualFactorsOfSelectedObjectsTableRow(_message.Message):
    __slots__ = ("no", "description", "object_type", "object_list", "strain_type", "factor", "comment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_LIST_FIELD_NUMBER: _ClassVar[int]
    STRAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    object_type: LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType
    object_list: _containers.RepeatedScalarFieldContainer[int]
    strain_type: LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType
    factor: float
    comment: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_type: _Optional[_Union[LoadCombinationIndividualFactorsOfSelectedObjectsTableObjectType, str]] = ..., object_list: _Optional[_Iterable[int]] = ..., strain_type: _Optional[_Union[LoadCombinationIndividualFactorsOfSelectedObjectsTableStrainType, str]] = ..., factor: _Optional[float] = ..., comment: _Optional[str] = ...) -> None: ...
