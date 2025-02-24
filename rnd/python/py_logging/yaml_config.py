import logging
import json
import logging.config
import yaml 

class FilterLogs(logging.Filter):
    def filter(self, record):
        return "CRITICAL" in record.getMessage()

with open("yaml_config.yaml", "r") as file:
    logging_config = yaml.safe_load(file)

logging.config.dictConfig(logging_config)
logger = logging.getLogger("module_name")
if __name__ == "__main__":
    logger.info("This is logged to only the log file because it is a higher level than the one for console")
    logger.info("This is logged to only the file because though it is CRITICAL, the level is higher than the one for console")
    logger.error("This is logged to only the file because though it is an error, it is not critical")
    logger.error("This is logged to both the console and file because it is an error and it is CRITICAL")

