import asyncio
from abc import ABC
from datetime import datetime
from typing import Optional, Dict

from hyper_fetch.caching.base import AsyncCacheBackend


class MemoryCache(AsyncCacheBackend, ABC):
    def __init__(self, max_size: int):
        self.cache: Dict[str, tuple[bytes, float]] = {}
        self.max_size = max_size
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[bytes]:
        key = self.encode_key(key)
        async with self._lock:
            if key in self.cache:
                data, expiry = self.cache[key]
                if expiry > datetime.now().timestamp():
                    return data

                del self.cache[key]

            return None

    async def set(self, key: str, value: bytes, ttl: Optional[int] = None) -> None:
        key = self.encode_key(key)
        async with self._lock:
            while (
                sum(len(v[0]) for v in self.cache.values()) + len(value) > self.max_size
            ):
                if not self.cache:
                    return
                # Remove oldest item
                oldest_key = min(self.cache.items(), key=lambda x: x[1][1])[0]
                del self.cache[oldest_key]

            expiry = datetime.now().timestamp() + (ttl or 3600)
            self.cache[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        key = self.encode_key(key)
        async with self._lock:
            self.cache.pop(key, None)
