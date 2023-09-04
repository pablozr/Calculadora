from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs) 
        
        # Basic layout configuration
        self.centralwg = QWidget()
        self.v_layout = QVBoxLayout()
        self.centralwg.setLayout(self.v_layout)
        self.setCentralWidget(self.centralwg)
        self.setWindowTitle('Calculadora')

    def adjust_fixed(self):
        # Adjusting the size, and making it fixed
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def add_widget_to_vlayout(self, widget):
        # Adds Widget to layout
        self.v_layout.addWidget(widget)

    def make_msg_box(self):
        return QMessageBox(self)
      