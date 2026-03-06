from core.save_manager import save_data
from core.formula import get_variables
from utils.types_and_constants import Grades
from models.subject import Subject

def change_subject_name(data, filename, subject, old_name, new_name) -> None: 

    """
    Se o novo nome existir e for diferente do nome antigo, muda o nome da matéria e salva
    """

    if not new_name: return
    subject = data.pop(old_name)
    subject.name = new_name
    data[new_name] = subject
    save_data(data, filename)

def change_subject_formula(data, filename, subject, old_formula, new_formula): 

    """
    Se a fórmula nova for diferente da antiga, atualiza e salve
    """

    if old_formula == new_formula: return 
    subject.formula = new_formula
    new_vars = get_variables(new_formula)
    subject.grades = {v: subject.grades.get(v, None) for v in new_vars}
    save_data(data, filename)

def add_subject(data, filename, name, formula) -> None:

    """
    Adiciona uma matéria nova com os dados e salva.
    """

    detected_vars = get_variables(formula)
    grades: Grades = {v: None for v in detected_vars}
    data[name] = Subject(name, formula, grades)
    save_data(data, filename)

