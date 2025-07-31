from PySide6.QtWidgets import QMenu

class SettingsMenu(QMenu):
    
    def __init__(self):
        super().__init__("Settings")
        _ = self.addAction("My Profile")
        _ = self.addAction("Usage")
        _ = self.addAction("API Keys")