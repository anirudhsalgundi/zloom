import logging
import shutil

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

width = shutil.get_terminal_size().columns

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

def log_banner(logger: logging.Logger, message: str) -> None:
    print("-" * width)
    logger.info(message)