from dlubal.api.rfem.application_pb2 import Object, ObjectList, CreateObjectListRequest
from google.protobuf.any_pb2 import Any
from google.protobuf.struct_pb2 import Value


def pack_object(object, model_id=None) -> Object:
    packed = Any()
    packed.Pack(object)

    if model_id is None:
        return Object(object=packed)

    return Object(object=packed, model_id=model_id)


def unpack_object(packed_object: Object, Type):
    result = Type()
    packed_object.object.Unpack(result)
    return result


def pack_object_list(object_list, model_id=None, return_object_id=None):
    packed_list = ObjectList()
    packed_list.objects.extend(pack_object(obj, model_id) for obj in object_list)

    if return_object_id is not None:
        return CreateObjectListRequest(objects=packed_list, return_object_id=return_object_id)

    return packed_list


def unpack_object_list(packed_object_list: ObjectList, type_lst: list):
    unpacked_list = []

    for i, object in enumerate(packed_object_list.objects):
        unpacked_list.append(unpack_object(object, type_lst[i]))

    return unpacked_list


def get_internal_value(value: Value):
    '''
    Get the internal value stored in a generic Value object
    '''
    return getattr(value, value.WhichOneof('kind'))
