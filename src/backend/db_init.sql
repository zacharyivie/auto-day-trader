-- Create Users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL CHECK(LENGTH(username) > 0),
    password TEXT NOT NULL CHECK(LENGTH(password) > 0),
    salt TEXT NOT NULL CHECK(LENGTH(salt) > 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_endpoint TEXT NOT NULL CHECK(LENGTH(api_endpoint) > 0),
    auth_token TEXT NOT NULL CHECK(LENGTH(auth_token) > 0),
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);