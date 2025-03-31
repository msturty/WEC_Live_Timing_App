import logging
import logging.config
import os
from datetime import datetime

def LogToFile(configDictionary):
    try:
        logFileFullPath = os.path.dirname(os.path.abspath(__file__))
        logFileFullPath = os.path.join(logFileFullPath, "logs")
        logFileName = datetime.now().strftime(configDictionary["applicationName"] + "%Y_%m_%d.log")
        logFileNameAndPath = os.path.join(logFileFullPath, logFileName)
        print(logFileNameAndPath)
                    
        if not os.path.exists(logFileFullPath):
            os.makedirs(logFileFullPath, exist_ok=True)
        
        LOG_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "DEBUG",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": logFileNameAndPath,
                    "formatter": "standard",
                    "level": "DEBUG",
                    "mode": "a",  # Use "a" (append) or "w" (overwrite)
                    "delay": False  # Ensures the file is opened immediately
                }
            },
            "loggers": {
                "": {  # Root logger
                    "handlers": ["console","file"],
                    "level": "DEBUG",
                    "propagate": True
                },
                "RPALogger": {  # Specific module logger
                    "handlers": ["console", "file"],
                    "level": "DEBUG",
                    "propagate": True
                }
            }
        }
        logging.config.dictConfig(LOG_CONFIG)
        logger = logging.getLogger("StandardLogger")
        return logger
    except Exception as e:
        return Exception
