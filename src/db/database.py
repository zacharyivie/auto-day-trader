import sqlite3
from pathlib import Path
from contextlib import contextmanager
import sqlite_vec

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Create database in user's app data directory
            app_data = Path.home() / "AppData" / "Local" / "AutoDayTrader"
            app_data.mkdir(parents=True, exist_ok=True)
            db_path = str(app_data / "autodaytrader.db")
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with tables and sqlite-vec extension"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Load sqlite-vec extension
            sqlite_vec.load(conn)
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'FILLED', 'CANCELLED')),
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message_type TEXT NOT NULL CHECK (message_type IN ('TRADE', 'COT', 'SYSTEM')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Documents table for RAG
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    doc_type TEXT NOT NULL, -- 'research', 'news', 'analysis', etc.
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Vector table for embeddings (sqlite-vec approach)
            cursor.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_documents USING vec0(
                    document_id INTEGER PRIMARY KEY,
                    embedding FLOAT[1536]
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        # Load sqlite-vec for each connection
        sqlite_vec.load(conn)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()