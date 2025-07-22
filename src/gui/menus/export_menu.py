from PySide6.QtWidgets import QMenu

class ExportMenu(QMenu):
    def __init__(self):
        super().__init__("Export")
        self.addAction("Trade History")
        self.addAction("Trading Journal")
        self.addAction("System Log")