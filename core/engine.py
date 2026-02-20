from models.subject import Subject
from utils.types_and_constants import MIN_GRADE, MAX_GRADE, Grades

def binary_search_target_grade(subject: Subject, target: str) -> float | None:
    low = MIN_GRADE
    high = MAX_GRADE
    required_grade = None

    while low <= high:
        mid = (low + high) // 2
        subject.set_grade(target, float(mid))

        if subject.has_passed():
            required_grade = float(mid)
            high = mid - 1
        else:
            low = mid + 1

    return required_grade


def solve_target_grade(formula: str, grades: Grades, target: str) -> float | None:
    test_subject = Subject("Test", formula, grades.copy())

    test_subject.set_grade(target, MAX_GRADE)
    if not test_subject.has_passed():
        return None

    test_subject.set_grade(target, MIN_GRADE)
    if test_subject.has_passed():
        return MIN_GRADE

    return binary_search_target_grade(test_subject, target)