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

import copy
import typing
from typing import Iterator

from diffusion.internal.serialisers.generic_model import (
    GenericConfig,
    GenericModel,
)
from diffusion.internal.utils import _KT, _VT_co, _T_co, validate_member_arguments


class ImmutableMapping(
    typing.Generic[_KT, _VT_co], typing.Mapping[_KT, _VT_co], GenericModel
):
    _innerdict: typing.Dict[_KT, _VT_co]

    def __getitem__(self, __k: _KT) -> _VT_co:
        return self._innerdict[__k]

    @classmethod
    def __class_getitem__(
        cls, item: typing.Tuple[_KT, _VT_co]
    ) -> typing.Type[ImmutableMapping[_KT, _VT_co]]:
        return typing.cast("typing.Type[ImmutableMapping[_KT, _VT_co]]", cls)

    def __len__(self) -> int:
        return len(self._innerdict)

    def __iter__(self) -> Iterator[_T_co]:
        return typing.cast(Iterator[_T_co], iter(self._innerdict))

    @validate_member_arguments
    def __init__(self, innerdict: typing.Optional[typing.Dict[_KT, _VT_co]] = None):
        innerdict = innerdict or dict()
        self.hash = hash(tuple(innerdict.items()))
        self._innerdict = innerdict

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return repr(self._innerdict)

    @classmethod
    def create(cls, param: typing.Mapping[_KT, _VT_co]) -> typing.Mapping[_KT, _VT_co]:
        return cls(dict(copy.deepcopy(param)))

    class Config(GenericConfig["ImmutableMapping"]):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {"fetch-topic-properties": {"topic-properties": "_innerdict"}}
