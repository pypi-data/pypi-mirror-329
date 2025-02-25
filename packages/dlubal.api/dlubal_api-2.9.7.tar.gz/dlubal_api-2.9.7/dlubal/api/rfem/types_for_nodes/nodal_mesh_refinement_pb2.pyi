from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodalMeshRefinementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NODAL_MESH_REFINEMENT_TYPE_UNKNOWN: _ClassVar[NodalMeshRefinementType]
    NODAL_MESH_REFINEMENT_TYPE_CIRCULAR: _ClassVar[NodalMeshRefinementType]
    NODAL_MESH_REFINEMENT_TYPE_RECTANGULAR: _ClassVar[NodalMeshRefinementType]

class NodalMeshRefinementCircularLengthArrangement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_RADIAL: _ClassVar[NodalMeshRefinementCircularLengthArrangement]
    NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_COMBINED: _ClassVar[NodalMeshRefinementCircularLengthArrangement]
    NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_GRADUALLY: _ClassVar[NodalMeshRefinementCircularLengthArrangement]
NODAL_MESH_REFINEMENT_TYPE_UNKNOWN: NodalMeshRefinementType
NODAL_MESH_REFINEMENT_TYPE_CIRCULAR: NodalMeshRefinementType
NODAL_MESH_REFINEMENT_TYPE_RECTANGULAR: NodalMeshRefinementType
NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_RADIAL: NodalMeshRefinementCircularLengthArrangement
NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_COMBINED: NodalMeshRefinementCircularLengthArrangement
NODAL_MESH_REFINEMENT_CIRCULAR_LENGTH_ARRANGEMENT_GRADUALLY: NodalMeshRefinementCircularLengthArrangement

class NodalMeshRefinement(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "comment", "nodes", "circular_radius", "circular_target_inner_length", "circular_target_outer_length", "circular_length_arrangement", "rectangular_side", "rectangular_target_inner_length", "is_generated", "generating_object_info", "apply_only_on_selected_surfaces", "selected_surfaces", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    CIRCULAR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    CIRCULAR_TARGET_INNER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    CIRCULAR_TARGET_OUTER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    CIRCULAR_LENGTH_ARRANGEMENT_FIELD_NUMBER: _ClassVar[int]
    RECTANGULAR_SIDE_FIELD_NUMBER: _ClassVar[int]
    RECTANGULAR_TARGET_INNER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    APPLY_ONLY_ON_SELECTED_SURFACES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: NodalMeshRefinementType
    user_defined_name_enabled: bool
    name: str
    comment: str
    nodes: _containers.RepeatedScalarFieldContainer[int]
    circular_radius: float
    circular_target_inner_length: float
    circular_target_outer_length: float
    circular_length_arrangement: NodalMeshRefinementCircularLengthArrangement
    rectangular_side: float
    rectangular_target_inner_length: float
    is_generated: bool
    generating_object_info: str
    apply_only_on_selected_surfaces: bool
    selected_surfaces: _containers.RepeatedScalarFieldContainer[int]
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[NodalMeshRefinementType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., nodes: _Optional[_Iterable[int]] = ..., circular_radius: _Optional[float] = ..., circular_target_inner_length: _Optional[float] = ..., circular_target_outer_length: _Optional[float] = ..., circular_length_arrangement: _Optional[_Union[NodalMeshRefinementCircularLengthArrangement, str]] = ..., rectangular_side: _Optional[float] = ..., rectangular_target_inner_length: _Optional[float] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., apply_only_on_selected_surfaces: bool = ..., selected_surfaces: _Optional[_Iterable[int]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
