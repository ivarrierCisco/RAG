from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QLineEdit
from services.product_query_service import ProductQueryService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cisco Product Query")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter your SPARQL query here...")
        self.layout.addWidget(self.query_input)

        self.query_button = QPushButton("Run Query", self)
        self.query_button.clicked.connect(self.run_query)
        self.layout.addWidget(self.query_button)

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.layout.addWidget(self.result_display)

        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

        self.product_query_service = ProductQueryService()

    def run_query(self):
        query = self.query_input.text()
        if query:
            self.status_label.setText("Running query...")
            result = self.product_query_service.query_products(query)
            self.result_display.setPlainText(result)
            self.status_label.setText("Query completed.")
        else:
            self.status_label.setText("Please enter a query.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())