from typing import Callable
Grades = dict[str, float | None]
Options = dict[str, Callable]

MIN_PASSING_GRADE = 70.0
MIN_GRADE = 0.0
MAX_GRADE = 100.0

SAVES_DIRECTORY = "saves"
DEFAULT_FILE_NAME = "new_save.json"