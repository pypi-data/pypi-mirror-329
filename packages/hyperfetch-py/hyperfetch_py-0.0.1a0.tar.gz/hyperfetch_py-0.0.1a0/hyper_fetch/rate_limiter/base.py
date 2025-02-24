from abc import ABC, abstractmethod


class RateLimiter(ABC):
    @abstractmethod
    async def acquire(self) -> None: ...

    @abstractmethod
    async def release(self) -> None: ...
