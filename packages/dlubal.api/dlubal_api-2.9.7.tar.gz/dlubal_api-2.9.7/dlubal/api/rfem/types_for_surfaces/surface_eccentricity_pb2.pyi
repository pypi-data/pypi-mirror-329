from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceEccentricityThicknessAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_TOP: _ClassVar[SurfaceEccentricityThicknessAlignment]
    SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_BOTTOM: _ClassVar[SurfaceEccentricityThicknessAlignment]
    SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_CENTER: _ClassVar[SurfaceEccentricityThicknessAlignment]

class SurfaceEccentricityTransverseOffsetReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_NONE: _ClassVar[SurfaceEccentricityTransverseOffsetReferenceType]
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_MEMBER_SECTION: _ClassVar[SurfaceEccentricityTransverseOffsetReferenceType]
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_SURFACE_THICKNESS: _ClassVar[SurfaceEccentricityTransverseOffsetReferenceType]

class SurfaceEccentricityTransverseOffsetAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_TOP: _ClassVar[SurfaceEccentricityTransverseOffsetAlignment]
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_BOTTOM: _ClassVar[SurfaceEccentricityTransverseOffsetAlignment]
    SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_CENTER: _ClassVar[SurfaceEccentricityTransverseOffsetAlignment]
SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_TOP: SurfaceEccentricityThicknessAlignment
SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_BOTTOM: SurfaceEccentricityThicknessAlignment
SURFACE_ECCENTRICITY_THICKNESS_ALIGNMENT_CENTER: SurfaceEccentricityThicknessAlignment
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_NONE: SurfaceEccentricityTransverseOffsetReferenceType
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_MEMBER_SECTION: SurfaceEccentricityTransverseOffsetReferenceType
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_SURFACE_THICKNESS: SurfaceEccentricityTransverseOffsetReferenceType
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_TOP: SurfaceEccentricityTransverseOffsetAlignment
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_BOTTOM: SurfaceEccentricityTransverseOffsetAlignment
SURFACE_ECCENTRICITY_TRANSVERSE_OFFSET_ALIGNMENT_CENTER: SurfaceEccentricityTransverseOffsetAlignment

class SurfaceEccentricity(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "offset", "assigned_to_surfaces", "thickness_alignment", "transverse_offset_active", "transverse_offset_reference_type", "transverse_offset_reference_member", "transverse_offset_reference_surface", "transverse_offset_member_reference_node", "transverse_offset_surface_reference_node", "transverse_offset_alignment", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACES_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_MEMBER_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_SURFACE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_MEMBER_REFERENCE_NODE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_SURFACE_REFERENCE_NODE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    offset: float
    assigned_to_surfaces: _containers.RepeatedScalarFieldContainer[int]
    thickness_alignment: SurfaceEccentricityThicknessAlignment
    transverse_offset_active: bool
    transverse_offset_reference_type: SurfaceEccentricityTransverseOffsetReferenceType
    transverse_offset_reference_member: int
    transverse_offset_reference_surface: int
    transverse_offset_member_reference_node: int
    transverse_offset_surface_reference_node: int
    transverse_offset_alignment: SurfaceEccentricityTransverseOffsetAlignment
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., offset: _Optional[float] = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., thickness_alignment: _Optional[_Union[SurfaceEccentricityThicknessAlignment, str]] = ..., transverse_offset_active: bool = ..., transverse_offset_reference_type: _Optional[_Union[SurfaceEccentricityTransverseOffsetReferenceType, str]] = ..., transverse_offset_reference_member: _Optional[int] = ..., transverse_offset_reference_surface: _Optional[int] = ..., transverse_offset_member_reference_node: _Optional[int] = ..., transverse_offset_surface_reference_node: _Optional[int] = ..., transverse_offset_alignment: _Optional[_Union[SurfaceEccentricityTransverseOffsetAlignment, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
