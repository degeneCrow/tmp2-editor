from pathlib import Path

from PySide6.QtWidgets import QTableWidgetItem

from trivia_editor.models.basic_question import Choice
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
    self._view.table.itemChanged.connect(self._on_table_item_changed)
    self._view.s_save_active.connect(self.save_questions)
    self._view.s_save_custom.connect(self.save_custom_questions)
    self._view.s_del_question.connect(self.del_question)
    self._view.s_add_question.connect(self.add_question)

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



  def _on_table_item_changed(self, item : QTableWidgetItem):
    if not item:
      return

    # figure out what question was actually changed
    t_row = item.row()

    # collect ALL the props
    q_id = int(self._view.table.item(t_row, 0).text())
    q_text = self._view.table.item(t_row, 1).text()
    q_answers = [
      item.text() if item is not None else ""
      for item in [
        self._view.table.item(t_row, col) for col in range(2, 6)
      ]
    ]
    q_corr_ans_id = self._view.table.cellWidget(t_row, 6).currentIndex() - 1
    q_choices = [
      Choice(
        text = text,
        # figure out a funky way to check if int of the last dropdown refers to this answer
        correct = (index == q_corr_ans_id)
      )
      for index, text in enumerate(q_answers)
    ]

    # this is the wrong basket, but i'm too tired to make a new one
    q_updated = Question(
      id=q_id,
      text=q_text,
      choices=q_choices
    )

    self.store.update_question_from_table(q_updated)

