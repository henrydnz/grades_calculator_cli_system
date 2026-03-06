"""
Core funcitons for the solver function
"""

from models.subject import Subject
from utils.types_and_constants import MIN_GRADE, MAX_GRADE, Grades

def binary_search_target_grade(test_subject: Subject, target: str) -> float | None:

    """
    Busca binária da nota mínima necessária da variavel target para a aprovação.
    """

    low = MIN_GRADE
    high = MAX_GRADE
    required_grade = None

    while low <= high:
        mid = (low + high) // 2
        test_subject.grades[target] = float(mid)

        if test_subject.has_passed():
            required_grade = float(mid)
            high = mid - 1
        else:
            low = mid + 1

    return required_grade

def solve_target_grade(formula: str, simulation_grades: Grades, target: str) -> float | None:

    """ 
    Retorna a nota mínima requerida da variavel target para a aprovação na matéria.
    
    1. testa se passa com nota máxima em target. 
    Caso não passe, é impossível passar. Retorna None.

    2. testa se passa com nota mínima em target. 
    Se passa, retorna a nota mínima.

    3. retorna a busca binária da nota mínima aprovável para a variável target.
    """

    test_subject = Subject("Test", formula, simulation_grades.copy())

    test_subject.grades[target] = MAX_GRADE
    if not test_subject.has_passed():
        return None

    test_subject.grades[target] = MIN_GRADE
    if test_subject.has_passed():
        return MIN_GRADE

    return binary_search_target_grade(test_subject, target)
