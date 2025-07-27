from typing import List, Dict, Optional
import sqlite3
import json

class BaseQueries:
    def __init__(self, database):
        self.db = database

class UserQueries(BaseQueries):
    def create_user(self, username: str, email: str, password_hash: str) -> int:
        """Create a new user and return user ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

class TradeQueries(BaseQueries):
    def create_trade(self, user_id: int, symbol: str, side: str, quantity: int, price: float, notes: str = None) -> int:
        """Create a new trade and return trade ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO trades (user_id, symbol, side, quantity, price, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, symbol, side, quantity, price, notes)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_trades_by_user(self, user_id: int) -> List[Dict]:
        """Get all trades for a user"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM trades WHERE user_id = ? ORDER BY timestamp DESC",
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def update_trade_status(self, trade_id: int, status: str) -> bool:
        """Update trade status"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE trades SET status = ? WHERE id = ?",
                (status, trade_id)
            )
            conn.commit()
            return cursor.rowcount > 0

class MessageQueries(BaseQueries):
    def create_message(self, user_id: int, message_type: str, content: str) -> int:
        """Create a new message and return message ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (user_id, message_type, content) VALUES (?, ?, ?)",
                (user_id, message_type, content)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_messages_by_user(self, user_id: int, message_type: str = None) -> List[Dict]:
        """Get messages for a user, optionally filtered by type"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if message_type:
                cursor.execute(
                    "SELECT * FROM messages WHERE user_id = ? AND message_type = ? ORDER BY timestamp DESC",
                    (user_id, message_type)
                )
            else:
                cursor.execute(
                    "SELECT * FROM messages WHERE user_id = ? ORDER BY timestamp DESC",
                    (user_id,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_message_read(self, message_id: int) -> bool:
        """Mark message as read"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE messages SET is_read = 1 WHERE id = ?",
                (message_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread messages for a user"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE user_id = ? AND is_read = 0",
                (user_id,)
            )
            return cursor.fetchone()[0]

class DocumentQueries(BaseQueries):
    """Queries for RAG document storage and retrieval using sqlite-vec"""
    
    def create_document(self, user_id: int, title: str, content: str, doc_type: str, embedding: List[float]) -> int:
        """Create a new document with embedding"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert document
            cursor.execute(
                "INSERT INTO documents (user_id, title, content, doc_type) VALUES (?, ?, ?, ?)",
                (user_id, title, content, doc_type)
            )
            document_id = cursor.lastrowid
            
            # Insert embedding into vector table
            cursor.execute(
                "INSERT INTO vec_documents (document_id, embedding) VALUES (?, ?)",
                (document_id, json.dumps(embedding))
            )
            
            conn.commit()
            return document_id
    
    def search_similar_documents(self, user_id: int, query_embedding: List[float], limit: int = 5, doc_type: str = None) -> List[Dict]:
        """Search for similar documents using vector similarity"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Convert embedding to JSON string for sqlite-vec
            query_vec = json.dumps(query_embedding)
            
            if doc_type:
                cursor.execute("""
                    SELECT d.id, d.title, d.content, d.doc_type,
                           vec_distance_cosine(v.embedding, ?) as distance
                    FROM documents d
                    JOIN vec_documents v ON d.id = v.document_id
                    WHERE d.user_id = ? AND d.doc_type = ?
                    ORDER BY distance ASC
                    LIMIT ?
                """, (query_vec, user_id, doc_type, limit))
            else:
                cursor.execute("""
                    SELECT d.id, d.title, d.content, d.doc_type,
                           vec_distance_cosine(v.embedding, ?) as distance
                    FROM documents d
                    JOIN vec_documents v ON d.id = v.document_id
                    WHERE d.user_id = ?
                    ORDER BY distance ASC
                    LIMIT ?
                """, (query_vec, user_id, limit))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                result['similarity'] = 1 - result['distance']  # Convert distance to similarity
                results.append(result)
            
            return results
    
    def get_document_by_id(self, document_id: int) -> Optional[Dict]:
        """Get document by ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_document_embedding(self, document_id: int, embedding: List[float]) -> bool:
        """Update document embedding"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE vec_documents SET embedding = ? WHERE document_id = ?",
                (json.dumps(embedding), document_id)
            )
            cursor.execute(
                "UPDATE documents SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (document_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
