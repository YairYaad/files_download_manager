import httpx
from typing import Optional

_client: Optional[httpx.AsyncClient] = None


async def init_client():
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(None),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            follow_redirects=False
        )
    return _client


async def get_client() -> httpx.AsyncClient:
    if _client is None or _client.is_closed:
        return await init_client()
    return _client


async def close_client():
    global _client
    if _client:
        await _client.aclose()
        _client = None
