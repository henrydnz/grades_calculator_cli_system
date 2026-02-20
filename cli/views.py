from cli.formatting import (
    console_print, 
    bold,
    sep, 
    title, 
    err, 
    pause,
    format_grade
)
from models.subject import Subject

def display_grades(subject: Subject) -> None:
    tab = " "*2
    print("Notas registradas:")
    for var in subject.get_sorted_vars(): 
        console_print(f"{tab}{var}: {format_grade(subject.grades[var])}")

def display_subject_summary(subject: Subject) -> None:      
    console_print(f"Formula: {subject.formula}")
    console_print(f"Media Atual: {bold(format_grade(int(subject.final_grade())))}")
    console_print(f"Status: {bold(subject.get_status())}\n")
    display_grades(subject)
    print()

def show_options(options, enter_icon="<=="):
    emphasis = "bold yellow"
    format_op = lambda i: f"[{emphasis}]{i}[/{emphasis}]"
    tab = " "*2
    sep()
    for i, s in enumerate(options, 1):
        console_print(f"{tab}{format_op(f"{i}.")} {s}")
    sep()
    console_print(f"\n{format_op(f"{enter_icon} [Enter]")}")

def show_edit_grades_menu(options, subject: Subject):
    title(f"edicao de notas - {subject.name}")
    display_grades(subject)
    show_options(options)

def show_subject_menu(subject_options: list[str], subject: Subject):
    title(f"{subject.name} - resumo")
    display_subject_summary(subject)
    show_options(subject_options)

def show_subject_selection_menu(subject_list: list[str]):
    title("selecionar materia")

    if not subject_list:
        err("Nenhuma materia cadastrada!")
        pause()
        return
    
    show_options(subject_list)

def show_main_menu(options, filename):
    title("grade calc system - main menu")
    console_print(f"[green]>[/green] Save atual: [green]{filename}[/green]\n")
    show_options(options)

def show_save_menu(options):
    title("grade calc system - save menu")
    show_options(options, enter_icon="Sair")

def show_save_selection_menu(file_list: list[str]) -> str | None:
    title("carregar save")

    if not file_list:
        err("Nenhum save existente!")
        print("Crie um save para carregar.")
        pause()
        return

    show_options(file_list)

def show_delete_save_menu(file_list: list[str]):
    title("deletar save")

    if not file_list:
        err("Nenhum save existente!") 
        pause()
        return 
    
    show_options(file_list)