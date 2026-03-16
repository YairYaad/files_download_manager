import logging
import sys
from pythonjsonlogger.json import JsonFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(filename)s %(lineno)d %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
