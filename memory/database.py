from sqlite3 import Binary
from memory.db_commands import get_max_game_id, get_db_size

_SELECT_MEMORY_QUERY = '''
    SELECT prev_memories.state,
           prev_memories.action_idx,
           prev_memories.score,
           next_memories.score,
           next_memories.state
    FROM history AS prev_memories
    LEFT JOIN history AS next_memories
    ON prev_memories.game_id = next_memories.game_id AND next_memories.state_id = (prev_memories.state_id + 1)
    ORDER BY RANDOM() 
    LIMIT %d
'''

class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def size(self):
        return self._query_history_count()

    def fetch_random_batch(self, batch_size):
        return list(self.cursor.execute(_SELECT_MEMORY_QUERY % batch_size))

    def insert(self, game_id, state_id, state, action_idx, score, predictions):
        self.cursor.execute('INSERT INTO history (game_id, state_id, state, action_idx, score, pred1, pred2, pred3, pred4, pred5, pred6) '
                            'VALUES (?,?,?,?,?, ?,?,?,?,?,?)', (game_id, state_id, Binary(state), int(action_idx), score) + tuple(predictions))

    def rollback_changes(self):
        self.conn.rollback()

    def commit_changes(self):
        self.conn.commit()

    def get_free_game_id(self):
        return get_max_game_id(self.conn) + 1

    def _query_history_count(self):
        return get_db_size(self.conn)
