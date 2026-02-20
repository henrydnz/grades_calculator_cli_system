from cli.actions import (
    delete_subject, 
    solver, 
    create_subject,
    edit_one_grade,
    edit_all_grades,
    edit_name, 
    edit_formula, 
    delete_subject, 
    create_save, 
    delete_save
)
from cli.prompts import run_menu
from cli.views import (
    show_subject_menu, 
    show_subject_selection_menu, 
    show_main_menu, 
    show_save_selection_menu,
    show_save_menu, 
    show_delete_save_menu,
    show_edit_grades_menu
)
from core.save_manager import load_data, list_saves

def edit_grade_menu(data, subject, filename):
    run_menu(
        options_factory=lambda: {
            "Editar uma nota": lambda: edit_one_grade(data, subject, filename),
            "Editar todas as notas": lambda: edit_all_grades(data, subject, filename)
        },
        show_function=lambda options: show_edit_grades_menu(options, subject)
    )

def subject_menu(data, subject_name, filename):
    subject = data[subject_name]

    run_menu(
        options_factory=lambda: {
            "Calcular Variavel": lambda: solver(subject),
            "Editar Notas": lambda: edit_grade_menu(data, subject, filename),
            "Editar Nome": lambda: edit_name(data, subject, filename),
            "Editar Formula": lambda: edit_formula(data, subject, filename),
            "Excluir Materia": lambda: delete_subject(data, subject.name, filename)
        }, 
        show_function=lambda options: show_subject_menu(options, subject)
    )

def subject_selection_menu(data, filename):
    run_menu(
        options_factory=lambda: {
            sub: (lambda sub=sub: subject_menu(data, sub, filename)) 
            for sub in sorted(list(data.keys()))
        }, 
        show_function=lambda options: show_subject_selection_menu(options)
    )

def main_menu(filename) -> None:
    if not filename: return
    data = load_data(filename)
    
    run_menu(
        options_factory=lambda: {
            "Acessar Materia": lambda: subject_selection_menu(data, filename),
            "Criar Nova Materia": lambda: create_subject(data, filename),
        }, 
        show_function=lambda options: show_main_menu(options, filename)
    )

def save_selection_menu():
    run_menu(
        options_factory=lambda: {s: (lambda s=s: main_menu(s)) for s in list_saves()}, 
        show_function=lambda options: show_save_selection_menu(options)
    )

def delete_save_menu():
    run_menu(
        options_factory=lambda: {s: (lambda s=s: delete_save(s)) for s in list_saves()}, 
        show_function=lambda options: show_delete_save_menu(options)
    )

def save_menu() -> None:
    # if theres only one file, starts system on this file
    if len(saves:=list_saves()) == 1: main_menu(saves[0])

    run_menu(
        options_factory=lambda: {
            "Criar Arquivo": lambda: main_menu(create_save()),
            "Carregar Arquivo": lambda:  save_selection_menu(),
            "Deletar Arquivo": lambda: delete_save_menu()
        }, 
        show_function=lambda options: show_save_menu(options)
    )

