
# TODO: change reward to absolute score
_DATABASE_SCHEMA = '''
    CREATE TABLE history (
        game_id INT NOT NULL,
        state_id INT NOT NULL,
        state BLOB NOT NULL,
        action_idx INT NOT NULL,
        reward REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP); 
'''
_DATABASE_HISTORY_INDEX = '''
        CREATE INDEX game_moment ON history (game_id, state_id);
'''

def commit_db_schema(connection):
    cursor = connection.cursor()
    cursor.execute(_DATABASE_SCHEMA)
    cursor.execute(_DATABASE_HISTORY_INDEX)
    connection.commit()
