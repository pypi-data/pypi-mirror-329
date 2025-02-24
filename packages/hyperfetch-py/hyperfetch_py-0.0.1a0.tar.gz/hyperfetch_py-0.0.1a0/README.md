# HyperFetch: Asynchronous HTTP Downloader

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

HyperFetch is a feature-rich, asynchronous HTTP downloader, designed for high-performance parallel
downloads. It offers a wide range of features including retry logic, rate limiting, chunked downloads, progress
tracking, and more.

## Features

* **Asynchronous Parallel Downloads:** Download multiple URLs concurrently for maximum efficiency.
* **Retry Logic:** Configurable retry mechanism with exponential backoff for handling transient errors.
* **Timeout Control:** Granular control over connection and read timeouts.
* **Rate Limiting:** Prevent server overload with configurable rate limiting.
* **Chunked Downloads:** Support for downloading large files in chunks using HTTP Range requests.
* **Progress Tracking:** Monitor download progress with progress callbacks.
* **Content Validation:** Verify downloaded content using checksums.
* **Caching:** Avoid redundant downloads with a built-in caching mechanism.
* **Redirect Handling:** Control redirect behavior.
* **SSL/TLS Verification:** Configurable SSL/TLS verification settings.
* **Custom Headers:** Customize request headers.
* **Cookies:** Support for storing and sending cookies.
* **Download Queues:** Manage large numbers of URLs with download queues.
* **Download Scheduling:** Schedule downloads for specific times.
* **Plugin System:** Extend functionality with custom plugins.
* **Logging:** Comprehensive logging for debugging and monitoring.
* **Proxy Support:** HTTP/HTTPS and SOCKS5 proxy support.
* **Skip URL functionality:** Skip specific URLs based on a callback.

## Installation

```bash
pip install hyperfetch-py
```

## Quick Usage

```python
import asyncio
from hyper_fetch.downloader import AsyncDownloader
from hyper_fetch.types import DownloadRequest


async def main():
    req = DownloadRequest.make("https://httpbin.org/headers")
    downloader = AsyncDownloader()
    result = await downloader.download(req)
    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
```

## Usage

```python
import asyncio
from pathlib import Path
from typing import List

import aiofiles

from hyper_fetch.downloader import AsyncDownloader
from hyper_fetch.types import (
    RetryConfig,
    ChunkConfig,
    SSLConfig,
    DownloadRequest,
    ProgressInfo,
)


def download(
        urls: List[str],
        output_dir: str,
        concurrency: int,
        retry: int,
        timeout: int,
        chunk_size: int,
        verify: bool,
):
    """Download files from URLs"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Configure downloader
    retry_config = RetryConfig(max_attempts=retry)
    chunk_config = ChunkConfig(enabled=True, size=chunk_size)
    ssl_config = SSLConfig(verify=verify)

    # Progress callback
    def show_progress(url: str, progress: ProgressInfo):
        if progress.total_bytes:
            percentage = (progress.bytes_downloaded / progress.total_bytes) * 100
            print(f"{url}: {percentage:.1f}% complete")

    async def run_downloads():
        downloader = AsyncDownloader(concurrency=concurrency, retry_config=retry_config)
        downloader.add_progress_callback(show_progress)

        # Create download requests
        requests = [
            DownloadRequest(
                url=url,
                context={"output_path": output_path / Path(url).name},
                chunk_config=chunk_config,
                ssl=ssl_config,
            )
            for url in urls
        ]

        # Download files
        results = await downloader.download_many(requests)

        # Save files
        for result in results:
            if result.error:
                print(f"Error downloading {result.url}: {result.error}")
                continue

            output_file = result.context["output_path"]
            async with aiofiles.open(output_file, "wb") as f:
                await f.write(result.content)

            print(f"Downloaded {result.url} to {output_file}")

    asyncio.run(run_downloads())
```

## Configuration

You can configure HyperFetch using the following classes:

* `RetryConfig`: Configure retry behavior.
* `TimeoutConfig`: Configure connection and read timeouts.
* `RateLimiter`: Configure rate limiting.
* `AsyncDownloader`: Main downloader class with various configuration options.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

Copyright Dr. Masroor Ehsan 2025.

Distributed under the MIT License. See the `LICENSE` file for more information.
