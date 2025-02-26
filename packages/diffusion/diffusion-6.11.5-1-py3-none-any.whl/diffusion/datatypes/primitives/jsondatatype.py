from __future__ import annotations

import typing
from typing import Optional, Union

from .primitivedatatype import T, PrimitiveDataType

JsonTypes = Union[dict, list, str, int, float]


class JsonDataType(
    PrimitiveDataType[
        JsonTypes
    ],
    typing.Generic[T]
):
    """ JSON data type implementation. """

    type_code = 15
    type_name = "json"
    raw_types = JsonTypes.__args__  # type: ignore

    def __init__(self, value: Optional[JsonTypes]) -> None:
        super().__init__(value)
