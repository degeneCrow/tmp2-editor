import os
from pathlib import Path
from mutagen import File
from playsound3 import playsound

from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

from trivia_editor.models.basic_question import Choice
from trivia_editor.views.base_game_view import BaseGameView
from trivia_editor.services.question_store import QuestionStore

class BaseGameController:
  def __init__(
    self,
    view: BaseGameView,
    store: QuestionStore
  ):
    self._view = view
    self._store = store
    self._game_path: Path | None = None
    self._current_db: Path | None = None

    # connecting view signals to controller methods
    self._view.s_load_active.connect(self.load_default_questions)
    self._view.s_load_custom.connect(self.load_custom_questions)
    self._view.s_save_active.connect(self.save_questions)
    self._view.s_save_custom.connect(self.save_custom_questions)
    self._view.s_del_question.connect(self.del_question)
    self._view.s_add_question.connect(self.add_question)

    self._view.question_tab.table.cellChanged.connect(self._on_questions_content_changed)
    self._view.audio_tab.table.cellChanged.connect(self._on_audio_content_changed)

    self._view.audio_tab.s_play_audio.connect(self.play_audio)
    self._view.audio_tab.s_upload_audio.connect(self.replace_audio)

  @property
  def view(self):
    return self._view

  @property
  def store(self):
    return self._store

  @property
  def game_path(self) -> Path | None:
    return self._game_path

  def set_game_path(self, game_path: str | Path):
    self._game_path = Path(game_path)




  def _load_questions(self):
    self.store.load_questions(self._current_db)
    self.view.refresh(self.store.questions)
    # let's also immediately validate the loaded questions
    errors = self.store.validate_questions(self.game_path)
    self.view.highlight_errors(errors)

  def load_default_questions(self):
    print("default question loading called!")
    self._current_db = Path(self.game_path / "content/TDQuestion.jet" )
    self._load_questions()

  def load_custom_questions(self, custom_filepath: str):
    print("custom question loading called!")
    self._current_db = Path(custom_filepath)
    self._load_questions()

  def save_questions(self):
    print("question saving called!")
    errors = self.store.validate_questions(self.game_path)
    # we always run these to clear errors
    self.view.highlight_errors(errors)
    if len(errors) > 0:
      return
    # no errors found, we can save
    self.store.save_questions(self._current_db)

  def save_custom_questions(self, custom_filepath: str):
    print("custom question saving called!")
    file_db_path = Path(custom_filepath)
    errors = self.store.validate_questions(self.game_path)
    # we always run these to clear errors
    self.view.highlight_errors(errors)
    if len(errors) > 0:
      return
    # no errors found, we can save
    self.store.save_questions(file_db_path)

  def add_question(self):
    print("registering a new question row!")
    self.store.add_question(4)
    self.view.refresh(self.store.questions)

  def del_question(self, q_id : int):
    print("deleting a question from db!")
    self.store.del_question(q_id)
    self.view.refresh(self.store.questions)

  def _on_questions_content_changed(self, t_row: int, t_col: int):
    question_table = self.view.question_tab.table

    # collect ALL the props
    q_id = int(question_table.item(t_row, 0).text())
    q_text = question_table.item(t_row, 1).text()
    q_answers = [
      item.text() if item is not None else ""
      for item in [
        question_table.item(t_row, col) for col in range(2, 6)
      ]
    ]
    q_corr_ans_id = question_table.cellWidget(t_row, 6).currentIndex() - 1
    q_choices = [
      Choice(
        text = text,
        correct = (index == q_corr_ans_id)
      )
      for index, text in enumerate(q_answers)
    ]

    self.store.update_from_question_table(q_id, q_text, q_choices)

  def _on_audio_content_changed(self, t_row: int, t_col: int):
    audio_table = self.view.audio_tab.table

    # collect ALL the props
    q_id = int(audio_table.item(t_row, 0).text())
    # user can't edit the question itself here, so we don't care about it
    q_subQuest = str(audio_table.item(t_row, 2).text())
    q_subIntro = str(audio_table.item(t_row, 4).text())
    q_subOutro = str(audio_table.item(t_row, 6).text())

    self.store.update_from_audio_table(q_id, q_subQuest, q_subIntro, q_subOutro)


  def play_audio(self, relative_path:str):
    path = self.game_path/relative_path
    print(f"Called to play {path}")
    # do a quick check on if the file actually exists
    if not path.exists():
      QMessageBox.warning(
          None,
          "Audio errors!",
          f"The following question audio does not have a linked audio file:\n{relative_path}"
      )
      return
    playsound(path, False, None)

  def replace_audio(self, q_id:int, absolute_filepath:str, audio_type:str):
    source = Path(absolute_filepath)
    targetPath = Path(self.game_path/"content/TDQuestion"/str(q_id))
    targetFile = f"{audio_type}.ogg"
    print(f"Picked '{source}' to replace {targetPath/targetFile}")

    # double-check source file
    if not source.exists:
      QMessageBox.warning(
          self,
          "Audio errors!",
          f"The selected file does not exist:\n{source}"
      )
    if not self._is_ogg(source):
      QMessageBox.warning(
          self,
          "Audio errors!",
          f"The selected file is not a proper .ogg file:\n{source}"
      )
    # validation worked
    os.makedirs(targetPath)
    source.replace(targetPath/targetFile)

  def _is_ogg(self, file : Path):
    with open(file, "rb") as f:
      #validates encoding to be an audio file
      if f.read(4) == b"OggS":
        return True
      #else
      return False

