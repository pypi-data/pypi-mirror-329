from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResultCombinationCombinationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_COMBINATION_TYPE_GENERAL: _ClassVar[ResultCombinationCombinationType]
    RESULT_COMBINATION_COMBINATION_TYPE_ENVELOPE_PERMANENT: _ClassVar[ResultCombinationCombinationType]
    RESULT_COMBINATION_COMBINATION_TYPE_ENVELOPE_TRANSIENT: _ClassVar[ResultCombinationCombinationType]
    RESULT_COMBINATION_COMBINATION_TYPE_SUPERPOSITION: _ClassVar[ResultCombinationCombinationType]

class ResultCombinationSrssExtremeValueSign(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_POSITIVE_OR_NEGATIVE: _ClassVar[ResultCombinationSrssExtremeValueSign]
    RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_ACCORDING_TO_LC_OR_CO: _ClassVar[ResultCombinationSrssExtremeValueSign]
    RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_NEGATIVE: _ClassVar[ResultCombinationSrssExtremeValueSign]
    RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_POSITIVE: _ClassVar[ResultCombinationSrssExtremeValueSign]

class ResultCombinationItemsOperatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_OR: _ClassVar[ResultCombinationItemsOperatorType]
    RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_AND: _ClassVar[ResultCombinationItemsOperatorType]
    RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_NONE: _ClassVar[ResultCombinationItemsOperatorType]

class ResultCombinationItemsCaseObjectSubResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_FINAL_STATE: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_ALL: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_SUB_RESULT_ID: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_ABSOLUTE_SUM: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_X: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_X_WITH_MODE_SHAPE: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Y: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Y_WITH_MODE_SHAPE: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Z: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Z_WITH_MODE_SHAPE: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUMS_ENVELOPE: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_X: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_Y: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_Z: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SRSS: _ClassVar[ResultCombinationItemsCaseObjectSubResultType]

class ResultCombinationItemsCaseObjectLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_LOAD_TYPE_TRANSIENT: _ClassVar[ResultCombinationItemsCaseObjectLoadType]
    RESULT_COMBINATION_ITEMS_CASE_OBJECT_LOAD_TYPE_PERMANENT: _ClassVar[ResultCombinationItemsCaseObjectLoadType]

class ResultCombinationItemsGroupLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_COMBINATION_ITEMS_GROUP_LOAD_TYPE_TRANSIENT: _ClassVar[ResultCombinationItemsGroupLoadType]
    RESULT_COMBINATION_ITEMS_GROUP_LOAD_TYPE_PERMANENT: _ClassVar[ResultCombinationItemsGroupLoadType]
RESULT_COMBINATION_COMBINATION_TYPE_GENERAL: ResultCombinationCombinationType
RESULT_COMBINATION_COMBINATION_TYPE_ENVELOPE_PERMANENT: ResultCombinationCombinationType
RESULT_COMBINATION_COMBINATION_TYPE_ENVELOPE_TRANSIENT: ResultCombinationCombinationType
RESULT_COMBINATION_COMBINATION_TYPE_SUPERPOSITION: ResultCombinationCombinationType
RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_POSITIVE_OR_NEGATIVE: ResultCombinationSrssExtremeValueSign
RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_ACCORDING_TO_LC_OR_CO: ResultCombinationSrssExtremeValueSign
RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_NEGATIVE: ResultCombinationSrssExtremeValueSign
RESULT_COMBINATION_SRSS_EXTREME_VALUE_SIGN_POSITIVE: ResultCombinationSrssExtremeValueSign
RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_OR: ResultCombinationItemsOperatorType
RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_AND: ResultCombinationItemsOperatorType
RESULT_COMBINATION_ITEMS_OPERATOR_TYPE_NONE: ResultCombinationItemsOperatorType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_FINAL_STATE: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_ALL: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_INCREMENTAL_SUB_RESULT_ID: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_ABSOLUTE_SUM: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_X: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_X_WITH_MODE_SHAPE: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Y: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Y_WITH_MODE_SHAPE: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Z: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_DIRECTION_Z_WITH_MODE_SHAPE: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUMS_ENVELOPE: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_X: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_Y: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SCALED_SUM_FULL_Z: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_SUB_RESULT_TYPE_SUB_RESULT_SPECTRAL_ANALYSIS_SRSS: ResultCombinationItemsCaseObjectSubResultType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_LOAD_TYPE_TRANSIENT: ResultCombinationItemsCaseObjectLoadType
RESULT_COMBINATION_ITEMS_CASE_OBJECT_LOAD_TYPE_PERMANENT: ResultCombinationItemsCaseObjectLoadType
RESULT_COMBINATION_ITEMS_GROUP_LOAD_TYPE_TRANSIENT: ResultCombinationItemsGroupLoadType
RESULT_COMBINATION_ITEMS_GROUP_LOAD_TYPE_PERMANENT: ResultCombinationItemsGroupLoadType

class ResultCombination(_message.Message):
    __slots__ = ("no", "design_situation", "user_defined_name_enabled", "name", "to_solve", "comment", "combination_type", "srss_combination", "srss_extreme_value_sign", "srss_use_equivalent_linear_combination", "srss_according_load_case_or_combination", "items", "combination_rule_str", "generate_subcombinations", "load_duration", "is_generated", "consider_construction_stage", "consider_construction_stage_active", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SITUATION_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TO_SOLVE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SRSS_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    SRSS_EXTREME_VALUE_SIGN_FIELD_NUMBER: _ClassVar[int]
    SRSS_USE_EQUIVALENT_LINEAR_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    SRSS_ACCORDING_LOAD_CASE_OR_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_STR_FIELD_NUMBER: _ClassVar[int]
    GENERATE_SUBCOMBINATIONS_FIELD_NUMBER: _ClassVar[int]
    LOAD_DURATION_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_CONSTRUCTION_STAGE_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_CONSTRUCTION_STAGE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    design_situation: int
    user_defined_name_enabled: bool
    name: str
    to_solve: bool
    comment: str
    combination_type: ResultCombinationCombinationType
    srss_combination: bool
    srss_extreme_value_sign: ResultCombinationSrssExtremeValueSign
    srss_use_equivalent_linear_combination: bool
    srss_according_load_case_or_combination: int
    items: ResultCombinationItemsTable
    combination_rule_str: str
    generate_subcombinations: bool
    load_duration: str
    is_generated: bool
    consider_construction_stage: int
    consider_construction_stage_active: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., design_situation: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., to_solve: bool = ..., comment: _Optional[str] = ..., combination_type: _Optional[_Union[ResultCombinationCombinationType, str]] = ..., srss_combination: bool = ..., srss_extreme_value_sign: _Optional[_Union[ResultCombinationSrssExtremeValueSign, str]] = ..., srss_use_equivalent_linear_combination: bool = ..., srss_according_load_case_or_combination: _Optional[int] = ..., items: _Optional[_Union[ResultCombinationItemsTable, _Mapping]] = ..., combination_rule_str: _Optional[str] = ..., generate_subcombinations: bool = ..., load_duration: _Optional[str] = ..., is_generated: bool = ..., consider_construction_stage: _Optional[int] = ..., consider_construction_stage_active: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class ResultCombinationItemsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ResultCombinationItemsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ResultCombinationItemsRow, _Mapping]]] = ...) -> None: ...

