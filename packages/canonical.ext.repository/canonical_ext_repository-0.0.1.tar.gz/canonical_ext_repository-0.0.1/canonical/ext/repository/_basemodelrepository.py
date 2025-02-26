# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Iterable
from typing import TypeVar

import pydantic

from libcanonical.protocols.itransaction import ITransaction
from .protocols import IModelRepository


M = TypeVar('M', bound=pydantic.BaseModel)


class BaseModelRepository(IModelRepository[M]):

    def key(self, instance: M) -> Any:
        raise NotImplementedError

    async def get(
        self,
        key: Any,
        transaction: ITransaction | None = None
    ) -> M | None:
        raise NotImplementedError

    async def persist(
        self,
        instance: M,
        transaction: ITransaction | None = None,
        exclude: set[str] | None = None
    ) -> M:
        ...

    async def persist_many(
        self,
        objects: Iterable[M],
        transaction: ITransaction | None = None,
        batch_size: int | None = None,
        exclude: set[str] | None = None
    ) -> Iterable[M]:
        raise NotImplementedError