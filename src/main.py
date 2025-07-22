from gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication()
window = MainWindow()
window.show()
app.exec()