
_DATABASE_SCHEMA = '''
    CREATE TABLE history (
        game_id INT NOT NULL,
        state_id INT NOT NULL,
        state BLOB NOT NULL,
        action_idx INT NOT NULL,
        score REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        pred1 REAL, pred2 REAL, pred3 REAL, pred4 REAL, pred5 REAL, pred6 REAL,
        PRIMARY KEY (game_id, state_id)
    ); 
'''

def commit_db_schema(conn):
    conn.execute(_DATABASE_SCHEMA)
    conn.commit()


def get_max_game_id(conn):
    res = conn.execute('SELECT MAX(game_id) FROM history')
    (max_game_id, ) = list(res)[0]
    return max_game_id if max_game_id is not None else 0


def get_db_size(conn):
    res = conn.execute('SELECT COUNT(*) FROM history')
    (count, ) = list(res)[0]
    return count if count is not None else 0

