"""
Algumas ações chamadas pelas opções dos menus (lambda).

Retorno das ações: 
- None | False: Mantém o fluxo no menu de origem da ação
- True: Retorna ao menu anterior ao menu contendo a ação.
"""

from cli.formatting import pause, success, title
from cli.prompts import (
    get_formula, get_new_filename,
    confirm_file_deletion, 
    confirm_subject_deletion,
    build_simulation, get_new_grades, 
    prompt_grade_edit, prompt_name_edit,
    prompt_formula_edit
)
from cli.views import view_solver_result, view_solver
from core.solver import solve_target_grade
from core.save_manager import delete_json, get_path, save_data
from core.subject_manager import change_subject_name, add_subject, change_subject_formula
from models.subject import Subject
from typing import Literal

# main menu > criar nova matéria
def create_subject(data, filename) -> None:
    title("criar nova materia")

    name = input("Nome da nova matéria (Enter = cancelar): ").strip()
    if not name: 
        return 

    formula = get_formula()

    add_subject(data, filename, name, formula)

# materia - resumo > editar notas
def edit_grade(data, subject, filename, op) -> Literal[True]:
    # editar uma nota
    if op == 1:
        var, val = prompt_grade_edit(subject.get_sorted_vars())
        if subject.grades[var] != val:
            subject.grades[var] = val
            save_data(data, filename)

    # editar todas as notas
    if op == 2:
        new_grades, has_changes = get_new_grades(subject)    
        if has_changes:
            subject.grades = new_grades
            save_data(data, filename)

    return True

# materia - resumo > calcular variavel   
def solver(subject: Subject) -> None:
    missing_grades = subject.get_missing_grades()
    view_solver(subject, missing_grades)

    if not missing_grades or subject.has_passed(): 
        return

    simulation_grades, target = build_simulation(
        subject.get_filled_grades().copy(), 
        missing_grades
    )
    
    view_solver_result(
        solve_target_grade(subject.formula, simulation_grades, target), 
        target
    )

# materia - resumo > editar nome
def edit_name(data, subject, filename) -> None:
    old_name = subject.name
    new_name = prompt_name_edit(data, old_name)
    
    change_subject_name(data, filename, subject, old_name, new_name)
    
# materia - resumo > editar formula
def edit_formula(data, subject, filename) -> None:
    old_formula = subject.formula
    new_formula = prompt_formula_edit(subject.name, old_formula)

    change_subject_formula(data, filename, subject, old_formula, new_formula)

# materia - resumo > deletar materia
def delete_subject(data, subject_name, filename) -> Literal[True]:
    if confirm_subject_deletion(subject_name):
        del data[subject_name]
        save_data(data, filename)

    return True

# save menu > criar arquivo
def create_save() -> None:
    title("create save")

    new_filename = get_new_filename()
    if new_filename is None: 
        return

    with open(get_path(new_filename), "w") as f:
        f.write("{}")

# save menu > deletar arquivo
def delete_save(filename) -> Literal[True]:    
    if confirm_file_deletion(filename):
        delete_json(filename)
        
    return True