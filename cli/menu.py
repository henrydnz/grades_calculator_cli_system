from cli.actions import (
    delete_subject, 
    edit_grade, 
    solver, 
    create_subject,
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
    show_delete_save_menu
)
from core.save_manager import load_data, list_saves

def subject_menu(data, subject_name, filename):
    subject = data[subject_name]

    run_menu(
        options_factory=lambda: {
            "Calcular Variavel": lambda: solver(subject),
            "Editar Notas": lambda: edit_grade(data, subject, filename),
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
            "Create File": lambda: main_menu(create_save()),
            "Load File": lambda:  save_selection_menu(),
            "Delete File": lambda: delete_save_menu()
        }, 
        show_function=lambda options: show_save_menu(options)
    )

