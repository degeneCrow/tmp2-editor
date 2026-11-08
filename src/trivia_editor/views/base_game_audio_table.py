from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import(
  QTableWidget, QTableWidgetItem,
)

from trivia_editor.views.components.database_table import BaseGameTable
from trivia_editor.models.basic_question import Question

class BaseGameAudioTable(BaseGameTable):
  HEADERS = [
    "ID",
    "Question",
    "Question subtitle",
    # "Question audio",
    "Intro subtitle",
    # "Intro audio",
    "Outro subtitle",
    # "Outro audio",
  ]

  NON_EDITABLE_COLUMNS = {0}

  COLUMN_WIDTHS = [80, 400, 400, 400, 400]

  def __init__(self, parent=None):
    super().__init__(parent)

  def refresh(self, questions: list[Question]):
    # remove all existing entries
    self.table.setRowCount(0)

    for q in questions:
      this_row = self.table.rowCount()
      self.table.insertRow(this_row)

      ###########
      ########### CHANGE THIS LATER
      ###########
      values = [
        q.id,
        q.text,
        q.questionAudio,
        q.introAudio,
        q.outro,
      ]

      for col_nr, value in enumerate(values):
        cell = QTableWidgetItem(str(value))
        if col_nr < 2: # making ID & question columns not editable
          cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(this_row, col_nr, cell)
      ###########
      ########### CHANGE THIS LATER
      ###########


