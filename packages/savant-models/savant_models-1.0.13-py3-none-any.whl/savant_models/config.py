import os

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    LOGGER_NAME: str = "ml-annotation-tool"
    LOG_FORMAT: str = (
        "%(levelprefix)s | %(asctime)s | %(pathname)s:%(lineno)d | %(message)s"
    )
    LOG_LEVEL: str = (
        "ERROR"
        if os.getenv("ENVIRONMENT") == "testing"
        or os.getenv("ENVIRONMENT") == "local"
        or os.getenv("ENVIRONMENT") == "production"
        else "DEBUG"
    )
    # Logging config
    version: float = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "registry": {"handlers": ["default"], "level": LOG_LEVEL},
    }
