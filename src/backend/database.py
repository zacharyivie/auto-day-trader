from sqlite3 import connect, Connection
from pathlib import Path
import os
import platform
import logging

CURRENT_DIR = Path(__file__).parent
DB_INIT_PATH: Path = CURRENT_DIR / "db_init.sql"
APP_NAME: str = "AutoDayTrader"

_LOGGER_NAME: str = __name__.split('.')[-1].upper()

class Database:
    """Handle database connections and initialization"""
    db_initialized: bool = False
    
    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(_LOGGER_NAME)
        self._db_path: Path = self._get_db_path()
        if not Database.db_initialized:
            self.init_db()
            Database.db_initialized = True
        
    def _get_db_path(self) -> Path:
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
        db_path = app_dir / "autodaytrader_v1.db"
        
        self._logger.info(f"Using path {db_path}")
        return db_path
    
    def init_db(self) -> None:
        """Initialize the database"""
        with connect(self._db_path) as conn:
            cursor = conn.cursor()
            with open(DB_INIT_PATH, "r") as f:
                init_script: str = f.read() 
                _ = cursor.executescript(init_script)
            conn.commit()
            self._logger.info(f"Database initialized successfully to path {self._db_path}")
            
    def connect(self) -> Connection:
        """Get a connection to the database"""
        self._logger.info(f"Database connection created")
        return connect(self._db_path)