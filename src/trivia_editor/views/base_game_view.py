from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import(
  QLabel, QPushButton,
  QVBoxLayout, QHBoxLayout, QStackedLayout,
  QWidget, QTabWidget,
  QFileDialog, QMessageBox
)

from trivia_editor.models.basic_question import Question,Choice
from trivia_editor.views.base_game_question_table import BaseGameQuestionTable
from trivia_editor.views.base_game_audio_table import BaseGameAudioTable

class BaseGameView(QWidget):
  s_load_active = Signal()
  s_load_custom = Signal(str)
  s_save_active = Signal()
  s_save_custom = Signal(str)
  s_add_question = Signal()
  s_del_question = Signal(int)

  TC_BUTTONS = [
    (
      "Load active question set",
      "Read the question database that the game would load if you ran it now",
      "s_load_active"
    ),
    (
      "Load question set...",
      "Pick the question database to edit (make sure it's for the base game!)",
      "_choose_custom_db_to_load"
    ),
    (
      "Save as Active",
      "Save the current question database as the one the game would load if you ran it now",
      "s_save_active"
    ),
    (
      "Save as...",
      "Save the current question database with a custom name; useful for testing and iteration",
      "_choose_custom_db_to_save"
    ),
    (
      "Add question",
      "Insert a new row of questions at the end of the database",
      "s_add_question"
    ),
    (
      "Delete question",
      "Remove the selected question from the database",
      "_remove_selected_question"
    ),
  ]

  ERROR_HIGHLIGHT = QColor('#dd6969')

  def __init__(self, parent=None):
    super().__init__(parent)

    # main container for the temp text AND tables & controls
    self.pages = QStackedLayout(self)

    # Placeholder content page
    self.placeholder_page = QWidget()
    p_layout = QVBoxLayout(self.placeholder_page)
    self.p_widget = QLabel("Select game folder to load questions!")
    p_layout.addWidget(self.p_widget)
    # adding page to main layout
    self.pages.addWidget(self.placeholder_page)

    # main content page
    self.content_page = QWidget()
    c_layout = QHBoxLayout(self.content_page)

    self.question_tab = BaseGameQuestionTable()
    self.audio_tab = BaseGameAudioTable()

    self.content_tabs = QTabWidget()
    self.content_tabs.addTab(self.question_tab, "Questions")
    self.content_tabs.addTab(self.audio_tab, "Audio files")
    c_layout.addWidget(self.content_tabs)

    self.table_controls = QWidget()
    tc_layout = QVBoxLayout(self.table_controls)
    tc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    for text, tooltip, signal_name in self.TC_BUTTONS:
      button = QPushButton(text)
      button.setToolTip(tooltip)
      button.clicked.connect(getattr(self, signal_name))
      tc_layout.addWidget(button)
    c_layout.addWidget(self.table_controls)

    # adding page to main layout
    self.pages.addWidget(self.content_page)

  def _choose_custom_db_to_load(self):
    path, _ = QFileDialog.getOpenFileName(
      self,
      "Load question database",
      "",
      "Trivia Murder Party Question databases (*.jet);;All files (*)",
    )
    if path:  # Empty when cancelled
      self.s_load_custom.emit(path)

  def _choose_custom_db_to_save(self):
    path, _ = QFileDialog.getSaveFileName(
      self,
      "Save question database",
      "",
      "Trivia Murder Party Question databases (*.jet)",
    )
    if path:  # Empty when cancelled
      #making sure the right extension is set
      if not path.lower().endswith(".jet"):
        path += ".jet"
      self.s_save_custom.emit(path)

  def _remove_selected_question(self):
    # first, check which tab is active/visible
    table = (
      self.question_tab.table
      if self.content_tabs.currentWidget() is self.question_tab
      else self.audio_tab.table
    )
    # then, get selected item/row from THAT table
    selected = table.selectedItems()
    if not selected:
        return
    row = selected[0].row()
    q_id = int(table.item(row, 0).text())
    # pass id to the controller
    self.s_del_question.emit(q_id)

  def refresh(self, questions : list[Question]):
    tables = (self.question_tab.table, self.audio_tab.table)
    try:
      # hide the tables
      self.pages.setCurrentWidget(self.placeholder_page)
      self.p_widget.setText("Refreshing question database, please wait...")

      # stop all inputs while refresh is happening
      for table in tables:
        table.blockSignals(True)
        table.setEnabled(False)

      # actually INITIATE refresh
      self.question_tab.refresh(questions)
      self.audio_tab.refresh(questions)

    # clear any accidental edits that happened so far, and re-enable inputs
    finally:
      for table in tables:
        table.clearSelection()
        table.clearFocus()
        table.setEnabled(True)
        table.blockSignals(False)
      # display the tables
      self.pages.setCurrentWidget(self.content_page)

  def highlight_errors(self, errors: dict[int, list[str]]):
    print("error highlighting called")
    # highlight rows in both child tables
    self.question_tab.highlight_errors(errors)
    self.audio_tab.highlight_errors(errors)
    # display global-ish warning for user
    QMessageBox.warning(
        self,
        "Question errors!",
        f"The following questions have errors:\n - {"\n - ".join(str(q_id) for q_id in errors)}"
    )
