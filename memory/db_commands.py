
_DATABASE_SCHEMA = '''
    CREATE TABLE history (
        game_id INT NOT NULL,
        state_id INT NOT NULL,
        state BLOB NOT NULL,
        action_idx INT NOT NULL,
        score REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (game_id, state_id)
    ); 
'''

def commit_db_schema(connection):
    cursor = connection.cursor()
    cursor.execute(_DATABASE_SCHEMA)
    connection.commit()
