import json
from pathlib import Path

from trivia_editor.models.basic_question import Choice,Question

class QuestionStore:
  def __init__(self):
    self.questions: list[Question] = []

  def load_questions(self, file_path: Path):
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
