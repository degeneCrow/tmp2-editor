from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import(
  QHBoxLayout,
  QWidget, QTableWidget, QTableWidgetItem,
  QPushButton
)

from trivia_editor.views.components.database_table import BaseGameTable
from trivia_editor.models.basic_question import Question

class BaseGameAudioTable(BaseGameTable):
  HEADERS = [
    "ID",
    "Question",
    "Question subtitle",
    "Question audio",
    "Intro subtitle",
    "Intro audio",
    "Outro subtitle",
    "Outro audio",
  ]

  NON_EDITABLE_COLUMNS = {0, 1}

  COLUMN_WIDTHS = [80, 400, 400, 80, 400, 80, 400, 80]

  AUDIO_FILENAMES = {
    "questionAudio" : "questionAudio.ogg",
    "introAudio" : "introAudio.ogg",
    "outro" : "outroAudio.ogg",
  }

  s_play_audio = Signal(str)

  def __init__(self, parent=None):
    super().__init__(parent)

  def refresh(self, questions: list[Question]):
    # remove all existing entries
    self.table.setRowCount(0)

    for q in questions:
      this_row = self.table.rowCount()
      self.table.insertRow(this_row)

      # This is a lot manual that the question table
      # Could probably figure out a way to make it more dynamic,
      # but eh.
      # do it yourself if you want
      c1 = QTableWidgetItem(q.id)
      c1.setFlags(~Qt.ItemIsEditable)
      self.table.setItem(this_row, 0, c1)

      c1 = QTableWidgetItem(q.text)
      c1.setFlags(~Qt.ItemIsEditable)
      self.table.setItem(this_row, 1, c1)

      c1 = QTableWidgetItem(q.questionAudio)
      self.table.setItem(this_row, 2, c1)

      c1 = self._build_audio_controls(q, "questionAudio")
      self.table.setCellWidget(this_row, 3, c1)

      c1 = QTableWidgetItem(q.introAudio)
      self.table.setItem(this_row, 4, c1)

      c1 = self._build_audio_controls(q, "introAudio")
      self.table.setCellWidget(this_row, 5, c1)

      c1 = QTableWidgetItem(q.outro)
      self.table.setItem(this_row, 6, c1)

      c1 = self._build_audio_controls(q, "outro")
      self.table.setCellWidget(this_row, 7, c1)

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

  def _audio_path(self, q_id: int, kind: str) -> str:
    filename = self.AUDIO_FILENAMES[kind]
    return (
      # self.game_path /
      f"content/TDQuestion/{str(q_id)}/{filename}"
    )

  def _build_audio_controls(self, q: Question, audio_type: str) -> QWidget:
    playback_path = self._audio_path(q.id, audio_type)

    container = QWidget()
    layout = QHBoxLayout(container)

    play_button = QPushButton("▶")
    # play_button.setEnabled(playback_path.is_file())
    play_button.clicked.connect(
      lambda _checked=False, path=str(playback_path):
        self.s_play_audio.emit(path)
    )
    replace_btn = QPushButton("📤")
    replace_btn.setEnabled(bool(getattr(q, audio_type, None)))
    replace_btn.clicked.connect(
      lambda _checked=False, q_id=q.id, audio_type=audio_type:
        self._choose_audio_replacement(q_id, audio_type)
    )

    layout.addWidget(play_button)
    layout.addWidget(replace_btn)

    return container

  def _choose_audio_replacement(self, q_id:int, audio_type:str):
    print(f"Picked to replace {audio_type} on {q_id}")
