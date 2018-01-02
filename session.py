import os
import sqlite3
from config import MODEL_FILENAME, DB_FILENAME, PREVIEW_FILENAME
from simulator.memory.database import Database


def init_session(session_path, session_config, conv_configs, dense_configs):
    from simulator.agent.model import build_network_from_layers_config, plot_model
    from simulator.memory.db_commands import commit_db_schema

    model = build_network_from_layers_config(session_config, conv_configs, dense_configs)
    plot_model(os.path.join(session_path, PREVIEW_FILENAME), model)
    model.save(os.path.join(session_path, MODEL_FILENAME))

    with sqlite3.connect(os.path.join(session_path, DB_FILENAME)) as db_conn:
        commit_db_schema(db_conn)


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
        from simulator.agent.model import load_model

        self.db_conn = sqlite3.connect(self.db_path)
        self.model = load_model(self.model_path)
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

