from PySide6.QtWidgets import QMenuBar
from gui.menus import ExportMenu, SettingsMenu

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.addMenu(ExportMenu())
        self.addMenu(SettingsMenu())