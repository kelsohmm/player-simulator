import sqlite3
from config import *
from memory.database import Database
from memory.db_commands import commit_db_schema
from memory.gamestate_repo import Repo
from training.model import create_network, load_model


class Session:
    def open(self, session_path):
        self.model_path = os.path.join(session_path, 'model.h5')

        if os.path.exists(session_path):
            self._open_existing(session_path)
        else:
            self._open_new(session_path)

        self.repo = Repo(Database(self.db_conn))

        return self.model, self.repo

    def save_model(self):
        self.model.save(self.model_path)

    def _open_existing(self, session_path):
        self.db_conn = sqlite3.connect(os.path.join(session_path, 'transitions.db'))
        self.model = load_model(self.model_path)

    def _open_new(self, session_path):
        os.makedirs(session_path)
        self.db_conn = sqlite3.connect(os.path.join(session_path, 'transitions.db'))
        commit_db_schema(self.db_conn)
        self.model = create_network(os.path.join(session_path, 'model_preview.png'))
        self.save_model()

