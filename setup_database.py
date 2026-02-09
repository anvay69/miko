import sqlite3

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('miko.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL commands to create tables and indexes
create_users_table = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

create_scores_table = '''
CREATE TABLE IF NOT EXISTS scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    time_used INTEGER NOT NULL,
    solved INTEGER NOT NULL,
    total INTEGER NOT NULL,
    difficulty TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
'''

create_leaderboard_table = '''
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id INTEGER NOT NULL,
    score_id INTEGER NOT NULL,
    difficulty TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (score_id) REFERENCES scores(score_id) ON DELETE CASCADE
);
'''

# Create indexes
create_index_username = '''
CREATE INDEX IF NOT EXISTS idx_username ON users(username);
'''

create_index_email = '''
CREATE INDEX IF NOT EXISTS idx_email ON users(email);
'''

create_index_user_id = '''
CREATE INDEX IF NOT EXISTS idx_user_id ON scores(user_id);
'''

create_index_leaderboard_user_id = '''
CREATE INDEX IF NOT EXISTS idx_leaderboard_user_id ON leaderboard(user_id);
'''

create_index_leaderboard_difficulty = '''
CREATE INDEX IF NOT EXISTS idx_leaderboard_difficulty ON leaderboard(difficulty);
'''

# Execute the SQL commands
cursor.execute(create_users_table)
cursor.execute(create_scores_table)
cursor.execute(create_leaderboard_table)
cursor.execute(create_index_username)
cursor.execute(create_index_email)
cursor.execute(create_index_user_id)
cursor.execute(create_index_leaderboard_user_id)
cursor.execute(create_index_leaderboard_difficulty)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete. The 'miko.db' database has been created with the necessary tables and indexes.")

