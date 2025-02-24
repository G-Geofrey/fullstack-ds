import logging
import logging.config

class FilterLogs(logging.Filter):
    def filter(self, record):
        return "CRITICAL" in record.getMessage()

logging_config = {
    "version":1,
    "disable_existing_loggers":False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
        },
        "simple": {
            "format": "%(asctime)s:%(levelname)s:%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s:%(module)s:%(funcName)s:%(name)s:%(levelname)s:%(message)s"
        }
    },
    "filters": {
        "console_filter": {
            "()": FilterLogs,
        }
    },
    "handlers": {
        "default": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
            "filters": ["console_filter"]
        },
        "file_handler": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"./logs/{__name__}.log",
            "formatter": "detailed"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "WARNING"
        },
        __name__: {
            "handlers": ["default", "file_handler"],
            "level": "INFO",
            "propagate": False
        }
    }
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.info("This is logged to only the log file because it is a higher level than the one for console")
    logger.info("This is logged to only the file because though it is CRITICAL, the level is higher than the one for console")
    logger.error("This is logged to only the file because though it is an error, it is not critical")
    logger.error("This is logged to both the console and file because it is an error and it is CRITICAL")