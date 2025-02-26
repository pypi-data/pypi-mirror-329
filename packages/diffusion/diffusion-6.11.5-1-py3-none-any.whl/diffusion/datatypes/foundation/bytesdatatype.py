from __future__ import annotations

import typing

from diffusion.datatypes.foundation.abstract import A_T
from diffusion.datatypes.foundation.ibytesdatatype import IBytes as IBytesParent


@typing.final
class Bytes(IBytesParent):
    """
    Represents a basic, bytes-only implementation of
    [IBytes][diffusion.datatypes.foundation.ibytesdatatype.IBytes]

    Effectively a lower bound on IBytes types.
    """

    type_name: typing.ClassVar[str] = "Bytes"

    @classmethod
    def encode(cls, value: typing.Any) -> bytes:
        return value

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> typing.Any:
        return data
