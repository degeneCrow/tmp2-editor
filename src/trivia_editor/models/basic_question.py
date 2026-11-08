from dataclasses import dataclass, field

@dataclass
class Choice:
  text: str = ""
  correct: bool = False

@dataclass
class Question:
  # it's actually a string,
  # but we're parsing it as an int
  id: int = -1
  # this is the question that is displayed
  text: str = ""
  # no explanation needed
  choices: list[Choice] = field(default_factory=list)
  # the following 3 are for in-game subtitles i think?
  # maybe also a check on if there is an intro/outro to play?
  introAudio: str | None = None
  questionAudio: str = ""
  outro: str | None = None

  #btw, the first fifth of questions don't even have these set for some reason

  # checks if this is a us-centric question
  us: bool = False
  # what is this for???
  x: bool = False
