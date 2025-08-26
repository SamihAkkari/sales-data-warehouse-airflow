from logging_manager import Loggers
from data_ingestion import Ingestor
import utils as utils


# Initialise the directories
utils.init_dirs_and_logs()

# 
log_manager = Loggers()  # uses default rotating file handler
log_manager.setup()

ingestor = Ingestor(log_manager)
ingestor.ingest()