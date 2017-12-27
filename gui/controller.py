from gui.session_select_window import SessionSelectWindow


class Controller:
    def __init__(self):
        self._current_window = SessionSelectWindow(callback=self.show_session_window)

    def show_session_window(self, session_path):
        self._current_window.quit()