from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from trivia_editor.app import AppController

def main():
  app = QApplication(sys.argv)
  window = AppController()
  window.show()
  return app.exec()

if __name__ == "__main__":
  sys.exit(main())
