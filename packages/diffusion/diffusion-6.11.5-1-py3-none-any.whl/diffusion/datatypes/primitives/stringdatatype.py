from .jsondatatype import JsonDataType


class StringDataType(JsonDataType[str]):
    """String data type.

    The string value is serialized as CBOR-format binary.
    """

    type_code = 17
    type_name = "string"
