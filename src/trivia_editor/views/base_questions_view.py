from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem

from trivia_editor.models.basic_question import Question,Choice

class BaseQuestionsView(QWidget):
  HEADERS = [
    "ID",
    "Question",
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Correct choice",
  ]

  def __init__(self, parent=None):
    super().__init__(parent)

    self.layout = QVBoxLayout(self)

    # default warning text that should be removed after game path loaded?
    self.placeholder = QLabel("Select game folder to load questions!")
    self.layout.addWidget(self.placeholder)

    self.table = QTableWidget(0, len(self.HEADERS), self)
    self.table.setHorizontalHeaderLabels(self.HEADERS)
    self.table.verticalHeader().hide()
    self.layout.addWidget(self.table)
    self.table.hide()

  def refresh_questions(self, questions: list[Question]):
    self.table.setRowCount(0)

    for question in questions:
      if len(question.choices) > 4:
        raise ValueError(
          f"Question {question.id} has {len(question.choices)} choices; expected max of 4."
        )

      # calculating temp id of "correct answer"; also allows to check that only 1 is correct
      correct_positions = [
        index + 1
        for index, choice in enumerate(question.choices)
        if choice.correct
      ]
      if len(correct_positions) != 1:
        raise ValueError(
          f"Question {question.id} must have exactly one correct choice."
        )

      row = self.table.rowCount()
      self.table.insertRow(row)

      values = [
        question.id,
        question.text,
        *(choice.text for choice in question.choices),
        str(correct_positions[0]),
      ]

      for column, value in enumerate(values):
        self.table.setItem(row, column, QTableWidgetItem(str(value)))

    self.table.resizeColumnsToContents()
    self.table.show()

  def display_questions(self, questions: list[Question]):
    self.placeholder.hide()
    self.table.hide()
    self.refresh_questions(questions)

