from sqlite3 import Binary

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

    def insert(self, game_id, state_id, state, action_idx, score):
        self.cursor.execute('INSERT INTO history (game_id, state_id, state, action_idx, score) ' # do not insert timestamp
                            'VALUES (?,?,?,?,?)', (game_id, state_id, Binary(state), int(action_idx), score))
        self.conn.commit()

    def get_free_game_id(self):
        res = self.cursor.execute('SELECT MAX(game_id) FROM history')
        (max_game_id, ) = list(res)[0]
        return max_game_id+1 if max_game_id is not None else 0

    def _query_history_count(self):
        res = self.cursor.execute('SELECT COUNT(*) FROM history')
        (count, ) = list(res)[0]
        return count if count is not None else 0
