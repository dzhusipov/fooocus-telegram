-- Sqlite
CREATE TABLE user_history (
    id INTEGER PRIMARY KEY,
    chat_id TEXT NOT NULL,
    user_prompt TEXT,
    result_image BLOB
);

-- Postgresql
CREATE TABLE user_history (
    id SERIAL PRIMARY KEY,
    chat_id TEXT NOT NULL,
    user_prompt TEXT,
    result_image BYTEA
);