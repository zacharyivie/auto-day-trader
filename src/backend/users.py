from sqlite3 import Cursor
from .database import Database

class User:
    
    def __init__(self):
        self._db: Database = Database()
    
    def CreateUser(self, username: str, password: str, salt: str) -> None:
        with self._db.connect() as conn:
            cursor: Cursor = conn.cursor()
            _ = cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, password, salt))
            conn.commit()
            
    def GetUserById(self, id: int) -> dict[str, str]:
        with self._db.connect() as conn:
            cursor: Cursor = conn.cursor()
            user_query = cursor.execute("SELECT username, password, salt FROM users WHERE id = ?", (id,))
            users = user_query.fetchall()
            if len(users) == 0:
                raise ValueError(f"No user with id: {id}")
            return {"username": users[0][0], "password": users[0][1], "salt": users[0][2]}
    
    def GetUserIdByUsername(self, username: str) -> dict[str, int]:
        with self._db.connect() as conn:
            cursor: Cursor = conn.cursor()
            user_query = cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            users = user_query.fetchall()
            if len(users) == 0:
                raise ValueError(f"No user with username: {username}")
            return {"id": users[0][0]}
    
    def DeleteUser(self, id: int) -> int:
        with self._db.connect() as conn:
            cursor: Cursor = conn.cursor()
            _ = cursor.execute("DELETE FROM users WHERE id = ?", (id,))
            users_deleted = cursor.rowcount
            conn.commit()
            return users_deleted