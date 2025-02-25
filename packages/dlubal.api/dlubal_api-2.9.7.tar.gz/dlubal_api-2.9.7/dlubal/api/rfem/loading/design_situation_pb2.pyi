from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DesignSituation(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "design_situation_type", "active", "comment", "is_generated", "generating_object_info", "combination_wizard", "consider_inclusive_exclusive_load_cases", "relationship_between_load_cases", "case_objects", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SITUATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_WIZARD_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_INCLUSIVE_EXCLUSIVE_LOAD_CASES_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIP_BETWEEN_LOAD_CASES_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    design_situation_type: str
    active: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    combination_wizard: int
    consider_inclusive_exclusive_load_cases: bool
    relationship_between_load_cases: int
    case_objects: DesignSituationCaseObjectsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., design_situation_type: _Optional[str] = ..., active: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., combination_wizard: _Optional[int] = ..., consider_inclusive_exclusive_load_cases: bool = ..., relationship_between_load_cases: _Optional[int] = ..., case_objects: _Optional[_Union[DesignSituationCaseObjectsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class DesignSituationCaseObjectsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[DesignSituationCaseObjectsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[DesignSituationCaseObjectsRow, _Mapping]]] = ...) -> None: ...

class DesignSituationCaseObjectsRow(_message.Message):
    __slots__ = ("no", "description", "case_object")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CASE_OBJECT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    case_object: int
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., case_object: _Optional[int] = ...) -> None: ...
