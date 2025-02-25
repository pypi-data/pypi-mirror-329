from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImperfectionCaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_TYPE_UNKNOWN: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_BUCKLING_MODE: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_DYNAMIC_EIGENMODE: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_IMPERFECTION_CASES_GROUP: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_INITIAL_SWAY_VIA_TABLE: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_LOCAL_IMPERFECTIONS: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_NOTIONAL_LOADS_FROM_LOAD_CASE: _ClassVar[ImperfectionCaseType]
    IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_STATIC_DEFORMATION: _ClassVar[ImperfectionCaseType]

class ImperfectionCaseDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_X: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_NEGATIVE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_NEGATIVE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_NEGATIVE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Y: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Y_NEGATIVE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Z: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Z_NEGATIVE: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_SPATIAL: _ClassVar[ImperfectionCaseDirection]
    IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_SPATIAL_NEGATIVE: _ClassVar[ImperfectionCaseDirection]

class ImperfectionCaseDirectionForLevelDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_X: _ClassVar[ImperfectionCaseDirectionForLevelDirection]
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_XY: _ClassVar[ImperfectionCaseDirectionForLevelDirection]
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_XZ: _ClassVar[ImperfectionCaseDirectionForLevelDirection]
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_Y: _ClassVar[ImperfectionCaseDirectionForLevelDirection]
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_YZ: _ClassVar[ImperfectionCaseDirectionForLevelDirection]
    IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_Z: _ClassVar[ImperfectionCaseDirectionForLevelDirection]

class ImperfectionCaseSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_SOURCE_OWN_LOAD_CASE_OR_COMBINATION: _ClassVar[ImperfectionCaseSource]
    IMPERFECTION_CASE_SOURCE_AUTOMATICALLY: _ClassVar[ImperfectionCaseSource]
    IMPERFECTION_CASE_SOURCE_LOAD_CASE: _ClassVar[ImperfectionCaseSource]
    IMPERFECTION_CASE_SOURCE_LOAD_COMBINATION: _ClassVar[ImperfectionCaseSource]

class ImperfectionCaseMagnitudeAssignmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_MAGNITUDE_ASSIGNMENT_TYPE_LOCATION_WITH_LARGEST_DISPLACEMENT: _ClassVar[ImperfectionCaseMagnitudeAssignmentType]
    IMPERFECTION_CASE_MAGNITUDE_ASSIGNMENT_TYPE_SPECIFIC_NODE: _ClassVar[ImperfectionCaseMagnitudeAssignmentType]

class ImperfectionCaseImperfectionCasesItemsOperatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_OR: _ClassVar[ImperfectionCaseImperfectionCasesItemsOperatorType]
    IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_AND: _ClassVar[ImperfectionCaseImperfectionCasesItemsOperatorType]
    IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_NONE: _ClassVar[ImperfectionCaseImperfectionCasesItemsOperatorType]
IMPERFECTION_CASE_TYPE_UNKNOWN: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_BUCKLING_MODE: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_DYNAMIC_EIGENMODE: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_IMPERFECTION_CASES_GROUP: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_INITIAL_SWAY_VIA_TABLE: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_LOCAL_IMPERFECTIONS: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_NOTIONAL_LOADS_FROM_LOAD_CASE: ImperfectionCaseType
IMPERFECTION_CASE_TYPE_IMPERFECTION_TYPE_STATIC_DEFORMATION: ImperfectionCaseType
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_X: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Y: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Y_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Z: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_LOCAL_Z_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_SPATIAL: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_IMPERFECTION_CASE_DIRECTION_SPATIAL_NEGATIVE: ImperfectionCaseDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_X: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_XY: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_XZ: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_Y: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_YZ: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_DIRECTION_FOR_LEVEL_DIRECTION_ALONG_Z: ImperfectionCaseDirectionForLevelDirection
IMPERFECTION_CASE_SOURCE_OWN_LOAD_CASE_OR_COMBINATION: ImperfectionCaseSource
IMPERFECTION_CASE_SOURCE_AUTOMATICALLY: ImperfectionCaseSource
IMPERFECTION_CASE_SOURCE_LOAD_CASE: ImperfectionCaseSource
IMPERFECTION_CASE_SOURCE_LOAD_COMBINATION: ImperfectionCaseSource
IMPERFECTION_CASE_MAGNITUDE_ASSIGNMENT_TYPE_LOCATION_WITH_LARGEST_DISPLACEMENT: ImperfectionCaseMagnitudeAssignmentType
IMPERFECTION_CASE_MAGNITUDE_ASSIGNMENT_TYPE_SPECIFIC_NODE: ImperfectionCaseMagnitudeAssignmentType
IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_OR: ImperfectionCaseImperfectionCasesItemsOperatorType
IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_AND: ImperfectionCaseImperfectionCasesItemsOperatorType
IMPERFECTION_CASE_IMPERFECTION_CASES_ITEMS_OPERATOR_TYPE_OPERATOR_NONE: ImperfectionCaseImperfectionCasesItemsOperatorType

