import logging
import sys
from typing import Optional, Union
from enum import Enum
from logging.handlers import RotatingFileHandler

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class GroovinLogger:
    def __init__(self, 
        name: str = "groovindb", 
        level: Union[str, LogLevel] = LogLevel.INFO,
        log_file: Optional[str] = None,
        format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        rotate: bool = True,
        max_bytes: int = 10_000_000,  # 10MB
        backup_count: int = 5
    ):
        self.logger = logging.getLogger(name)
        self._set_level(level)
        self._configure_handlers(log_file, format)

        # Agregar rotación de logs
        if rotate and log_file:
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )

    def _set_level(self, level: Union[str, LogLevel]):
        if isinstance(level, str):
            level = LogLevel[level.upper()]
        self.logger.setLevel(level.value)

    def _configure_handlers(self, log_file: Optional[str], format: str):
        if self.logger.handlers:
            return

        formatter = logging.Formatter(format)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler opcional para archivo
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def set_level(self, level: Union[str, LogLevel]):
        self._set_level(level)

logger = GroovinLogger().logger 