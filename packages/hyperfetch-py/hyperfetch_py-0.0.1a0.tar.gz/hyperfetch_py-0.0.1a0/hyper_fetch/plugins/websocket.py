from typing import Dict

import httpx

from hyper_fetch.types import Plugin, DownloadRequest, DownloadResult


class WebSocketPlugin(Plugin):
    """Plugin for WebSocket support"""

    def __init__(self):
        self.active_connections: Dict[str, httpx.WebSocket] = {}

    async def initialize(self) -> None:
        pass

    async def pre_request(self, request: DownloadRequest) -> DownloadRequest:
        if request.url.startswith(("ws://", "wss://")):
            # Handle WebSocket connection
            ws = await httpx.WebSocket(request.url)
            self.active_connections[request.url] = ws
        return request

    async def post_response(self, result: DownloadResult) -> DownloadResult:
        return result

    async def cleanup(self) -> None:
        for ws in self.active_connections.values():
            await ws.close()
