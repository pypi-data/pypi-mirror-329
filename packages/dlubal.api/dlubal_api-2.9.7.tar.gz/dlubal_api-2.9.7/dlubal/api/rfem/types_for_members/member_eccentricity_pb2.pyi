from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberEccentricitySpecificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_RELATIVE_TO_SECTION: _ClassVar[MemberEccentricitySpecificationType]
    MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_ABSOLUTE: _ClassVar[MemberEccentricitySpecificationType]
    MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_RELATIVE_AND_ABSOLUTE: _ClassVar[MemberEccentricitySpecificationType]

class MemberEccentricityHorizontalSectionAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_LEFT: _ClassVar[MemberEccentricityHorizontalSectionAlignment]
    MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_CENTER: _ClassVar[MemberEccentricityHorizontalSectionAlignment]
    MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_RIGHT: _ClassVar[MemberEccentricityHorizontalSectionAlignment]

class MemberEccentricityVerticalSectionAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_TOP: _ClassVar[MemberEccentricityVerticalSectionAlignment]
    MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_BOTTOM: _ClassVar[MemberEccentricityVerticalSectionAlignment]
    MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_CENTER: _ClassVar[MemberEccentricityVerticalSectionAlignment]

class MemberEccentricityTransverseOffsetReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_NONE: _ClassVar[MemberEccentricityTransverseOffsetReferenceType]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_MEMBER_SECTION: _ClassVar[MemberEccentricityTransverseOffsetReferenceType]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_SURFACE_THICKNESS: _ClassVar[MemberEccentricityTransverseOffsetReferenceType]

class MemberEccentricityTransverseOffsetVerticalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_TOP: _ClassVar[MemberEccentricityTransverseOffsetVerticalAlignment]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_BOTTOM: _ClassVar[MemberEccentricityTransverseOffsetVerticalAlignment]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_CENTER: _ClassVar[MemberEccentricityTransverseOffsetVerticalAlignment]

class MemberEccentricityTransverseOffsetHorizontalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_LEFT: _ClassVar[MemberEccentricityTransverseOffsetHorizontalAlignment]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_CENTER: _ClassVar[MemberEccentricityTransverseOffsetHorizontalAlignment]
    MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_RIGHT: _ClassVar[MemberEccentricityTransverseOffsetHorizontalAlignment]
MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_RELATIVE_TO_SECTION: MemberEccentricitySpecificationType
MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_ABSOLUTE: MemberEccentricitySpecificationType
MEMBER_ECCENTRICITY_SPECIFICATION_TYPE_RELATIVE_AND_ABSOLUTE: MemberEccentricitySpecificationType
MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_LEFT: MemberEccentricityHorizontalSectionAlignment
MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_CENTER: MemberEccentricityHorizontalSectionAlignment
MEMBER_ECCENTRICITY_HORIZONTAL_SECTION_ALIGNMENT_RIGHT: MemberEccentricityHorizontalSectionAlignment
MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_TOP: MemberEccentricityVerticalSectionAlignment
MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_BOTTOM: MemberEccentricityVerticalSectionAlignment
MEMBER_ECCENTRICITY_VERTICAL_SECTION_ALIGNMENT_CENTER: MemberEccentricityVerticalSectionAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_NONE: MemberEccentricityTransverseOffsetReferenceType
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_MEMBER_SECTION: MemberEccentricityTransverseOffsetReferenceType
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_REFERENCE_TYPE_FROM_SURFACE_THICKNESS: MemberEccentricityTransverseOffsetReferenceType
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_TOP: MemberEccentricityTransverseOffsetVerticalAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_BOTTOM: MemberEccentricityTransverseOffsetVerticalAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_CENTER: MemberEccentricityTransverseOffsetVerticalAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_LEFT: MemberEccentricityTransverseOffsetHorizontalAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_CENTER: MemberEccentricityTransverseOffsetHorizontalAlignment
MEMBER_ECCENTRICITY_TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_RIGHT: MemberEccentricityTransverseOffsetHorizontalAlignment

class MemberEccentricity(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "specification_type", "coordinate_system", "offset", "offset_x", "offset_y", "offset_z", "transverse_offset_active", "axial_offset_active", "hinge_location_at_node", "horizontal_section_alignment", "vertical_section_alignment", "transverse_offset_reference_type", "transverse_offset_reference_member", "transverse_offset_reference_surface", "transverse_offset_member_reference_node", "transverse_offset_surface_reference_node", "transverse_offset_vertical_alignment", "transverse_offset_horizontal_alignment", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SPECIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Z_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    AXIAL_OFFSET_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    HINGE_LOCATION_AT_NODE_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_SECTION_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_SECTION_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_MEMBER_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_REFERENCE_SURFACE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_MEMBER_REFERENCE_NODE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_SURFACE_REFERENCE_NODE_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    TRANSVERSE_OFFSET_HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    specification_type: MemberEccentricitySpecificationType
    coordinate_system: str
    offset: _common_pb2.Vector3d
    offset_x: float
    offset_y: float
    offset_z: float
    transverse_offset_active: bool
    axial_offset_active: bool
    hinge_location_at_node: bool
    horizontal_section_alignment: MemberEccentricityHorizontalSectionAlignment
    vertical_section_alignment: MemberEccentricityVerticalSectionAlignment
    transverse_offset_reference_type: MemberEccentricityTransverseOffsetReferenceType
    transverse_offset_reference_member: int
    transverse_offset_reference_surface: int
    transverse_offset_member_reference_node: int
    transverse_offset_surface_reference_node: int
    transverse_offset_vertical_alignment: MemberEccentricityTransverseOffsetVerticalAlignment
    transverse_offset_horizontal_alignment: MemberEccentricityTransverseOffsetHorizontalAlignment
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., specification_type: _Optional[_Union[MemberEccentricitySpecificationType, str]] = ..., coordinate_system: _Optional[str] = ..., offset: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., offset_x: _Optional[float] = ..., offset_y: _Optional[float] = ..., offset_z: _Optional[float] = ..., transverse_offset_active: bool = ..., axial_offset_active: bool = ..., hinge_location_at_node: bool = ..., horizontal_section_alignment: _Optional[_Union[MemberEccentricityHorizontalSectionAlignment, str]] = ..., vertical_section_alignment: _Optional[_Union[MemberEccentricityVerticalSectionAlignment, str]] = ..., transverse_offset_reference_type: _Optional[_Union[MemberEccentricityTransverseOffsetReferenceType, str]] = ..., transverse_offset_reference_member: _Optional[int] = ..., transverse_offset_reference_surface: _Optional[int] = ..., transverse_offset_member_reference_node: _Optional[int] = ..., transverse_offset_surface_reference_node: _Optional[int] = ..., transverse_offset_vertical_alignment: _Optional[_Union[MemberEccentricityTransverseOffsetVerticalAlignment, str]] = ..., transverse_offset_horizontal_alignment: _Optional[_Union[MemberEccentricityTransverseOffsetHorizontalAlignment, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
