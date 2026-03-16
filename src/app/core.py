from src.app.auth import get_kaggle_auth_header
from src.utils.http_client import get_client
from src.utils.logger import logger
import aiofiles
import os


async def get_storage_url(dataset_url: str) -> str:
    client = await get_client()
    auth_headers = get_kaggle_auth_header()

    response = await client.get(dataset_url, headers=auth_headers)

    if response.status_code == 302:
        storage_url = response.headers.get("Location")
        if not storage_url:
            raise ValueError("Kaggle returned 302 but no Location header found.")
        return storage_url

    response.raise_for_status()

    if response.status_code == 200:
        return dataset_url

    raise Exception(f"Failed to get storage URL: {response.status_code}")


async def save(storage_url: str, file_path: str):
    client = await get_client()
    start_byte = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    headers = {"Range": f"bytes={start_byte}-"} if start_byte > 0 else {}

    async with client.stream("GET", storage_url, headers=headers) as response:
        response.raise_for_status()
        write_mode = "ab" if response.status_code == 206 else "wb"

        if start_byte > 0 and response.status_code == 200:
            logger.info(f"Server ignored Range header, starting download from scratch.", extra={'path': file_path})

        async with aiofiles.open(file_path, mode=write_mode) as f:
            async for chunk in response.aiter_bytes(chunk_size=8192):
                await f.write(chunk)
