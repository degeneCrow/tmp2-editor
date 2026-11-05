from pathlib import Path

from trivia_editor.controllers.base_questions_controller import BaseQuestionsController
from trivia_editor.views.base_questions_view import BaseQuestionsView
from trivia_editor.services.question_store import QuestionStore
from trivia_editor.views.final_round_view import FinalRoundView
from trivia_editor.views.main_window import MainWindow

class AppController:
  def __init__(self):
    self.game_path : Path = None
    self.base_questions = BaseQuestionsController(BaseQuestionsView(), QuestionStore())

    self.window = MainWindow(views=[
      ("Base Game Questions", self.base_questions.view),
      ("Final Round Questions", FinalRoundView()),
    ])


    self.window.game_folder_selector.folder_selected.connect(
      self.on_game_folder_selected
    )

  def show(self):
    self.window.show()

  def on_game_folder_selected(self):
    self.game_path = self.window.game_folder_selector.game_path()
    print(f"Selected game folder: {self.game_path}")

    self.base_questions.load_questions(self.game_path)
