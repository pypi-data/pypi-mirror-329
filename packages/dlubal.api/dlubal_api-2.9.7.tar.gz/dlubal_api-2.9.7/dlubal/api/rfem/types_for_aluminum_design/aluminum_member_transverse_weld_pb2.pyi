from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AluminumMemberTransverseWeldComponentsWeldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_WELD_TYPE_WELD_COMPONENT_TYPE_BUTT: _ClassVar[AluminumMemberTransverseWeldComponentsWeldType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_WELD_TYPE_WELD_COMPONENT_TYPE_FILLET: _ClassVar[AluminumMemberTransverseWeldComponentsWeldType]

class AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: _ClassVar[AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: _ClassVar[AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType]

class AluminumMemberTransverseWeldComponentsMethodEcOrAdmType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_EC_OR_ADM_TYPE_WELDING_METHOD_TIG: _ClassVar[AluminumMemberTransverseWeldComponentsMethodEcOrAdmType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_EC_OR_ADM_TYPE_WELDING_METHOD_MIG: _ClassVar[AluminumMemberTransverseWeldComponentsMethodEcOrAdmType]

class AluminumMemberTransverseWeldComponentsMethodGbType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_SMAW: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_FCAW: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_FCAW_S: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_GMAW: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_GTAW: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
    ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_SAW: _ClassVar[AluminumMemberTransverseWeldComponentsMethodGbType]
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_WELD_TYPE_WELD_COMPONENT_TYPE_BUTT: AluminumMemberTransverseWeldComponentsWeldType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_WELD_TYPE_WELD_COMPONENT_TYPE_FILLET: AluminumMemberTransverseWeldComponentsWeldType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_EC_OR_ADM_TYPE_WELDING_METHOD_TIG: AluminumMemberTransverseWeldComponentsMethodEcOrAdmType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_EC_OR_ADM_TYPE_WELDING_METHOD_MIG: AluminumMemberTransverseWeldComponentsMethodEcOrAdmType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_SMAW: AluminumMemberTransverseWeldComponentsMethodGbType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_FCAW: AluminumMemberTransverseWeldComponentsMethodGbType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_FCAW_S: AluminumMemberTransverseWeldComponentsMethodGbType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_GMAW: AluminumMemberTransverseWeldComponentsMethodGbType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_GTAW: AluminumMemberTransverseWeldComponentsMethodGbType
ALUMINUM_MEMBER_TRANSVERSE_WELD_COMPONENTS_METHOD_GB_TYPE_WELDING_METHOD_SAW: AluminumMemberTransverseWeldComponentsMethodGbType

class AluminumMemberTransverseWeld(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "components", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    components: AluminumMemberTransverseWeldComponentsTable
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., components: _Optional[_Union[AluminumMemberTransverseWeldComponentsTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class AluminumMemberTransverseWeldComponentsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumMemberTransverseWeldComponentsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumMemberTransverseWeldComponentsRow, _Mapping]]] = ...) -> None: ...

class AluminumMemberTransverseWeldComponentsRow(_message.Message):
    __slots__ = ("no", "description", "weld_type", "position", "multiple", "note", "multiple_number", "multiple_offset_definition_type", "multiple_offset", "size", "method_ec_or_adm_type", "method_gb_type", "number_of_heat_paths", "temperature_of_material_between_welding_cycles")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    METHOD_EC_OR_ADM_TYPE_FIELD_NUMBER: _ClassVar[int]
    METHOD_GB_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_HEAT_PATHS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_OF_MATERIAL_BETWEEN_WELDING_CYCLES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    weld_type: AluminumMemberTransverseWeldComponentsWeldType
    position: float
    multiple: bool
    note: str
    multiple_number: int
    multiple_offset_definition_type: AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType
    multiple_offset: float
    size: float
    method_ec_or_adm_type: AluminumMemberTransverseWeldComponentsMethodEcOrAdmType
    method_gb_type: AluminumMemberTransverseWeldComponentsMethodGbType
    number_of_heat_paths: int
    temperature_of_material_between_welding_cycles: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., weld_type: _Optional[_Union[AluminumMemberTransverseWeldComponentsWeldType, str]] = ..., position: _Optional[float] = ..., multiple: bool = ..., note: _Optional[str] = ..., multiple_number: _Optional[int] = ..., multiple_offset_definition_type: _Optional[_Union[AluminumMemberTransverseWeldComponentsMultipleOffsetDefinitionType, str]] = ..., multiple_offset: _Optional[float] = ..., size: _Optional[float] = ..., method_ec_or_adm_type: _Optional[_Union[AluminumMemberTransverseWeldComponentsMethodEcOrAdmType, str]] = ..., method_gb_type: _Optional[_Union[AluminumMemberTransverseWeldComponentsMethodGbType, str]] = ..., number_of_heat_paths: _Optional[int] = ..., temperature_of_material_between_welding_cycles: _Optional[float] = ...) -> None: ...