class ResultCombinationItemsRow(_message.Message):
    __slots__ = ("no", "description", "case_object_item", "operator_type", "left_parenthesis", "right_parenthesis", "group_factor", "case_object_factor", "case_object_sub_result_type", "case_object_sub_result_id", "case_object_load_type", "group_load_type", "action", "is_leading", "gamma", "psi", "xi", "k_fi", "c_esl", "k_def", "psi_0", "psi_1", "psi_2", "fi", "gamma_0", "alfa", "k_f", "phi", "rho", "omega_0", "gamma_l_1", "k_creep", "gamma_n", "j_2", "omega_m", "omega_n", "d1", "d2")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_ITEM_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    LEFT_PARENTHESIS_FIELD_NUMBER: _ClassVar[int]
    RIGHT_PARENTHESIS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_SUB_RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_SUB_RESULT_ID_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUP_LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    no: int
    description: str
    case_object_item: int
    operator_type: ResultCombinationItemsOperatorType
    left_parenthesis: bool
    right_parenthesis: bool
    group_factor: float
    case_object_factor: float
    case_object_sub_result_type: ResultCombinationItemsCaseObjectSubResultType
    case_object_sub_result_id: int
    case_object_load_type: ResultCombinationItemsCaseObjectLoadType
    group_load_type: ResultCombinationItemsGroupLoadType
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
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., case_object_item: _Optional[int] = ..., operator_type: _Optional[_Union[ResultCombinationItemsOperatorType, str]] = ..., left_parenthesis: bool = ..., right_parenthesis: bool = ..., group_factor: _Optional[float] = ..., case_object_factor: _Optional[float] = ..., case_object_sub_result_type: _Optional[_Union[ResultCombinationItemsCaseObjectSubResultType, str]] = ..., case_object_sub_result_id: _Optional[int] = ..., case_object_load_type: _Optional[_Union[ResultCombinationItemsCaseObjectLoadType, str]] = ..., group_load_type: _Optional[_Union[ResultCombinationItemsGroupLoadType, str]] = ..., action: _Optional[int] = ..., is_leading: bool = ..., gamma: _Optional[float] = ..., psi: _Optional[float] = ..., xi: _Optional[float] = ..., k_fi: _Optional[float] = ..., c_esl: _Optional[float] = ..., k_def: _Optional[float] = ..., psi_0: _Optional[float] = ..., psi_1: _Optional[float] = ..., psi_2: _Optional[float] = ..., fi: _Optional[float] = ..., gamma_0: _Optional[float] = ..., alfa: _Optional[float] = ..., k_f: _Optional[float] = ..., phi: _Optional[float] = ..., rho: _Optional[float] = ..., omega_0: _Optional[float] = ..., gamma_l_1: _Optional[float] = ..., k_creep: _Optional[float] = ..., gamma_n: _Optional[float] = ..., j_2: _Optional[float] = ..., omega_m: _Optional[float] = ..., omega_n: _Optional[float] = ..., d1: _Optional[float] = ..., d2: _Optional[float] = ...) -> None: ...
