from src.utils.http_client import init_client, close_client
from src.app.core import get_storage_url, save
from contextlib import asynccontextmanager
from src.utils.hash_functions import check_corrupted
from src.utils.settings import settings
from src.utils.logger import logger
from fastapi import FastAPI
import asyncio
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_client()
    yield
    await close_client()


app = FastAPI(lifespan=lifespan)


@app.post('/download')
async def download():
    attempts = 0
    max_attempts = 5
    path = settings.LOCAL_DOWNLOADS_LOCATION

    while attempts < max_attempts:
        try:
            url = await get_storage_url(settings.KAGGLE_DOWNLOAD_URL)
            server_hash = await save(url, path)
            check_corrupted(path, server_hash)
            return 'file downloaded', 200
        except (httpx.TransportError, httpx.HTTPStatusError) as e:
            if isinstance(e, httpx.TransportError) or e.response.is_server_error:
                attempts += 1
                logger.warning(f'disconnected, retrying attempt number {attempts}')
                await asyncio.sleep(2 ** attempts)
            elif e.response.status_code in (401, 403):
                logger.error(
                    f'Kaggle authentication failed. check your API token',
                    extra={'status': e.response.status_code, 'attempt': attempts}
                )
                raise e
            else:
                logger.error(f'HTTP error: {e.response.status_code}', extra={'attempt': attempts})
                raise e
        except Exception as e:
            logger.exception('unexpected error while downloading file', extra={'attempt': attempts})
            raise e
