from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StabilityAnalysisSettingsAnalysisType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_EIGENVALUE_METHOD: _ClassVar[StabilityAnalysisSettingsAnalysisType]
    STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTALY_METHOD_WITHOUT_EIGENVALUE: _ClassVar[StabilityAnalysisSettingsAnalysisType]
    STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTALY_METHOD_WITH_EIGENVALUE: _ClassVar[StabilityAnalysisSettingsAnalysisType]
    STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTAL_METHOD_MATERIAL_PARAMETERS_REDUCTION: _ClassVar[StabilityAnalysisSettingsAnalysisType]

class StabilityAnalysisSettingsEigenvalueMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_LANCZOS: _ClassVar[StabilityAnalysisSettingsEigenvalueMethod]
    STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_ICG_ITERATION: _ClassVar[StabilityAnalysisSettingsEigenvalueMethod]
    STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_ROOTS_OF_CHARACTERISTIC_POLYNOMIAL: _ClassVar[StabilityAnalysisSettingsEigenvalueMethod]
    STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_SHIFTED_INVERSE_POWER_METHOD: _ClassVar[StabilityAnalysisSettingsEigenvalueMethod]
    STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_SUBSPACE_ITERATION: _ClassVar[StabilityAnalysisSettingsEigenvalueMethod]

class StabilityAnalysisSettingsMatrixType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STABILITY_ANALYSIS_SETTINGS_MATRIX_TYPE_STANDARD: _ClassVar[StabilityAnalysisSettingsMatrixType]
    STABILITY_ANALYSIS_SETTINGS_MATRIX_TYPE_UNIT: _ClassVar[StabilityAnalysisSettingsMatrixType]

class StabilityAnalysisSettingsStoppingOfLoadIncreasingResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_X: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_Y: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_Z: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_X: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_Y: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
    STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_Z: _ClassVar[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult]
STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_EIGENVALUE_METHOD: StabilityAnalysisSettingsAnalysisType
STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTALY_METHOD_WITHOUT_EIGENVALUE: StabilityAnalysisSettingsAnalysisType
STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTALY_METHOD_WITH_EIGENVALUE: StabilityAnalysisSettingsAnalysisType
STABILITY_ANALYSIS_SETTINGS_ANALYSIS_TYPE_INCREMENTAL_METHOD_MATERIAL_PARAMETERS_REDUCTION: StabilityAnalysisSettingsAnalysisType
STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_LANCZOS: StabilityAnalysisSettingsEigenvalueMethod
STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_ICG_ITERATION: StabilityAnalysisSettingsEigenvalueMethod
STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_ROOTS_OF_CHARACTERISTIC_POLYNOMIAL: StabilityAnalysisSettingsEigenvalueMethod
STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_SHIFTED_INVERSE_POWER_METHOD: StabilityAnalysisSettingsEigenvalueMethod
STABILITY_ANALYSIS_SETTINGS_EIGENVALUE_METHOD_SUBSPACE_ITERATION: StabilityAnalysisSettingsEigenvalueMethod
STABILITY_ANALYSIS_SETTINGS_MATRIX_TYPE_STANDARD: StabilityAnalysisSettingsMatrixType
STABILITY_ANALYSIS_SETTINGS_MATRIX_TYPE_UNIT: StabilityAnalysisSettingsMatrixType
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_X: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_Y: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_DISPLACEMENT_U_Z: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_X: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_Y: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
STABILITY_ANALYSIS_SETTINGS_STOPPING_OF_LOAD_INCREASING_RESULT_ROTATION_PHI_Z: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult

