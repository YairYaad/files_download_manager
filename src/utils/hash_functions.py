from src.utils.logger import logger
import hashlib
import base64


def calculate_file_md5_base64(file_path: str, chunk_size: int = 65536) -> str:
    hasher = hashlib.md5()

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)

    raw_hash = hasher.digest()
    base64_hash = base64.b64encode(raw_hash).decode('utf-8')

    return base64_hash


def get_md5_hash(headers):
    all_hashes = headers.get_list('x-goog-hash')
    server_md5_b64 = None

    for h in all_hashes:
        if h.startswith('md5='):
            server_md5_b64 = h.replace('md5=', '')
            break

    return server_md5_b64


def check_corrupted(file_path: str, server_hash: str):
    local_hash = calculate_file_md5_base64(file_path)

    if local_hash == server_hash:
        logger.info('integrity check passed: file is valid')
    else:
        logger.error('integrity check failed', extra={'local': local_hash, 'server': server_hash})
        raise Exception('downloaded file is corrupted')
