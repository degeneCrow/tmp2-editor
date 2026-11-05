from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from trivia_editor.views.questions_view import QuestionsView
from trivia_editor.views.final_round_view import FinalRoundView
from trivia_editor.views.components.game_folder_selector import GameFolderSelector

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("\"Trivia Murder Party 2\" Question Library Editor")
    self.resize(1000, 500)

    tabs = QTabWidget()
    tabs.addTab(QuestionsView(), "Base Game Questions")
    tabs.addTab(FinalRoundView(), "Final Round")

    # adding the game folder selector up top
    content = QWidget()

    layout = QVBoxLayout(content)
    layout.addWidget(GameFolderSelector())
    layout.addWidget(tabs)

    self.setCentralWidget(content)
