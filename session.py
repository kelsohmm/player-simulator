import sqlite3
from config import *
from memory.database import Database
from memory.db_commands import commit_db_schema
from memory.gamestate_repo import Repo
from training.model import create_network, load_model

DB_FILENAME = 'history.db'

class Session:
    def __init__(self, session_path):
        self.session_path = session_path
        self.model_path = os.path.join(session_path, 'model.h5')

    def __enter__(self):
        if os.path.exists(self.session_path):
            self._open_existing()
        else:
            self._open_new()

        self.db = Database(self.db_conn)

        return self

    def __exit__(self, type, value, traceback):
        self.db_conn.close()

    def get_db(self):
        return self.db

    def get_model(self):
        return self.model

    def save_model(self):
        self.model.save(self.model_path)

    def _open_existing(self):
        self.db_conn = sqlite3.connect(os.path.join(self.session_path, DB_FILENAME))
        self.model = load_model(self.model_path)

    def _open_new(self):
        os.makedirs(self.session_path)
        self.db_conn = sqlite3.connect(os.path.join(self.session_path, DB_FILENAME))
        commit_db_schema(self.db_conn)
        self.model = create_network(os.path.join(self.session_path, 'model_preview.png'))
        self.save_model()

