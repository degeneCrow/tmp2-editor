from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
  QFileDialog,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QPushButton,
  QVBoxLayout,
  QWidget,
  QMessageBox
)

class GameFolderSelector(QWidget):
  # to indicate to app at large
  # that a game folder seems to be successfully called
  folder_selected = Signal()

  def __init__(self, parent=None):
    super().__init__(parent)

    self.path_input = QLineEdit()
    self.path_input.setPlaceholderText("Select the game folder…")

    browse_button = QPushButton("Browse…")
    browse_button.clicked.connect(self.choose_folder)

    # place the txt input and folder picker btn in same row
    path_row = QHBoxLayout()
    path_row.addWidget(self.path_input)
    path_row.addWidget(browse_button)

    # adding a label up top
    layout = QVBoxLayout(self)
    layout.addWidget(QLabel("Game folder path (should end with TriviaDeath2)"))
    layout.addLayout(path_row)

  def choose_folder(self):
    # forcing a continuous selection loop until user provides a correct folder
    while True:
      folder = QFileDialog.getExistingDirectory(
        self,
        "Select game folder",
        self.path_input.text(),
      )

      # unless user cancelled manually
      if not folder:
        break

      if not self.is_valid_game_folder(folder):
        QMessageBox.warning(
          self,
          "Invalid game folder",
          "Please select the Trivia Murder Party folder "
          + "(usually located at 'The Jackbox Party Pack 6/games/TriviaDeath2/')",
        )
      else:
        self.path_input.setText(folder)
        self.folder_selected.emit()
        break

  def is_valid_game_folder(self, path=None):
    path = path if path is not None else self.path_input.text().strip()
    return Path(path).name.endswith("TriviaDeath2")

  def game_path(self):
    return self.path_input.text().strip()
