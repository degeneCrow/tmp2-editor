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
        id=int(item.get("id")) or -1,
        text=item.get("text") or "",
        choices=[
          Choice(
            text=choice.get("text") or "",
            correct=choice.get("correct") or False
          )
          for choice in item.get("choices")
        ],
        introAudio=item.get("introAudio"), # can be null
        questionAudio=item.get("questionAudio") or "",
        outro=item.get("outro"), # can be null
        us=item.get("us") or False,
        x=item.get("x") or False,
      )
      for item in data["content"]
    ]

  def save_questions(self, file_path: Path):
    data = { "content": [] }

    for q in self.questions:
      choices = []
      for c in q.choices:
        choices.append({
          "correct": c.correct,
          "text": str(c.text),
        })

      data["content"].append({
        "choices": choices,
        "id": str(q.id),
        # these two can be either string or null, so no special parsing
        "introAudio": q.introAudio,
        "outro": q.outro,
        "questionAudio": str(q.questionAudio),
        "text": str(q.text),
        # i am PRAYING nowhere in the code they are set as strings
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

  def update_question_from_table(self, q_updated:Question):
    for q_original in self.questions:
      if q_original.id != q_updated.id:
        continue
      # found id, now update the other values
      q_original.text = q_updated.text
      q_original.choices = [
        Choice(text=c.text, correct=c.correct)
        for c in q_updated.choices
      ]

  def validate_questions(self) -> dict[int, list[str]]:
    all_errors : dict[int, list[str]] = {}
    seen_ids = set()

    for i, q in enumerate(self.questions):
      errors = []

      # check if ID is unique
      if q.id in seen_ids:
        errors.append(f"Question ID {q.id} is duplicated.")
      seen_ids.add(q.id)

      # check if question has EXACTLY 4 answers
      if len(q.choices) != 4:
        errors.append(f"Question {q.id} must have EXACTLY 4 answers!")
      for j,a in enumerate(q.choices):
        if len(a.text.strip()) == 0:
          errors.append(f"Question {q.id} answer {j+1} needs to have text!")

      # check if question has EXACTLY 1 correct answer
      correct_count = sum(a.correct for a in q.choices)
      if correct_count != 1:
        errors.append(f"Question {q.id} must have one correct answer!!!")

      # if any errors were noticed, add them
      if errors:
        all_errors[i] = errors

    return all_errors
