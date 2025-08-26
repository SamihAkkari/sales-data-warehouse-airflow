import logging
from config import LoggingConfig
from logging.handlers import RotatingFileHandler
from paths import LOG_FILES

class Loggers:
    def __init__(self, log_file_key="app", default_handler="rotating_file"):
        if log_file_key not in LOG_FILES:
            raise ValueError(f"Unknown log_file_key '{log_file_key}'")
        self.log_file_path = LOG_FILES[log_file_key]
        self.handler_name = default_handler
        self.loggers = {}

    def setup(self):
        """
        Sets up multiple ETL loggers for Bronze, Silver, Gold stages.
        All loggers write to the same rotating log file.
        
        Returns:
            dict: {'bronze': logger, 'silver': logger, 'gold': logger}
        """
        self.set_formatter()
        self.set_handlers()
        self.apply_formatter_to_handler()
        self.set_loggers()

    def set_formatter(self):
        self.formatter = LoggingConfig.FORMATTER
    
    def set_handlers(self):
        handler_metadata = LoggingConfig.HANDLERS.get(self.handler_name)
        if not handler_metadata:
            raise ValueError(f"Handler '{self.handler_name}' is not defined in HANDLERS")
        
        if self.handler_name == "rotating_file":
            self.handler = RotatingFileHandler(
                self.log_file_path,
                maxBytes=handler_metadata.get("max_bytes"),
                backupCount=handler_metadata.get("backup_count"),
                encoding=handler_metadata.get("encoding")
            )

    def apply_formatter_to_handler(self):
        self.handler.setFormatter(self.formatter)

    def set_loggers(self):
        for stage in LoggingConfig.STAGES:
            logger = logging.getLogger(f"etl.{stage}")
            logger.setLevel(LoggingConfig.LEVEL)
            logger.propagate = LoggingConfig.PROPAGATE_STATUS
            logger.addHandler(self.handler)
            self.loggers[stage] = logger

    def get_logger(self, stage):
        if stage not in self.loggers:
            raise ValueError(f"Logger stage '{stage}' does not exist")
        return self.loggers[stage]