class ImperfectionCase(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "assigned_to_load_cases", "assigned_to_load_combinations", "is_active", "assign_to_combinations_without_assigned_imperfection_case", "direction", "direction_for_level_direction", "coordinate_system", "load_case_for_notional_loads", "sway_coefficients_reciprocal", "level_imperfections", "source", "shape_from_load_case", "shape_from_load_combination", "buckling_shape", "delta_zero", "magnitude_assignment_type", "reference_node", "amount_of_modes_to_investigate", "eigenmode_automatically", "imperfection_cases_items", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_LOAD_CASES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_LOAD_COMBINATIONS_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ASSIGN_TO_COMBINATIONS_WITHOUT_ASSIGNED_IMPERFECTION_CASE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FOR_LEVEL_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FOR_NOTIONAL_LOADS_FIELD_NUMBER: _ClassVar[int]
    SWAY_COEFFICIENTS_RECIPROCAL_FIELD_NUMBER: _ClassVar[int]
    LEVEL_IMPERFECTIONS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FROM_LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FROM_LOAD_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    BUCKLING_SHAPE_FIELD_NUMBER: _ClassVar[int]
    DELTA_ZERO_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_ASSIGNMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_NODE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_OF_MODES_TO_INVESTIGATE_FIELD_NUMBER: _ClassVar[int]
    EIGENMODE_AUTOMATICALLY_FIELD_NUMBER: _ClassVar[int]
    IMPERFECTION_CASES_ITEMS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: ImperfectionCaseType
    user_defined_name_enabled: bool
    name: str
    assigned_to_load_cases: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_load_combinations: _containers.RepeatedScalarFieldContainer[int]
    is_active: bool
    assign_to_combinations_without_assigned_imperfection_case: bool
    direction: ImperfectionCaseDirection
    direction_for_level_direction: ImperfectionCaseDirectionForLevelDirection
    coordinate_system: int
    load_case_for_notional_loads: int
    sway_coefficients_reciprocal: bool
    level_imperfections: ImperfectionCaseLevelImperfectionsTable
    source: ImperfectionCaseSource
    shape_from_load_case: int
    shape_from_load_combination: int
    buckling_shape: int
    delta_zero: float
    magnitude_assignment_type: ImperfectionCaseMagnitudeAssignmentType
    reference_node: int
    amount_of_modes_to_investigate: int
    eigenmode_automatically: bool
    imperfection_cases_items: ImperfectionCaseImperfectionCasesItemsTable
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[ImperfectionCaseType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_load_cases: _Optional[_Iterable[int]] = ..., assigned_to_load_combinations: _Optional[_Iterable[int]] = ..., is_active: bool = ..., assign_to_combinations_without_assigned_imperfection_case: bool = ..., direction: _Optional[_Union[ImperfectionCaseDirection, str]] = ..., direction_for_level_direction: _Optional[_Union[ImperfectionCaseDirectionForLevelDirection, str]] = ..., coordinate_system: _Optional[int] = ..., load_case_for_notional_loads: _Optional[int] = ..., sway_coefficients_reciprocal: bool = ..., level_imperfections: _Optional[_Union[ImperfectionCaseLevelImperfectionsTable, _Mapping]] = ..., source: _Optional[_Union[ImperfectionCaseSource, str]] = ..., shape_from_load_case: _Optional[int] = ..., shape_from_load_combination: _Optional[int] = ..., buckling_shape: _Optional[int] = ..., delta_zero: _Optional[float] = ..., magnitude_assignment_type: _Optional[_Union[ImperfectionCaseMagnitudeAssignmentType, str]] = ..., reference_node: _Optional[int] = ..., amount_of_modes_to_investigate: _Optional[int] = ..., eigenmode_automatically: bool = ..., imperfection_cases_items: _Optional[_Union[ImperfectionCaseImperfectionCasesItemsTable, _Mapping]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class ImperfectionCaseLevelImperfectionsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ImperfectionCaseLevelImperfectionsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ImperfectionCaseLevelImperfectionsRow, _Mapping]]] = ...) -> None: ...

class ImperfectionCaseLevelImperfectionsRow(_message.Message):
    __slots__ = ("no", "description", "level", "e_1", "theta_1", "e_2", "theta_2", "comment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    E_1_FIELD_NUMBER: _ClassVar[int]
    THETA_1_FIELD_NUMBER: _ClassVar[int]
    E_2_FIELD_NUMBER: _ClassVar[int]
    THETA_2_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    level: float
    e_1: float
    theta_1: float
    e_2: float
    theta_2: float
    comment: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., level: _Optional[float] = ..., e_1: _Optional[float] = ..., theta_1: _Optional[float] = ..., e_2: _Optional[float] = ..., theta_2: _Optional[float] = ..., comment: _Optional[str] = ...) -> None: ...

class ImperfectionCaseImperfectionCasesItemsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ImperfectionCaseImperfectionCasesItemsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ImperfectionCaseImperfectionCasesItemsRow, _Mapping]]] = ...) -> None: ...

class ImperfectionCaseImperfectionCasesItemsRow(_message.Message):
    __slots__ = ("no", "description", "name", "factor", "operator_type", "comment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    name: int
    factor: float
    operator_type: ImperfectionCaseImperfectionCasesItemsOperatorType
    comment: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., name: _Optional[int] = ..., factor: _Optional[float] = ..., operator_type: _Optional[_Union[ImperfectionCaseImperfectionCasesItemsOperatorType, str]] = ..., comment: _Optional[str] = ...) -> None: ...
