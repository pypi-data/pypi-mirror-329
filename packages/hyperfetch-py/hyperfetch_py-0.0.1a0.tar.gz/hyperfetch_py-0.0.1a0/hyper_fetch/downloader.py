import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Type, Callable

import httpx

from .caching.db import SQLiteCache
from .caching.disk import DiskCache
from .caching.memory import MemoryCache
from .rate_limiter.token_bucket import TokenBucketRateLimiter
from .types import *


class AsyncDownloader:
    def __init__(
        self,
        concurrency: int = 5,
        retry_config: Optional[RetryConfig] = None,
        rate_limit_config: Optional[RateLimitConfig] = None,
        cache_config: Optional[CacheConfig] = None,
        plugins: Optional[List[Type[Plugin]]] = None,
    ):
        self.concurrency = concurrency
        self.retry_config = retry_config or RetryConfig()
        self.rate_limiter = TokenBucketRateLimiter(
            rate_limit_config.requests_per_second if rate_limit_config else 10.0,
            rate_limit_config.burst_size if rate_limit_config else 20,
        )

        # Initialize caching
        if cache_config and cache_config.enabled:
            if cache_config.storage_type == "memory":
                self.cache = MemoryCache(cache_config.max_size)
            elif cache_config.storage_type == "db":
                self.cache = SQLiteCache(Path(cache_config.cache_path or ".cache.db"))
            else:
                self.cache = DiskCache(
                    Path(cache_config.cache_path or ".cache"), cache_config.max_size
                )
        else:
            self.cache = None

        # Initialize plugins
        self.plugins = [p() for p in (plugins or [])]

        # Download queue
        self._queue: asyncio.PriorityQueue[DownloadRequest] = asyncio.PriorityQueue()
        self._active_downloads: Dict[str, asyncio.Task] = {}

        # Progress tracking
        self._progress_callbacks: List[Callable[[str, ProgressInfo], None]] = []

        self.logger = logging.getLogger(__name__)

    async def initialize(self) -> None:
        """Initialize the downloader and its plugins"""
        for plugin in self.plugins:
            await plugin.initialize()

    async def shutdown(self) -> None:
        """Cleanup and shutdown"""
        # Cancel active downloads
        for task in self._active_downloads.values():
            task.cancel()

        # Cleanup plugins
        for plugin in self.plugins:
            await plugin.cleanup()

    async def _download_chunk(
        self, client: httpx.AsyncClient, request: DownloadRequest, start: int, end: int
    ) -> bytes:
        """Download a specific chunk of a file"""
        headers = request.headers or {}
        headers["Range"] = f"bytes={start}-{end}"

        response = await client.get(
            request.url,
            headers=headers,
            timeout=request.timeout,
            cookies=request.cookies,
        )

        return response.content

    async def _process_download(self, request: DownloadRequest) -> DownloadResult:
        """Process a single download request"""
        # Check caching first
        if self.cache and not request.bypass_cache:
            cached_data = await self.cache.get(request.url)
            if cached_data:
                return DownloadResult(
                    url=request.url,
                    status_code=200,
                    headers={},
                    content=cached_data,
                    context=request.context,
                    cached=True,
                )

        # Apply plugins pre-request
        for plugin in self.plugins:
            request = await plugin.pre_request(request)

        # Rate limiting
        await self.rate_limiter.acquire()

        async with httpx.AsyncClient(
            proxy=request.proxy,
            verify=(request.ssl and request.ssl.verify),
        ) as client:
            try:
                if request.chunk_config and request.chunk_config.enabled:
                    # Get file size
                    response = await client.head(
                        request.url,
                        headers=request.headers,
                        timeout=request.timeout,
                        cookies=request.cookies,
                    )
                    total_size = int(response.headers["Content-Length"])
                    chunk_size = request.chunk_config.size
                    chunks = []

                    for start in range(0, total_size, chunk_size):
                        end = min(start + chunk_size - 1, total_size - 1)
                        chunk = await self._download_chunk(client, request, start, end)
                        chunks.append(chunk)

                        # Report progress
                        if not any(self._progress_callbacks):
                            continue

                        progress = ProgressInfo(
                            bytes_downloaded=start + len(chunk),
                            total_bytes=total_size,
                            chunk_index=len(chunks),
                            total_chunks=(total_size + chunk_size - 1) // chunk_size,
                            speed_bps=0.0,  # Calculate actual speed
                            eta_seconds=None,  # Calculate ETA
                        )

                        for callback in self._progress_callbacks:
                            callback(request.url, progress)

                    content = b"".join(chunks)
                else:
                    response = await client.get(
                        request.url,
                        headers=request.headers,
                        timeout=request.timeout,
                        cookies=request.cookies,
                    )
                    content = response.content

                # Verify checksum if provided
                calculated_checksum = None
                checksum_verified = False
                if request.verify_checksum:
                    hasher = getattr(hashlib, request.verify_method.value)()
                    hasher.update(content)
                    calculated_checksum = hasher.hexdigest()
                    checksum_verified = calculated_checksum == request.verify_checksum

                result = DownloadResult(
                    url=request.url,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    content=content,
                    context=request.context,
                    checksum=calculated_checksum if request.verify_checksum else None,
                    checksum_verified=checksum_verified,
                )

                # Cache the result if appropriate
                if self.cache and response.status_code == 200:
                    await self.cache.set(request.url, content)

                # Apply plugins post-response
                for plugin in self.plugins:
                    result = await plugin.post_response(result)

                return result

            except Exception as e:
                return DownloadResult(
                    url=request.url,
                    status_code=-1,
                    headers={},
                    content=b"",
                    context=request.context,
                    error=e,
                )

    async def download(self, request: DownloadRequest) -> DownloadResult:
        """Download a single URL"""
        return await self._process_download(request)

    async def download_many(
        self, requests: List[DownloadRequest]
    ) -> List[DownloadResult]:
        """Download multiple URLs concurrently"""
        semaphore = asyncio.Semaphore(self.concurrency)

        async def bounded_download(request: DownloadRequest) -> DownloadResult:
            async with semaphore:
                return await self._process_download(request)

        tasks = [bounded_download(request) for request in requests]
        return await asyncio.gather(*tasks)

    async def add_to_queue(self, request: DownloadRequest) -> None:
        """Add a download request to the queue"""
        # If scheduled, add to scheduled queue
        if request.schedule_time:
            delay = (request.schedule_time - datetime.now()).total_seconds()
            if delay > 0:
                asyncio.create_task(self._schedule_download(request, delay))
                return

        # Add to priority queue
        await self._queue.put((request.priority.value, request))

    async def _schedule_download(self, request: DownloadRequest, delay: float) -> None:
        """Schedule a download for later"""
        await asyncio.sleep(delay)
        await self.add_to_queue(request)

    async def process_queue(self) -> None:
        """Process the download queue continuously"""
        while True:
            try:
                _, request = await self._queue.get()
                task = asyncio.create_task(self.download(request))
                self._active_downloads[request.url] = task
                task.add_done_callback(
                    lambda t: self._active_downloads.pop(request.url, None)
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing queue: {e}")
                await asyncio.sleep(1)

    def add_progress_callback(
        self, callback: Callable[[str, ProgressInfo], None]
    ) -> None:
        """Add a progress tracking callback"""
        self._progress_callbacks.append(callback)

    def remove_progress_callback(
        self, callback: Callable[[str, ProgressInfo], None]
    ) -> None:
        """Remove a progress tracking callback"""
        if callback in self._progress_callbacks:
            self._progress_callbacks.remove(callback)
