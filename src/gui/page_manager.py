from gui.pages.messages import MessagesPage
from PySide6.QtWidgets import QTabWidget

class PageManager(QTabWidget):
    def __init__(self):
        super().__init__()
        _ = self.addTab(MessagesPage(), "Messages")