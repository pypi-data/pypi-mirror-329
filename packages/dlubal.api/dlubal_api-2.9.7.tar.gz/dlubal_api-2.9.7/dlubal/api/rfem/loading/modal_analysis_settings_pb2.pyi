from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModalAnalysisSettingsSolutionMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_LANCZOS: _ClassVar[ModalAnalysisSettingsSolutionMethod]
    MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL: _ClassVar[ModalAnalysisSettingsSolutionMethod]
    MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_SHIFTED_INVERSE_POWER_METHOD: _ClassVar[ModalAnalysisSettingsSolutionMethod]
    MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_SUBSPACE_ITERATION: _ClassVar[ModalAnalysisSettingsSolutionMethod]

class ModalAnalysisSettingsMassConversionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS: _ClassVar[ModalAnalysisSettingsMassConversionType]
    MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_FULL_LOADS_AS_MASS: _ClassVar[ModalAnalysisSettingsMassConversionType]
    MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS_IN_DIRECTION_OF_GRAVITY: _ClassVar[ModalAnalysisSettingsMassConversionType]

class ModalAnalysisSettingsMassMatrixType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_DIAGONAL: _ClassVar[ModalAnalysisSettingsMassMatrixType]
    MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_CONSISTENT: _ClassVar[ModalAnalysisSettingsMassMatrixType]
    MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_DIAGONAL_WITH_TORSIONAL_ELEMENTS: _ClassVar[ModalAnalysisSettingsMassMatrixType]
    MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_UNIT: _ClassVar[ModalAnalysisSettingsMassMatrixType]

class ModalAnalysisSettingsNumberOfModesMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_USER_DEFINED: _ClassVar[ModalAnalysisSettingsNumberOfModesMethod]
    MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS: _ClassVar[ModalAnalysisSettingsNumberOfModesMethod]
    MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_MAXIMUM_FREQUENCY: _ClassVar[ModalAnalysisSettingsNumberOfModesMethod]

