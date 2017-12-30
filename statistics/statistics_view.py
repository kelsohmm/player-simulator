import pandas as pd

_HISTORY_VIEW_COLUMNS = ['game_id',
                         'state_id',
                         'action_idx',
                         'score',
                         'timestamp',
                         'pred1',
                         'pred2',
                         'pred3',
                         'pred4',
                         'pred5',
                         'pred6']

_TIMESTAMP_IDX = _HISTORY_VIEW_COLUMNS.index('timestamp')
_SELECT_HISTORY_QUERY = '''
    SELECT game_id,
           state_id,
           action_idx,
           score,
           (julianday(timestamp) - 2440587.5) * 86400.0 AS timestamp,
           pred1, pred2, pred3, pred4, pred5, pred6
    FROM history 
    ORDER BY game_id ASC, state_id ASC'''
_DB_DATE_FORMAT = '%Y-%m-%d '


class StatisticsView:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(_SELECT_HISTORY_QUERY)
        self.data = pd.DataFrame([], columns=_HISTORY_VIEW_COLUMNS)

    def get(self):
        self._update()
        return self.data

    def get_for_game(self, game_id):
        data = self.get()
        return data.loc[data['game_id'] == game_id]

    def _update(self):
        records = self.cursor.fetchall()
        if len(records) > 0:
            new_frame = pd.DataFrame.from_records(records,
                                                  columns=_HISTORY_VIEW_COLUMNS,
                                                  coerce_float=True)
            self.data = self.data.append(new_frame)
