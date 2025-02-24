import hashlib
from abc import ABC, abstractmethod
from typing import Optional


class CacheBackendBase(ABC):
    @staticmethod
    def encode_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()


class AsyncCacheBackend(CacheBackendBase):
    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]: ...

    @abstractmethod
    async def set(self, key: str, value: bytes, ttl: Optional[int] = None) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def clear(self) -> None: ...


class SyncCacheBackend(CacheBackendBase):
    @abstractmethod
    def get(self, key: str) -> Optional[bytes]: ...

    @abstractmethod
    def set(self, key: str, value: bytes, ttl: Optional[int] = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...
