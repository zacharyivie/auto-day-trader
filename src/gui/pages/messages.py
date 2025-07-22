from PySide6.QtWidgets import QWidget, QLabel,QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QListWidget

class MessagesPage(QWidget):
    def __init__(self):
        super().__init__()
        filter_options: QHBoxLayout = self.create_filter_options()
        messages_label: QLabel = QLabel("Messages")
        messages_log: QListWidget = self.create_messages_log()
        layout = QVBoxLayout()
        layout.addLayout(filter_options)
        layout.addWidget(messages_label)
        layout.addWidget(messages_log)
        self.setLayout(layout)
        
    def create_filter_options(self):
        options = QButtonGroup()
        options.setExclusive(True)
        all_button = QRadioButton("All")
        trades_button = QRadioButton("Trades")
        cot_button = QRadioButton("CoT")
        system_button = QRadioButton("System")
        options.addButton(all_button)
        options.addButton(trades_button)
        options.addButton(cot_button)
        options.addButton(system_button)
        filter_options = QHBoxLayout()
        filter_options.addWidget(all_button)
        filter_options.addWidget(trades_button)
        filter_options.addWidget(cot_button)
        filter_options.addWidget(system_button)
        return filter_options
    
    def create_messages_log(self):
        messages_list = QListWidget()
        for i in range(100):
            messages_list.addItem(f"Message {i}")
        return messages_list
        