class StabilityAnalysisSettings(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "assigned_to", "analysis_type", "number_of_lowest_eigenvalues", "considered_favored_effect", "eigenvalue_method", "find_eigenvectors_beyond_critical_load_factor", "critical_load_factor", "calculate_without_loading_for_instability", "activate_minimum_initial_prestress", "minimum_initial_strain", "display_local_torsional_rotations", "local_torsional_rotations", "matrix_type", "initial_load_factor", "load_factor_increment", "refinement_of_the_last_load_increment", "maximum_number_of_load_increments", "activate_stopping_of_load_increasing", "stopping_of_load_increasing_result", "stopping_of_load_increasing_limit_result_displacement", "stopping_of_load_increasing_limit_result_rotation", "stopping_of_load_increasing_limit_node", "save_results_of_all_increments", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LOWEST_EIGENVALUES_FIELD_NUMBER: _ClassVar[int]
    CONSIDERED_FAVORED_EFFECT_FIELD_NUMBER: _ClassVar[int]
    EIGENVALUE_METHOD_FIELD_NUMBER: _ClassVar[int]
    FIND_EIGENVECTORS_BEYOND_CRITICAL_LOAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_LOAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CALCULATE_WITHOUT_LOADING_FOR_INSTABILITY_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_MINIMUM_INITIAL_PRESTRESS_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_INITIAL_STRAIN_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_LOCAL_TORSIONAL_ROTATIONS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_TORSIONAL_ROTATIONS_FIELD_NUMBER: _ClassVar[int]
    MATRIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_LOAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    LOAD_FACTOR_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    REFINEMENT_OF_THE_LAST_LOAD_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_NUMBER_OF_LOAD_INCREMENTS_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_STOPPING_OF_LOAD_INCREASING_FIELD_NUMBER: _ClassVar[int]
    STOPPING_OF_LOAD_INCREASING_RESULT_FIELD_NUMBER: _ClassVar[int]
    STOPPING_OF_LOAD_INCREASING_LIMIT_RESULT_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    STOPPING_OF_LOAD_INCREASING_LIMIT_RESULT_ROTATION_FIELD_NUMBER: _ClassVar[int]
    STOPPING_OF_LOAD_INCREASING_LIMIT_NODE_FIELD_NUMBER: _ClassVar[int]
    SAVE_RESULTS_OF_ALL_INCREMENTS_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    comment: str
    assigned_to: str
    analysis_type: StabilityAnalysisSettingsAnalysisType
    number_of_lowest_eigenvalues: int
    considered_favored_effect: bool
    eigenvalue_method: StabilityAnalysisSettingsEigenvalueMethod
    find_eigenvectors_beyond_critical_load_factor: bool
    critical_load_factor: float
    calculate_without_loading_for_instability: bool
    activate_minimum_initial_prestress: bool
    minimum_initial_strain: float
    display_local_torsional_rotations: bool
    local_torsional_rotations: float
    matrix_type: StabilityAnalysisSettingsMatrixType
    initial_load_factor: float
    load_factor_increment: float
    refinement_of_the_last_load_increment: int
    maximum_number_of_load_increments: int
    activate_stopping_of_load_increasing: bool
    stopping_of_load_increasing_result: StabilityAnalysisSettingsStoppingOfLoadIncreasingResult
    stopping_of_load_increasing_limit_result_displacement: float
    stopping_of_load_increasing_limit_result_rotation: float
    stopping_of_load_increasing_limit_node: int
    save_results_of_all_increments: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., assigned_to: _Optional[str] = ..., analysis_type: _Optional[_Union[StabilityAnalysisSettingsAnalysisType, str]] = ..., number_of_lowest_eigenvalues: _Optional[int] = ..., considered_favored_effect: bool = ..., eigenvalue_method: _Optional[_Union[StabilityAnalysisSettingsEigenvalueMethod, str]] = ..., find_eigenvectors_beyond_critical_load_factor: bool = ..., critical_load_factor: _Optional[float] = ..., calculate_without_loading_for_instability: bool = ..., activate_minimum_initial_prestress: bool = ..., minimum_initial_strain: _Optional[float] = ..., display_local_torsional_rotations: bool = ..., local_torsional_rotations: _Optional[float] = ..., matrix_type: _Optional[_Union[StabilityAnalysisSettingsMatrixType, str]] = ..., initial_load_factor: _Optional[float] = ..., load_factor_increment: _Optional[float] = ..., refinement_of_the_last_load_increment: _Optional[int] = ..., maximum_number_of_load_increments: _Optional[int] = ..., activate_stopping_of_load_increasing: bool = ..., stopping_of_load_increasing_result: _Optional[_Union[StabilityAnalysisSettingsStoppingOfLoadIncreasingResult, str]] = ..., stopping_of_load_increasing_limit_result_displacement: _Optional[float] = ..., stopping_of_load_increasing_limit_result_rotation: _Optional[float] = ..., stopping_of_load_increasing_limit_node: _Optional[int] = ..., save_results_of_all_increments: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
