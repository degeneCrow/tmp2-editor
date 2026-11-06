from dataclasses import dataclass

@dataclass
class Choice:
  text: str
  correct: bool

@dataclass
class Question:
  id: int
  # this is the question that is displayed
  text: str
  # no explanation needed
  choices: list[Choice]
  # the following 3 are for in-game subtitles i think?
  # maybe also a check on if there is an intro/outro to play?
  introAudio: str | None = None
  questionAudio: str | None = None
  outro: str | None = None

  #btw, the first fifth of questions don't even have these set for some reason

  # checks if this is a us-centric question
  us: bool = False
  # what is this for???
  x: bool = False
