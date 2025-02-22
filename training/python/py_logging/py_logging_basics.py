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
# Add filter using Filter class
class FilterLogs(logging.Filter):
    def filter(self, record):
        return "CRITICAL" in record.getMessage()
stream_handler.addFilter(FilterLogs())
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(f"{__name__}.logs")
file_handler_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s")
file_handler.setFormatter(file_handler_formatter)
# Add filter using lambda function
file_handler.addFilter(lambda record: "SENSITIVE" not in record.getMessage())
logger.addHandler(file_handler)

logger.propagate=False

if __name__ == "__main__":
    logger.info("This is logged to only the log file because it is not sensitive")
    logger.info("This is not logged anywhere because though it is info, it has SENSITIVE information")
    logger.info("This is logged to only the file because though it is CRITICAL, the level is lower than the set level for streamhandler")
    logger.error("This is logged to only the file because though it is an error, it is not critical")
    logger.error("This is logged to both the console and file because it is an error and it is CRITICAL")