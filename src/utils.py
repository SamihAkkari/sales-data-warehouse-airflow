from paths import LOG_DIR, LOG_FILES
from pathlib import Path

def init_dirs_and_logs():
    # Ensure directories exist
    for dir_path in [LOG_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    # Ensure log files exist
    for log_file in LOG_FILES.values():
        # log_file.touch(exist_ok=True)
        log_file.write_text("")