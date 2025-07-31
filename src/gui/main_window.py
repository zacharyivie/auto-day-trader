from inferencing.generator import Generator
from PySide6.QtWidgets import QMainWindow
from gui.menu_bar import MenuBar
from gui.page_manager import PageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Day Trader")
        self.setFixedSize(800, 600)
        self.generator: Generator = Generator()
        self.setMenuBar(MenuBar())
        self.setCentralWidget(PageManager())
        