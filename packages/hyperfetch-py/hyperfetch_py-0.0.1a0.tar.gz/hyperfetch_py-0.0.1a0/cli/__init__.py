import asyncio
from pathlib import Path
from typing import List

import aiofiles
import click

from hyper_fetch.downloader import AsyncDownloader
from hyper_fetch.types import (
    RetryConfig,
    ChunkConfig,
    SSLConfig,
    DownloadRequest,
    ProgressInfo,
)


@click.group()
def cli():
    """HyperFetch CLI"""
    pass


@cli.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--output-dir", "-o", default=".", help="Output directory")
@click.option("--concurrency", "-c", default=5, help="Number of concurrent downloads")
@click.option("--retry", "-r", default=3, help="Number of retry attempts")
@click.option("--timeout", "-t", default=30, help="Timeout in seconds")
@click.option("--chunk-size", "-s", default=1024 * 1024, help="Chunk size in bytes")
@click.option("--verify/--no-verify", default=True, help="Verify SSL certificates")
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
            click.echo(f"{url}: {percentage:.1f}% complete")

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
                click.echo(f"Error downloading {result.url}: {result.error}")
                continue

            output_file = result.context["output_path"]
            async with aiofiles.open(output_file, "wb") as f:
                await f.write(result.content)

            click.echo(f"Downloaded {result.url} to {output_file}")

    asyncio.run(run_downloads())


if __name__ == "__main__":
    cli()
