from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceSetImperfectionDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_IMPERFECTION_DEFINITION_TYPE_RELATIVE: _ClassVar[SurfaceSetImperfectionDefinitionType]
    SURFACE_SET_IMPERFECTION_DEFINITION_TYPE_ABSOLUTE: _ClassVar[SurfaceSetImperfectionDefinitionType]

class SurfaceSetImperfectionImperfectionDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_UNKNOWN: _ClassVar[SurfaceSetImperfectionImperfectionDirection]
    SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_LOCAL_Z: _ClassVar[SurfaceSetImperfectionImperfectionDirection]
    SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_LOCAL_Z_NEGATIVE: _ClassVar[SurfaceSetImperfectionImperfectionDirection]
SURFACE_SET_IMPERFECTION_DEFINITION_TYPE_RELATIVE: SurfaceSetImperfectionDefinitionType
SURFACE_SET_IMPERFECTION_DEFINITION_TYPE_ABSOLUTE: SurfaceSetImperfectionDefinitionType
SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_UNKNOWN: SurfaceSetImperfectionImperfectionDirection
SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_LOCAL_Z: SurfaceSetImperfectionImperfectionDirection
SURFACE_SET_IMPERFECTION_IMPERFECTION_DIRECTION_LOCAL_Z_NEGATIVE: SurfaceSetImperfectionImperfectionDirection

class SurfaceSetImperfection(_message.Message):
    __slots__ = ("no", "definition_type", "imperfection_case", "imperfection_direction", "initial_bow", "initial_bow_relative", "parameters", "reference_length", "surface_sets", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMPERFECTION_CASE_FIELD_NUMBER: _ClassVar[int]
    IMPERFECTION_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INITIAL_BOW_FIELD_NUMBER: _ClassVar[int]
    INITIAL_BOW_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SURFACE_SETS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    definition_type: SurfaceSetImperfectionDefinitionType
    imperfection_case: int
    imperfection_direction: SurfaceSetImperfectionImperfectionDirection
    initial_bow: float
    initial_bow_relative: float
    parameters: _containers.RepeatedScalarFieldContainer[int]
    reference_length: float
    surface_sets: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., definition_type: _Optional[_Union[SurfaceSetImperfectionDefinitionType, str]] = ..., imperfection_case: _Optional[int] = ..., imperfection_direction: _Optional[_Union[SurfaceSetImperfectionImperfectionDirection, str]] = ..., initial_bow: _Optional[float] = ..., initial_bow_relative: _Optional[float] = ..., parameters: _Optional[_Iterable[int]] = ..., reference_length: _Optional[float] = ..., surface_sets: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
