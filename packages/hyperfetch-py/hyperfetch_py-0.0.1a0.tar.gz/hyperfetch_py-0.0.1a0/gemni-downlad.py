import asyncio
import httpx
import time
import hashlib
import os
from typing import List, Callable, Dict, Optional, Union, Tuple, Any
from dataclasses import dataclass
from collections import deque
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class DownloadResult:
    """Represents the result of a URL download."""

    url: str
    status_code: int
    headers: httpx.Headers
    content: bytes
    error: Optional[Exception] = None
    skipped: bool = False
    retries: int = 0
    progress: float = 0.0


class RetryConfig:
    """Configures retry behavior."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor


class TimeoutConfig:
    """Configures timeout behavior."""

    def __init__(self, connect_timeout: float = 10.0, read_timeout: float = 30.0):
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout


class RateLimiter:
    """Implements rate limiting."""

    def __init__(self, requests_per_second: Optional[float] = None):
        self.requests_per_second = requests_per_second
        self.last_request_time = 0.0

    async def acquire(self):
        if self.requests_per_second:
            elapsed = time.time() - self.last_request_time
            if elapsed < 1.0 / self.requests_per_second:
                await asyncio.sleep(1.0 / self.requests_per_second - elapsed)
            self.last_request_time = time.time()


class ChunkedDownloader:
    """Handles chunked downloads."""

    def __init__(self, chunk_size: int = 1024 * 1024):
        self.chunk_size = chunk_size

    async def download_chunked(
        self,
        client: httpx.AsyncClient,
        url: str,
        headers: Dict[str, str],
        progress_callback: Optional[Callable[[DownloadResult], None]] = None,
    ) -> bytes:
        start = 0
        total_content = b""
        async with client.stream("GET", url, headers=headers) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Length", 0))

            async for chunk in response.aiter_bytes():
                total_content += chunk
                start += len(chunk)
                if progress_callback and total_size > 0:
                    progress = start / total_size
                    result = DownloadResult(
                        url=url,
                        status_code=response.status_code,
                        headers=response.headers,
                        content=b"",
                        progress=progress,
                    )
                    progress_callback(result)
        return total_content


class AsyncDownloader:
    """Asynchronous HTTP downloader with advanced features."""

    def __init__(
        self,
        concurrency: int = 10,
        global_headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        retry_config: Optional[RetryConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None,
        rate_limiter: Optional[RateLimiter] = None,
        chunked_downloader: Optional[ChunkedDownloader] = None,
        verify_ssl: bool = True,
        user_agent: str = "AsyncDownloader/1.0",
        cookies: Optional[Dict[str, str]] = None,
    ):
        self.concurrency = concurrency
        self.global_headers = global_headers or {}
        self.proxy = proxy
        self.retry_config = retry_config or RetryConfig()
        self.timeout_config = timeout_config or TimeoutConfig()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.chunked_downloader = chunked_downloader or ChunkedDownloader()
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent
        self.cookies = cookies or {}
        self.sem = asyncio.Semaphore(concurrency)
        self.download_queue = deque()
        self.cache = {}  # Simple in-memory cache

    async def _download_single(
        self,
        url: str,
        headers_callback: Optional[Callable[[str], Tuple[Dict[str, str], bool]]] = None,
        progress_callback: Optional[Callable[[DownloadResult], None]] = None,
        checksum: Optional[str] = None,
    ) -> DownloadResult:
        """Downloads a single URL."""
        async with self.sem:
            retries = 0
            while retries <= self.retry_config.max_retries:
                try:
                    await self.rate_limiter.acquire()
                    headers = self.global_headers.copy()
                    if headers_callback:
                        custom_headers, should_download = headers_callback(url)
                        if not should_download:
                            return DownloadResult(
                                url=url,
                                status_code=0,
                                headers={},
                                content=b"",
                                skipped=True,
                            )
                        if custom_headers:
                            headers.update(custom_headers)
                    headers["User-Agent"] = self.user_agent
                    proxies = (
                        {"http://": self.proxy, "https://": self.proxy}
                        if self.proxy
                        else None
                    )
                    timeout = httpx.Timeout(
                        connect=self.timeout_config.connect_timeout,
                        read=self.timeout_config.read_timeout,
                    )

                    async with httpx.AsyncClient(
                        proxies=proxies,
                        timeout=timeout,
                        verify=self.verify_ssl,
                        cookies=self.cookies,
                    ) as client:
                        if "Range" in headers:
                            content = await self.chunked_downloader.download_chunked(
                                client, url, headers, progress_callback
                            )
                        else:
                            response = await client.get(url, headers=headers)
                            response.raise_for_status()
                            content = response.content

                        if checksum:
                            if hashlib.sha256(content).hexdigest() != checksum:
                                raise ValueError("Checksum mismatch")

                        result = DownloadResult(
                            url=url,
                            status_code=response.status_code,
                            headers=response.headers,
                            content=content,
                            retries=retries,
                        )
                        self.cache[url] = result
                        return result

                except httpx.HTTPError as e:
                    logging.warning(f"HTTP error downloading {url}: {e}")
                    retries += 1
                    await asyncio.sleep(self.retry_config.backoff_factor**retries)
                except Exception as e:
                    logging.error(f"Error downloading {url}: {e}")
                    return DownloadResult(
                        url=url,
                        status_code=0,
                        headers={},
                        content=b"",
                        error=e,
                        retries=retries,
                    )
            return DownloadResult(
                url=url,
                status_code=0,
                headers={},
                content=b"",
                error=Exception("Max retries exceeded"),
                retries=retries,
            )

    async def download(
        self,
        urls: List[str],
        callback: Optional[Callable[[DownloadResult], None]] = None,
        headers_callback: Optional[Callable[[str], Tuple[Dict[str, str], bool]]] = None,
        progress_callback: Optional[Callable[[DownloadResult], None]] = None,
        checksums: Optional[Dict[str, str]] = None,
    ) -> List[DownloadResult]:
        tasks = []
        for url in urls:
            if url in self.cache:
                if callback:
                    callback(self.cache[url])
                continue
            tasks.append(
                self._download_single(
                    url,
                    headers_callback,
                    progress_callback,
                    checksums.get(url) if checksums else None,
                )
            )
        results = await asyncio.gather(*tasks)

        if callback:
            for result in results:
                callback(result)

        return results
