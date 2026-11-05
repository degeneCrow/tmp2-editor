import json
from pathlib import Path
import shutil

from trivia_editor.models.basic_question import Choice,Question

class QuestionStore:
  def __init__(self):
    self.questions: list[Question] = []

  def create_backup(file_path: Path):
    backup = file_path.with_name(file_path.stem + ".bak" + file_path.suffix)
    number = 1
    while backup.exists():
      backup = file_path.with_name(f"{file_path.stem}.bak{number}{file_path.suffix}")
      number += 1

  def load_questions(self, file_path: Path):
    create_backup(file_path)

    data = json.loads(file_path.read_text(encoding="utf-8"))

    self.questions = [
      Question(
        id=item["id"],
        text=item["text"],
        choices=[
          Choice(
            text=choice["text"],
            # apparently later they decided to by default assume an option is incorrect???
            correct=choice.get("correct", False)
          )
          for choice in item["choices"]
        ],
        introAudio=item.get("introAudio"),
        questionAudio=item.get("questionAudio"),
        outro=item.get("outro"),
        us=item.get("us"),
        x=item.get("x"),
      )
      for item in data["content"]
    ]
