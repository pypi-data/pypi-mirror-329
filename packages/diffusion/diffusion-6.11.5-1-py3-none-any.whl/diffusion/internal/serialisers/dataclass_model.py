#   Copyright (c) 2024 Push Technology Ltd., All Rights Reserved.
#
#   Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.
from __future__ import annotations
import dataclasses
import functools
import typing
from collections.abc import Hashable

from typing import Protocol

from diffusion.internal.serialisers.generic_model import GenericModel_T, GenericConfig
if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser


class DataclassConfigMixin(typing.Generic[GenericModel_T], GenericConfig[GenericModel_T]):
    @classmethod
    @functools.lru_cache(maxsize=None)
    def field_names(
            cls, modelcls: typing.Type[GenericModel_T], serialiser=None
    ) -> typing.List[str]:
        assert dataclasses.is_dataclass(modelcls)
        return [
            field.name
            for field in dataclasses.fields(modelcls)
        ]

    @classmethod
    def find_aliases(
        cls, modelcls: typing.Type[GenericModel_T], serialiser: Serialiser
    ) -> typing.Mapping[str, str]:
        assert isinstance(modelcls, Hashable)
        return cls._find_aliases(modelcls, serialiser)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _find_aliases(
        cls, modelcls: typing.Type[GenericModel_T], serialiser: Serialiser
    ) -> typing.Mapping[str, str]:
        import diffusion.internal.pydantic_compat.v1 as pydantic_v1
        pydantic_model = getattr(modelcls, "__pydantic_model__")

        if pydantic_model:
            assert issubclass(pydantic_model, pydantic_v1.BaseModel)
            result = {v.alias: k for k, v in pydantic_model.__fields__.items()}
        else:
            result = dict()
        return result


if typing.TYPE_CHECKING:
    class DataclassWithConfig(Protocol):
        class Config(DataclassConfigMixin):
            pass