class ModalAnalysisSettingsNeglectMasses(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_IN_ALL_FIXED_SUPPORTS: _ClassVar[ModalAnalysisSettingsNeglectMasses]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_NO_NEGLECTION: _ClassVar[ModalAnalysisSettingsNeglectMasses]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_USER_DEFINED: _ClassVar[ModalAnalysisSettingsNeglectMasses]

class ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
    MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: _ClassVar[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType]
MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_LANCZOS: ModalAnalysisSettingsSolutionMethod
MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL: ModalAnalysisSettingsSolutionMethod
MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_SHIFTED_INVERSE_POWER_METHOD: ModalAnalysisSettingsSolutionMethod
MODAL_ANALYSIS_SETTINGS_SOLUTION_METHOD_SUBSPACE_ITERATION: ModalAnalysisSettingsSolutionMethod
MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS: ModalAnalysisSettingsMassConversionType
MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_FULL_LOADS_AS_MASS: ModalAnalysisSettingsMassConversionType
MODAL_ANALYSIS_SETTINGS_MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS_IN_DIRECTION_OF_GRAVITY: ModalAnalysisSettingsMassConversionType
MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_DIAGONAL: ModalAnalysisSettingsMassMatrixType
MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_CONSISTENT: ModalAnalysisSettingsMassMatrixType
MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_DIAGONAL_WITH_TORSIONAL_ELEMENTS: ModalAnalysisSettingsMassMatrixType
MODAL_ANALYSIS_SETTINGS_MASS_MATRIX_TYPE_UNIT: ModalAnalysisSettingsMassMatrixType
MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_USER_DEFINED: ModalAnalysisSettingsNumberOfModesMethod
MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS: ModalAnalysisSettingsNumberOfModesMethod
MODAL_ANALYSIS_SETTINGS_NUMBER_OF_MODES_METHOD_MAXIMUM_FREQUENCY: ModalAnalysisSettingsNumberOfModesMethod
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_IN_ALL_FIXED_SUPPORTS: ModalAnalysisSettingsNeglectMasses
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_NO_NEGLECTION: ModalAnalysisSettingsNeglectMasses
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_USER_DEFINED: ModalAnalysisSettingsNeglectMasses
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
MODAL_ANALYSIS_SETTINGS_NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType

class ModalAnalysisSettings(_message.Message):
    __slots__ = ("no", "acting_masses_about_axis_x_enabled", "acting_masses_about_axis_y_enabled", "acting_masses_about_axis_z_enabled", "acting_masses_in_direction_x_enabled", "acting_masses_in_direction_y_enabled", "acting_masses_in_direction_z_enabled", "activate_minimum_initial_prestress", "minimum_initial_strain", "assigned_to", "comment", "solution_method", "find_eigenvectors_beyond_frequency", "frequency", "mass_conversion_type", "mass_matrix_type", "number_of_modes_method", "maxmimum_natural_frequency", "effective_modal_mass_factor", "number_of_modes", "user_defined_name_enabled", "name", "neglect_masses", "neglect_masses_of_selected_objects_table", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_MINIMUM_INITIAL_PRESTRESS_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_INITIAL_STRAIN_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    FIND_EIGENVECTORS_BEYOND_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    MASS_CONVERSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MASS_MATRIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MODES_METHOD_FIELD_NUMBER: _ClassVar[int]
    MAXMIMUM_NATURAL_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_MODAL_MASS_FACTOR_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MODES_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASSES_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    acting_masses_about_axis_x_enabled: bool
    acting_masses_about_axis_y_enabled: bool
    acting_masses_about_axis_z_enabled: bool
    acting_masses_in_direction_x_enabled: bool
    acting_masses_in_direction_y_enabled: bool
    acting_masses_in_direction_z_enabled: bool
    activate_minimum_initial_prestress: bool
    minimum_initial_strain: float
    assigned_to: str
    comment: str
    solution_method: ModalAnalysisSettingsSolutionMethod
    find_eigenvectors_beyond_frequency: bool
    frequency: float
    mass_conversion_type: ModalAnalysisSettingsMassConversionType
    mass_matrix_type: ModalAnalysisSettingsMassMatrixType
    number_of_modes_method: ModalAnalysisSettingsNumberOfModesMethod
    maxmimum_natural_frequency: float
    effective_modal_mass_factor: float
    number_of_modes: int
    user_defined_name_enabled: bool
    name: str
    neglect_masses: ModalAnalysisSettingsNeglectMasses
    neglect_masses_of_selected_objects_table: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., acting_masses_about_axis_x_enabled: bool = ..., acting_masses_about_axis_y_enabled: bool = ..., acting_masses_about_axis_z_enabled: bool = ..., acting_masses_in_direction_x_enabled: bool = ..., acting_masses_in_direction_y_enabled: bool = ..., acting_masses_in_direction_z_enabled: bool = ..., activate_minimum_initial_prestress: bool = ..., minimum_initial_strain: _Optional[float] = ..., assigned_to: _Optional[str] = ..., comment: _Optional[str] = ..., solution_method: _Optional[_Union[ModalAnalysisSettingsSolutionMethod, str]] = ..., find_eigenvectors_beyond_frequency: bool = ..., frequency: _Optional[float] = ..., mass_conversion_type: _Optional[_Union[ModalAnalysisSettingsMassConversionType, str]] = ..., mass_matrix_type: _Optional[_Union[ModalAnalysisSettingsMassMatrixType, str]] = ..., number_of_modes_method: _Optional[_Union[ModalAnalysisSettingsNumberOfModesMethod, str]] = ..., maxmimum_natural_frequency: _Optional[float] = ..., effective_modal_mass_factor: _Optional[float] = ..., number_of_modes: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., neglect_masses: _Optional[_Union[ModalAnalysisSettingsNeglectMasses, str]] = ..., neglect_masses_of_selected_objects_table: _Optional[_Union[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableRow, _Mapping]]] = ...) -> None: ...

class ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableRow(_message.Message):
    __slots__ = ("no", "description", "object_type", "object_list", "neglect_mass_component_in_direction_x_enabled", "neglect_mass_component_in_direction_y_enabled", "neglect_mass_component_in_direction_z_enabled", "neglect_mass_component_about_axis_x_enabled", "neglect_mass_component_about_axis_y_enabled", "neglect_mass_component_about_axis_z_enabled", "comment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_LIST_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_IN_DIRECTION_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_IN_DIRECTION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_IN_DIRECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_ABOUT_AXIS_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_ABOUT_AXIS_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASS_COMPONENT_ABOUT_AXIS_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    object_type: ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType
    object_list: _containers.RepeatedScalarFieldContainer[int]
    neglect_mass_component_in_direction_x_enabled: bool
    neglect_mass_component_in_direction_y_enabled: bool
    neglect_mass_component_in_direction_z_enabled: bool
    neglect_mass_component_about_axis_x_enabled: bool
    neglect_mass_component_about_axis_y_enabled: bool
    neglect_mass_component_about_axis_z_enabled: bool
    comment: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_type: _Optional[_Union[ModalAnalysisSettingsNeglectMassesOfSelectedObjectsTableObjectType, str]] = ..., object_list: _Optional[_Iterable[int]] = ..., neglect_mass_component_in_direction_x_enabled: bool = ..., neglect_mass_component_in_direction_y_enabled: bool = ..., neglect_mass_component_in_direction_z_enabled: bool = ..., neglect_mass_component_about_axis_x_enabled: bool = ..., neglect_mass_component_about_axis_y_enabled: bool = ..., neglect_mass_component_about_axis_z_enabled: bool = ..., comment: _Optional[str] = ...) -> None: ...
