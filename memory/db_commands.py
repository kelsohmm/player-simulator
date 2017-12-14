import sqlite3


# TODO: change reward to absolute score
_DATABASE_SCHEMA = '''
    CREATE TABLE transitions (
        game_id INT NOT NULL,
        frame_number INT NOT NULL,
        curr_state BLOB NOT NULL,
        action_idx INT NOT NULL,
        reward REAL NOT NULL,
        next_state BLOB,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP); 
'''


def commit_db_schema(connection):
    cursor = connection.cursor()
    cursor.execute(_DATABASE_SCHEMA)
    connection.commit()
