from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, IntEnum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypeVar,
    Protocol,
    runtime_checkable,
    Callable,
)

T = TypeVar("T")


class DownloadPriority(IntEnum):
    LOW = 0
    NORMAL = 5
    HIGH = 7
    CRITICAL = 9


class VerificationMethod(StrEnum):
    MD5 = "md5"
    SHA256 = "sha256"
    SHA512 = "sha512"


@dataclass
class TimeoutConfig:
    connect: float = 30.0
    read: float = 30.0
    write: float = 30.0
    pool: float = 60.0


@dataclass
class RetryConfig:
    max_attempts: int = 3
    min_wait: float = 1.0
    max_wait: float = 60.0
    jitter: bool = True
    retry_codes: List[int] = (408, 429, 500, 502, 503, 504)


@dataclass
class RateLimitConfig:
    requests_per_second: float = 10.0
    burst_size: int = 20
    strategy: str = "token_bucket"


@dataclass
class CacheConfig:
    enabled: bool = True
    storage_type: str = "memory"  # or "disk", "db"
    max_size: int = 1024 * 1024 * 100  # 100MB
    ttl: int = 3600  # 1 hour
    cache_path: Optional[str] = None


@dataclass
class ChunkConfig:
    enabled: bool = False
    size: int = 1024 * 1024  # 1MB
    resume: bool = True


@dataclass
class SSLConfig:
    verify: bool = True
    cert_path: Optional[str] = None
    key_path: Optional[str] = None
    ca_path: Optional[str] = None


@dataclass
class AuthConfig:
    type: str = "basic"  # or "bearer", "digest"
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None


@dataclass
class DownloadRequest:
    url: str
    context: Any = None
    priority: DownloadPriority = DownloadPriority.NORMAL
    timeout: Optional[TimeoutConfig] = None
    headers: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None
    verify_checksum: Optional[str] = None
    verify_method: VerificationMethod = VerificationMethod.SHA256
    chunk_config: Optional[ChunkConfig] = None
    bypass_cache: bool = False
    schedule_time: Optional[datetime] = None
    auth: Optional[AuthConfig] = None
    ssl: Optional[SSLConfig] = None
    proxy: Optional[str] = None

    @classmethod
    def make(cls, url: str, context: Any = None) -> "DownloadRequest":
        return cls(url=url, context=context)

    @classmethod
    def make_many(
        cls, urls: List[str], callback: Callable[[str], None]
    ) -> List["DownloadRequest"]:
        return [
            cls(url=url, context=callback(url) if callback else None) for url in urls
        ]


@dataclass
class ProgressInfo:
    bytes_downloaded: int
    total_bytes: Optional[int]
    chunk_index: Optional[int]
    total_chunks: Optional[int]
    speed_bps: Optional[float]
    eta_seconds: Optional[float]


@dataclass
class DownloadResult:
    url: str
    status_code: int
    headers: Dict[str, str]
    content: bytes
    context: Any
    error: Optional[Exception] = None
    retry_count: int = 0
    cached: bool = False
    chunks_completed: int = 0
    total_chunks: int = 1
    checksum: Optional[str] = None
    checksum_verified: bool = False
    download_time: float = 0.0
    progress: Optional[ProgressInfo] = None


@runtime_checkable
class Plugin(Protocol):
    """Base protocol for plugins"""

    async def initialize(self) -> None: ...
    async def pre_request(self, request: DownloadRequest) -> DownloadRequest: ...
    async def post_response(self, result: DownloadResult) -> DownloadResult: ...
    async def cleanup(self) -> None: ...
