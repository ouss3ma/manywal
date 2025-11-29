import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent.parent / "logs" / ".manywal.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers (important in CLI apps)
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_FILE, mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))

        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
