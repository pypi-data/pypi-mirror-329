from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WindSimulationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIND_SIMULATION_TYPE_UNKNOWN: _ClassVar[WindSimulationType]
    WIND_SIMULATION_TYPE_STANDARD: _ClassVar[WindSimulationType]

class WindSimulationWindDirectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIND_SIMULATION_WIND_DIRECTION_TYPE_UNIFORM: _ClassVar[WindSimulationWindDirectionType]
    WIND_SIMULATION_WIND_DIRECTION_TYPE_USER_DEFINED: _ClassVar[WindSimulationWindDirectionType]

class WindSimulationInitialStateDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_FINAL_STATE: _ClassVar[WindSimulationInitialStateDefinitionType]
    WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STIFFNESS: _ClassVar[WindSimulationInitialStateDefinitionType]
    WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS: _ClassVar[WindSimulationInitialStateDefinitionType]
    WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS_WITH_USER_DEFINED_FACTORS: _ClassVar[WindSimulationInitialStateDefinitionType]

class WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_HINGE: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER_HINGE: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType]

class WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALL: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_X: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Y: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Z: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_X: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Y: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
    WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Z: _ClassVar[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType]
WIND_SIMULATION_TYPE_UNKNOWN: WindSimulationType
WIND_SIMULATION_TYPE_STANDARD: WindSimulationType
WIND_SIMULATION_WIND_DIRECTION_TYPE_UNIFORM: WindSimulationWindDirectionType
WIND_SIMULATION_WIND_DIRECTION_TYPE_USER_DEFINED: WindSimulationWindDirectionType
WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_FINAL_STATE: WindSimulationInitialStateDefinitionType
WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STIFFNESS: WindSimulationInitialStateDefinitionType
WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS: WindSimulationInitialStateDefinitionType
WIND_SIMULATION_INITIAL_STATE_DEFINITION_TYPE_STRAINS_WITH_USER_DEFINED_FACTORS: WindSimulationInitialStateDefinitionType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_UNKNOWN: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_HINGE: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_LINE_WITH_SUPPORT: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_MEMBER_HINGE: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_NODE_WITH_SUPPORT: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SOLID: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_OBJECT_TYPE_SURFACE: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALL: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_X: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Y: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_ALONG_Z: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_X: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Y: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
WIND_SIMULATION_INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_STRAIN_TYPE_AROUND_Z: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType

class WindSimulation(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "active", "wind_profile", "wind_simulation_analysis_settings", "wind_direction_type", "uniform_wind_direction_step", "uniform_wind_direction_range_start", "uniform_wind_direction_range_end", "user_defined_list_of_wind_directions", "generate_into_load_cases", "consider_initial_state", "initial_state_case", "initial_state_definition_type", "individual_factors_of_selected_objects_table", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    WIND_PROFILE_FIELD_NUMBER: _ClassVar[int]
    WIND_SIMULATION_ANALYSIS_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    WIND_DIRECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_WIND_DIRECTION_STEP_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_WIND_DIRECTION_RANGE_START_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_WIND_DIRECTION_RANGE_END_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_LIST_OF_WIND_DIRECTIONS_FIELD_NUMBER: _ClassVar[int]
    GENERATE_INTO_LOAD_CASES_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_INITIAL_STATE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATE_CASE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATE_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_FACTORS_OF_SELECTED_OBJECTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: WindSimulationType
    user_defined_name_enabled: bool
    name: str
    active: bool
    wind_profile: int
    wind_simulation_analysis_settings: int
    wind_direction_type: WindSimulationWindDirectionType
    uniform_wind_direction_step: float
    uniform_wind_direction_range_start: float
    uniform_wind_direction_range_end: float
    user_defined_list_of_wind_directions: _containers.RepeatedScalarFieldContainer[int]
    generate_into_load_cases: WindSimulationGenerateIntoLoadCasesTable
    consider_initial_state: bool
    initial_state_case: int
    initial_state_definition_type: WindSimulationInitialStateDefinitionType
    individual_factors_of_selected_objects_table: WindSimulationIndividualFactorsOfSelectedObjectsTable
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[WindSimulationType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., active: bool = ..., wind_profile: _Optional[int] = ..., wind_simulation_analysis_settings: _Optional[int] = ..., wind_direction_type: _Optional[_Union[WindSimulationWindDirectionType, str]] = ..., uniform_wind_direction_step: _Optional[float] = ..., uniform_wind_direction_range_start: _Optional[float] = ..., uniform_wind_direction_range_end: _Optional[float] = ..., user_defined_list_of_wind_directions: _Optional[_Iterable[int]] = ..., generate_into_load_cases: _Optional[_Union[WindSimulationGenerateIntoLoadCasesTable, _Mapping]] = ..., consider_initial_state: bool = ..., initial_state_case: _Optional[int] = ..., initial_state_definition_type: _Optional[_Union[WindSimulationInitialStateDefinitionType, str]] = ..., individual_factors_of_selected_objects_table: _Optional[_Union[WindSimulationIndividualFactorsOfSelectedObjectsTable, _Mapping]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class WindSimulationGenerateIntoLoadCasesTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[WindSimulationGenerateIntoLoadCasesRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[WindSimulationGenerateIntoLoadCasesRow, _Mapping]]] = ...) -> None: ...

class WindSimulationGenerateIntoLoadCasesRow(_message.Message):
    __slots__ = ("no", "description", "direction", "load_case")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    direction: float
    load_case: int
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., direction: _Optional[float] = ..., load_case: _Optional[int] = ...) -> None: ...

class WindSimulationIndividualFactorsOfSelectedObjectsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[WindSimulationIndividualFactorsOfSelectedObjectsTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[WindSimulationIndividualFactorsOfSelectedObjectsTableRow, _Mapping]]] = ...) -> None: ...

class WindSimulationIndividualFactorsOfSelectedObjectsTableRow(_message.Message):
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
    object_type: WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType
    object_list: _containers.RepeatedScalarFieldContainer[int]
    strain_type: WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType
    factor: float
    comment: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_type: _Optional[_Union[WindSimulationIndividualFactorsOfSelectedObjectsTableObjectType, str]] = ..., object_list: _Optional[_Iterable[int]] = ..., strain_type: _Optional[_Union[WindSimulationIndividualFactorsOfSelectedObjectsTableStrainType, str]] = ..., factor: _Optional[float] = ..., comment: _Optional[str] = ...) -> None: ...
