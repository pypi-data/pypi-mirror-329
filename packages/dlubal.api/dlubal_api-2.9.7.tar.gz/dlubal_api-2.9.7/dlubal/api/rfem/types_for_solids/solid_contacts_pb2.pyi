from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SolidContactsPerpendicularToSurface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FULL_FORCE_TRANSMISSION: _ClassVar[SolidContactsPerpendicularToSurface]
    SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FAILURE_UNDER_COMPRESSION: _ClassVar[SolidContactsPerpendicularToSurface]
    SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FAILURE_UNDER_TENSION: _ClassVar[SolidContactsPerpendicularToSurface]

class SolidContactsParallelToSurface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_FAILURE_IF_CONTACT_PERPENDICULAR_TO_SURFACES_FAILED: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_FRICTION: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_FRICTION_LIMIT: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_SOLID: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_FULL_FORCE_TRANSMISSION: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_RIGID_FRICTION: _ClassVar[SolidContactsParallelToSurface]
    SOLID_CONTACTS_PARALLEL_TO_SURFACE_RIGID_FRICTION_LIMIT: _ClassVar[SolidContactsParallelToSurface]
SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FULL_FORCE_TRANSMISSION: SolidContactsPerpendicularToSurface
SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FAILURE_UNDER_COMPRESSION: SolidContactsPerpendicularToSurface
SOLID_CONTACTS_PERPENDICULAR_TO_SURFACE_FAILURE_UNDER_TENSION: SolidContactsPerpendicularToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_FAILURE_IF_CONTACT_PERPENDICULAR_TO_SURFACES_FAILED: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_FRICTION: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_FRICTION_LIMIT: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_ELASTIC_SOLID: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_FULL_FORCE_TRANSMISSION: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_RIGID_FRICTION: SolidContactsParallelToSurface
SOLID_CONTACTS_PARALLEL_TO_SURFACE_RIGID_FRICTION_LIMIT: SolidContactsParallelToSurface

class SolidContacts(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "solids", "perpendicular_to_surface", "parallel_to_surface", "shear_stiffness", "friction_coefficient", "limit_stress", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_FIELD_NUMBER: _ClassVar[int]
    PERPENDICULAR_TO_SURFACE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_SURFACE_FIELD_NUMBER: _ClassVar[int]
    SHEAR_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    LIMIT_STRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    comment: str
    solids: _containers.RepeatedScalarFieldContainer[int]
    perpendicular_to_surface: SolidContactsPerpendicularToSurface
    parallel_to_surface: SolidContactsParallelToSurface
    shear_stiffness: float
    friction_coefficient: float
    limit_stress: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., solids: _Optional[_Iterable[int]] = ..., perpendicular_to_surface: _Optional[_Union[SolidContactsPerpendicularToSurface, str]] = ..., parallel_to_surface: _Optional[_Union[SolidContactsParallelToSurface, str]] = ..., shear_stiffness: _Optional[float] = ..., friction_coefficient: _Optional[float] = ..., limit_stress: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
