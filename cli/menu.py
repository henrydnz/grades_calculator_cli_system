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
    view_subject_menu, 
    view_subject_selection_menu, 
    view_main_menu, 
    view_save_selection_menu,
    view_save_menu, 
    view_delete_save_menu,
    view_edit_grades_menu
)
from core.save_manager import load_data, list_saves

def edit_grade_menu(data, subject, filename):

    def build_options(): 
        return {
            "Editar uma nota": lambda: edit_one_grade(data, subject, filename),
            "Editar todas as notas": lambda: edit_all_grades(data, subject, filename)
        }
    
    run_menu(build_options, lambda options: view_edit_grades_menu(options, subject))

def subject_menu(data, subject_name, filename):
    subject = data[subject_name]

    def build_options(): 
        return {
            "Calcular Variavel": lambda: solver(subject),
            "Editar Notas": lambda: edit_grade_menu(data, subject, filename),
            "Editar Nome": lambda: edit_name(data, subject, filename),
            "Editar Formula": lambda: edit_formula(data, subject, filename),
            "Excluir Materia": lambda: delete_subject(data, subject.name, filename)
        }

    run_menu(build_options, lambda options: view_subject_menu(options, subject))

def subject_selection_menu(data, filename):
    def build_options(): 
        return {
            sub: (lambda sub=sub: subject_menu(data, sub, filename)) 
            for sub in sorted(list(data.keys()))
        }

    run_menu(build_options, lambda options: view_subject_selection_menu(options))

def main_menu(filename) -> None:
    if not filename: return
    data = load_data(filename)

    def build_options(): 
        options = {
                "Criar Nova Materia": lambda: create_subject(data, filename),
        }

        if data: 
            options["Acessar Materia"] = lambda: subject_selection_menu(data, filename)
        
        return options
    
    run_menu(build_options, lambda options: view_main_menu(options, filename))

def save_selection_menu():
    def build_options(): return {s: (lambda s=s: main_menu(s)) for s in list_saves()}

    run_menu(build_options, lambda options: view_save_selection_menu(options))

def delete_save_menu():
    def build_options(): return {s: (lambda s=s: delete_save(s)) for s in list_saves()}

    run_menu(build_options, lambda options: view_delete_save_menu(options))

def save_menu() -> None:
    

    def build_options():
        options = {
            "Criar Arquivo": lambda: main_menu(create_save())    
        }

        saves = list_saves()
        has_one_save = len(saves) == 1

        if saves: 
            if has_one_save: 
                options[f"Carregar \"{saves[0]}\""] = lambda: main_menu(saves[0])
            else:
                options["Carregar Arquivo"] = lambda: save_selection_menu()
            options["Deletar Arquivo"] = lambda: delete_save_menu()

        return options
    
    run_menu(build_options, lambda options: view_save_menu(options))

