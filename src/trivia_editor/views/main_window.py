from collections.abc import Iterable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from trivia_editor.views.base_questions_view import BaseQuestionsView
from trivia_editor.views.final_round_view import FinalRoundView
from trivia_editor.views.components.game_folder_selector import GameFolderSelector

class MainWindow(QMainWindow):
  def __init__(self, views: Iterable[tuple[str, QWidget]]):
    super().__init__()
    self.setWindowTitle("\"Trivia Murder Party 2\" Question Library Editor")
    self.resize(1000, 500)

    content = QWidget()
    layout = QVBoxLayout(content)

    # adding the game folder selector up top
    layout.addWidget(GameFolderSelector())

    tabs = QTabWidget()
    for tab_title, view in views:
      tabs.addTab(view, tab_title)
    layout.addWidget(tabs)

    self.setCentralWidget(content)
