from PySide6.QtWidgets import QMenu

class ExportMenu(QMenu):
    def __init__(self):
        super().__init__("Export")
        _ = self.addAction("Trade History")
        _ = self.addAction("Trading Journal")
        _ = self.addAction("System Log")