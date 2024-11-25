import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="analyzer.log", level=logging.INFO, filemode="w")


__all__ = [
    'logger'
]