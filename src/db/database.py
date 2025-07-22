import sqlite3
from pathlib import Path
from contextlib import contextmanager

class Database:
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            app_data = Path.home() / "AppData" / "Local" / "AutoDayTrader"
            app_data.mkdir(parents=True, exist_ok=True)
            db_path = str(app_data / "autodaytrader.db")
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor