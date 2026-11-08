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
    # create_backup(file_path)

    data = json.loads(file_path.read_text(encoding="utf-8"))

    self.questions = [
      Question(
        id=item.get("id", -1),
        text=item.get("text", ""),
        choices=[
          Choice(
            text=choice.get("text", ""),
            # apparently later they decided to by default assume an option is incorrect???
            correct=choice.get("correct", False)
          )
          for choice in item.get("choices")
        ],
        introAudio=item.get("introAudio", ""),
        questionAudio=item.get("questionAudio", ""),
        outro=item.get("outro", ""),
        us=item.get("us", ""),
        x=item.get("x", ""),
      )
      for item in data["content"]
    ]

  def save_questions(self, file_path: Path):
    data = { "content": [] }

    for q in self.questions:
      choices = []
      for c in q.choices:
        choices.append({
          "text": c.text,
          "correct": c.correct
        })

      data["content"].append({
        "id": q.id,
        "text": q.text,
        "choices": choices,
        "introAudio": q.introAudio,
        "outro": q.outro,
        "questionAudio": q.questionAudio,
        "us": q.us,
        "x": q.x,
      })

    file_path.write_text(
      json.dumps(data, indent=4, ensure_ascii=False) + "\n",
      encoding="utf-8",
    )

  def add_question(self, answer_count:int):
    next_id = max((q.id for q in self.questions), default=0) + 1

    self.questions.append(
      Question(
        id=next_id,
        text="",
        choices=[
          Choice(text="",correct=False) for _ in range(answer_count)
        ],
        introAudio="",
        questionAudio="",
        outro="",
        us=False,
        x=False
      )
    )

  def del_question(self, question_id:int):
    for i, q in enumerate(self.questions):
      if q.id == question_id:
        del self.questions[i]

