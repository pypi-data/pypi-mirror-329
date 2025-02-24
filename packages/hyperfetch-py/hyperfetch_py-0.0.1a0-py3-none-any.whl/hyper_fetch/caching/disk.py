import asyncio
import pickle
from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiofiles

from hyper_fetch.caching.base import AsyncCacheBackend


class DiskCache(AsyncCacheBackend, ABC):
    def __init__(self, cache_dir: Path, max_size: int):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[bytes]:
        file_path = self._file_path(key)
        try:
            async with aiofiles.open(file_path, "rb") as f:
                metadata = pickle.loads(await f.read())
                if metadata["expiry"] > datetime.now().timestamp():
                    return metadata["data"]

                await self.delete(key)
        except (FileNotFoundError, pickle.PickleError):
            pass

        return None

    def _file_path(self, key: str) -> Path:
        return self.cache_dir / self.encode_key(key)

    def _purge_cache(self, requested_size: int):
        # Check and enforce size limit
        if self.max_size <= 0:
            return

        current_size = sum(f.stat().st_size for f in self.cache_dir.glob("*"))
        while current_size + requested_size > self.max_size:
            # Remove oldest file
            files = sorted(self.cache_dir.glob("*"), key=lambda x: x.stat().st_mtime)
            if not files:
                return
            files[0].unlink()
            current_size = sum(f.stat().st_size for f in self.cache_dir.glob("*"))

    async def set(self, key: str, value: bytes, ttl: Optional[int] = None) -> None:
        async with self._lock:
            self._purge_cache(len(value))

            file_path = self._file_path(key)
            metadata = {
                "data": value,
                "expiry": datetime.now().timestamp() + (ttl or 3600),
            }
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(pickle.dumps(metadata))

    async def delete(self, key: str) -> None:
        file_path = self._file_path(key)
        try:
            file_path.unlink()
        except FileNotFoundError:
            pass
