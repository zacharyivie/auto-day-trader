from PySide6.QtWidgets import QMenuBar
from gui.menus.export_menu import ExportMenu
from gui.menus.settings_menu import SettingsMenu

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        _ = self.addMenu(ExportMenu())
        _ = self.addMenu(SettingsMenu())