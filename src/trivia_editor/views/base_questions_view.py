from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

class BaseQuestionsView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)
    layout.addWidget(QLabel("Select game folder to load questions!"))
