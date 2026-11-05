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

  def load(self, path):
    self.questions = self.store.load_questions(path)
    self.view.display_questions(self.store)
