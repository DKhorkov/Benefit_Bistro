from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
    