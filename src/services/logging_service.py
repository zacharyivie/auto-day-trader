import logging
from pathlib import Path
import platform
import os

APP_NAME: str = "AutoDayTrader"

def _get_log_path() -> Path:
        """Get the path to the database file"""
        system = platform.system()
        if system == "Windows":
            base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        elif system == "Darwin":
            base_dir = Path.home() / "Library" / "Application Support"
        else:
            base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        app_dir = base_dir / APP_NAME
        app_dir.mkdir(parents=True, exist_ok=True)
        log_path = app_dir / "system.log"
        return log_path
        
def setup_logging():
    """Configure application-wide logging."""
    log_file = _get_log_path()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode='a', encoding='utf-8')
        ]
    )