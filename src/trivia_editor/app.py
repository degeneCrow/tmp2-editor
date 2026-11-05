from trivia_editor.controllers.base_questions_controller import BaseQuestionsController
from trivia_editor.views.base_questions_view import BaseQuestionsView
from trivia_editor.services.question_store import QuestionStore
from trivia_editor.views.final_round_view import FinalRoundView
from trivia_editor.views.main_window import MainWindow

class AppController:
  def __init__(self):
    self.base_questions = BaseQuestionsController(BaseQuestionsView(), QuestionStore())

    self.window = MainWindow(views=[
      ("Base Game Questions", self.base_questions.view),
      ("Final Round Questions", FinalRoundView()),
    ])

  def show(self):
    self.window.show()
