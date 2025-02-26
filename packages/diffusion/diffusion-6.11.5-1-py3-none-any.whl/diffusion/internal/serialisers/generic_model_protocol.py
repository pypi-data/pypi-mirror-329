#  Copyright (c) 2024 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import typing_extensions as typing
from typing import Optional

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser
    from diffusion.internal.services import ServiceValue


GenericModel_Args_T = typing.ParamSpec("GenericModel_Args_T")
GenericModelProtocol_T = typing.TypeVar("GenericModelProtocol_T", bound="GenericModelProtocol")


@typing.runtime_checkable
class GenericModelProtocol(typing.Protocol[GenericModel_Args_T]):
    class Config(typing.Protocol[GenericModelProtocol_T]):
        @classmethod
        def from_service_value(
                cls,
                modelcls: typing.Type[GenericModelProtocol_T],
                item: ServiceValue,
        ) -> GenericModelProtocol_T:
            raise NotImplementedError()

        @classmethod
        def as_service_value(
                cls: typing.Type[GenericModelProtocol.Config[GenericModelProtocol_T]],
                item: GenericModelProtocol_T,
                serialiser: Optional[Serialiser] = None,
        ) -> ServiceValue:
            raise NotImplementedError()

        @classmethod
        def as_tuple(
                cls, item: GenericModelProtocol_T, serialiser: Optional[Serialiser] = None
        ) -> typing.Tuple[typing.Any, ...]:
            raise NotImplementedError()

        @classmethod
        def from_tuple(
                cls,
                modelcls: typing.Type[GenericModelProtocol_T],
                tp: typing.Tuple[typing.Any, ...],
                serialiser: Optional[Serialiser] = None,
        ) -> GenericModelProtocol_T:
            raise NotImplementedError()

    @classmethod
    def from_fields(
        cls: typing.Type[GenericModelProtocol[GenericModel_Args_T]],
        *args: GenericModel_Args_T.args,
        **kwargs: GenericModel_Args_T.kwargs
    ) -> GenericModelProtocol[GenericModel_Args_T]:
        ...
