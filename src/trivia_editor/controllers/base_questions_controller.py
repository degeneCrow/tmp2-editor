from pathlib import Path

from trivia_editor.views.base_questions_view import BaseQuestionsView
from trivia_editor.services.question_store import QuestionStore

class BaseQuestionsController:
  def __init__(
    self,
    view: BaseQuestionsView,
    store: QuestionStore
  ):
    self.view = view
    self.store = store

  def load_questions(self, game_path):
    file_db_path = Path(game_path + '/content/TDQuestion.jet' )
    self.questions = self.store.load_questions(file_db_path)
    self.view.display_questions(self.store.questions)
