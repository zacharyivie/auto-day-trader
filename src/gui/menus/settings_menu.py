from PySide6.QtWidgets import QMenu

class SettingsMenu(QMenu):
    
    def __init__(self):
        super().__init__("Settings")
        self.addAction("My Profile")
        self.addAction("Usage")
        self.addAction("API Keys")