import logging

# Config root
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)


# Named loggers
logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(f"{__name__}.logs")
file_handler_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s")
file_handler.setFormatter(file_handler_formatter)
logger.addHandler(file_handler)

logger.propagate=False

if __name__ == "__main__":
    logger.info("This is logged to only the log file")
    logger.error("This is logged to both the log file and console")