from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTextEdit, QVBoxLayout, QWidget

class QueryInput(QWidget):
    def __init__(self, parent=None):
        super(QueryInput, self).__init__(parent)
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Enter your SPARQL query:")
        self.query_input = QLineEdit()
        self.submit_button = QPushButton("Submit Query")
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.query_input)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)

class QueryResultDisplay(QWidget):
    def __init__(self, parent=None):
        super(QueryResultDisplay, self).__init__(parent)
        self.layout = QVBoxLayout()
        
        self.result_label = QLabel("Query Results:")
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_display)
        
        self.setLayout(self.layout)

class StatusMessage(QWidget):
    def __init__(self, parent=None):
        super(StatusMessage, self).__init__(parent)
        self.layout = QVBoxLayout()
        
        self.status_label = QLabel("Status:")
        self.status_display = QLabel()
        
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_display)
        
        self.setLayout(self.layout)

    def update_status(self, message):
        self.status_display.setText(message)