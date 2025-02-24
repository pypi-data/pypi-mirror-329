# optional dependencies
try:
    import brotli
except ImportError:  # pragma: no cover
    try:
        import brotlicffi as brotli
    except ImportError:
        brotli = None
try:
    import zstandard
except ImportError:  # pragma: no cover
    zstandard = None  # type: ignore

from hyper_fetch.types import Plugin, DownloadRequest, DownloadResult


class CompressionPlugin(Plugin):
    """Plugin for handling compressed responses"""

    async def initialize(self) -> None:
        pass

    async def pre_request(self, request: DownloadRequest) -> DownloadRequest:
        if request.headers is None:
            request.headers = {}
        request.headers["Accept-Encoding"] = ", ".join(SUPPORTED_ENCODINGS)
        return request

    async def post_response(self, result: DownloadResult) -> DownloadResult:
        pass

    async def cleanup(self) -> None:
        pass


SUPPORTED_ENCODINGS = [
    "identity",
    "gzip",
    "deflate",
    "br",
    "zstd",
]

if brotli is None:
    SUPPORTED_ENCODINGS.pop("br")  # pragma: no cover
if zstandard is None:
    SUPPORTED_ENCODINGS.pop("zstd")  # pragma: no cover
