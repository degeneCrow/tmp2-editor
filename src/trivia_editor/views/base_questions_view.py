from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from trivia_editor.services.question_store import QuestionStore

class BaseQuestionsView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)
    layout.addWidget(QLabel("Select game folder to load questions!"))

  def display_questions(question_store: QuestionStore):
    print("QuestionStore successfully received")
