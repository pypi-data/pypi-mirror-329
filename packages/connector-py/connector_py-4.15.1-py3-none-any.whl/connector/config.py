import os
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


LOG_LEVEL_ENV_VAR = "LUMOS_LOG_LEVEL"
LOG_DIRECTORY_ENV_VAR = "LUMOS_LOG_DIRECTORY"


class Config:
    def __init__(self) -> None:
        self.log_level: LogLevel = LogLevel.ERROR
        self.log_directory: Path | None = None

        self.set_log_level()
        self.set_log_directory()

    def set_log_level(self) -> None:
        log_level_string = os.environ.get(LOG_LEVEL_ENV_VAR, "ERROR")
        try:
            self.log_level = LogLevel(log_level_string)
        except ValueError as e:
            raise ValueError(
                f"Invalid log level set by environment variable {LOG_LEVEL_ENV_VAR}: {log_level_string}"
            ) from e

    def set_log_directory(self) -> None:
        log_directory_string = os.environ.get(LOG_DIRECTORY_ENV_VAR, None)
        if log_directory_string is not None:
            self.log_directory = Path(log_directory_string)


config = Config()
