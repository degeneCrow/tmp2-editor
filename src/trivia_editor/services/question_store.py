import json
from pathlib import Path

from trivia_editor.models.basic_question import Choice,Question

class QuestionStore:
  def load_questions(path: Path) -> list[Question]:
    data = json.loads(path.read_text(encoding="utf-8"))

    return [
      Question(
        id=item["id"],
        text=item["text"],
        choices=[
            Choice(text=choice["text"], correct=choice["correct"])
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
