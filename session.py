from config import *
from memory.gamestate_repo import Repo
from training.model import create_network, load_model


class Session:
    def open(self, session_name):
        session_path = os.path.join(SESSIONS_DIR, session_name)
        self.model_path = os.path.join(session_path, 'model.h5')
        self.model_preview_path = os.path.join(session_path, 'model_preview.png')

        if os.path.exists(session_path):
            self.model = load_model(self.model_path)
        else:
            os.makedirs(session_path)
            self.model = create_network(self.model_preview_path)
        self.repo = Repo(session_path)

        return self.model, self.repo

    def save_model(self):
        self.model.save(self.model_path)

