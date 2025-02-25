from log.logger import Logger

logger = Logger(__name__, 4)

if __name__ == '__main__':
    logger.debug("Test debug!")
    logger.info("Test info!")
    logger.warning("Test warning!")
    logger.error("Test error!")
    logger.critical("Test critical!")
