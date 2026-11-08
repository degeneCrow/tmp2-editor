from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import(
  QTableWidget, QTableWidgetItem, QComboBox,
)

from trivia_editor.views.components.database_table import BaseGameTable
from trivia_editor.models.basic_question import Question

class BaseGameQuestionTable(BaseGameTable):
  HEADERS = [
    "ID",
    "Question",
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Correct choice",
  ]

  NON_EDITABLE_COLUMNS = {0}

  COLUMN_WIDTHS = [80, 400, 150, 150, 150, 150, 100]

  def __init__(self, parent=None):
    super().__init__(parent)

  def refresh(self, questions: list[Question]):
    # remove all existing entries
    self.table.setRowCount(0)

    for question in questions:
      # calculating temp id of "correct answer"
      correct_answers = [
        index + 1
        for index, choice in enumerate(question.choices)
        if choice.correct
      ]
      the_answer = correct_answers[0] if correct_answers else 0

      choices = [c.text for c in question.choices]
      choices.extend([""] * (4 - len(choices)))

      this_row = self.table.rowCount()
      self.table.insertRow(this_row)

      values = [
        question.id,
        question.text,
        *choices,
      ]

      for column, value in enumerate(values):
        cell = QTableWidgetItem(str(value))
        if column == 0: # making ID column not editable
          cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(this_row, column, cell)

      correct_cb = QComboBox()
      correct_cb.addItems(["0", "1", "2", "3", "4"])
      cb_model = correct_cb.model()
      cb_model.item(0).setEnabled(False)
      correct_cb.setCurrentIndex(the_answer)
      correct_cb.currentIndexChanged.connect(
        lambda _index, row=this_row: self._on_correct_choice_changed(this_row)
      )
      self.table.setCellWidget(this_row, 6, correct_cb)

  # a tiny helper method to link combobox edit to table edit
  def _on_correct_choice_changed(self, row: int):
    # this is bad but eeeeeeeeeh
    cell = self.table.item(row, 1)
    self.table.itemChanged.emit(cell)

