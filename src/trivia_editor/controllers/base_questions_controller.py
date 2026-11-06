from pathlib import Path

from trivia_editor.views.base_questions_view import BaseQuestionsView
from trivia_editor.services.question_store import QuestionStore

class BaseQuestionsController:
  def __init__(
    self,
    view: BaseQuestionsView,
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

  @property
  def view(self) -> Path | None:
    return self._view

  @property
  def store(self) -> Path | None:
    return self._store

  @property
  def game_path(self) -> Path | None:
    return self._game_path

  def set_game_path(self, game_path: str | Path):
    self._game_path = Path(game_path)




  def _load_questions(self):
    self.store.load_questions(self._current_db)
    self.view._display_questions(self.store.questions)

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
    self.store.save_questions(self._current_db)

  def save_custom_questions(self, custom_filepath: str):
    print("custom question saving called!")
    file_db_path = Path(custom_filepath)
    self.store.save_questions(file_db_path)

  def add_question(self):
    print("registering a new question row!")
    self.store.add_question(4)
    self.view._refresh_questions(self.store.questions)

  def del_question(self, q_id : int):
    print("deleting a question from db!")
    self.store.del_question(q_id)
    self.view._refresh_questions(self.store.questions)
