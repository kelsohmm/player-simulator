import os
from config import MODEL_FILENAME, DB_FILENAME, PREVIEW_FILENAME
from simulator.memory.db_commands import commit_db_schema
from simulator.memory.database import Database


def verify_session_path(session_path):
    model_path = os.path.join(session_path, MODEL_FILENAME)
    db_path = os.path.join(session_path, DB_FILENAME)
    try:
        return len(os.listdir(session_path)) == 0\
               or (os.path.exists(model_path) and os.path.exists(db_path))
    except:
        return False

class Session:
    def __init__(self, session_path):
        self.session_path = session_path
        self.model_path = os.path.join(session_path, MODEL_FILENAME)
        self.db_path = os.path.join(self.session_path, DB_FILENAME)

    def __enter__(self):
        import sqlite3
        self.db_conn = sqlite3.connect(self.db_path)
        if len(os.listdir(self.session_path)) > 0:
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
        from simulator.agent.model import load_model
        self.model = load_model(self.model_path)

    def _open_new(self):
        from simulator.agent.model import create_network
        commit_db_schema(self.db_conn)
        self.model = create_network(os.path.join(self.session_path, PREVIEW_FILENAME))
        self.save_model()

