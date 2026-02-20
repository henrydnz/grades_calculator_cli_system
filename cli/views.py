from cli.formatting import (
    console_print, 
    bold,
    sep, 
    title, 
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

def view_options(options, enter_icon="<=="):
    emphasis = "bold yellow"
    format_op = lambda i: f"[{emphasis}]{i}[/{emphasis}]"
    tab = " "*2
    sep()
    for i, s in enumerate(options, 1):
        console_print(f"{tab}{format_op(f"{i}.")} {s}")
    sep()
    console_print(f"\n{format_op(f"{enter_icon} [Enter]")}")

def view_edit_grades_menu(options, subject: Subject):
    title(f"edicao de notas - {subject.name}")
    display_grades(subject)
    view_options(options)

def view_subject_menu(subject_options: list[str], subject: Subject):
    title(f"{subject.name} - resumo")
    display_subject_summary(subject)
    view_options(subject_options)

def view_subject_selection_menu(subject_list: list[str]):
    title("selecionar materia")
    view_options(subject_list)

def view_main_menu(options, filename):
    title("grade calc system - main menu")
    console_print(f"[green]>[/green] Save atual: [green]{filename}[/green]\n")
    view_options(options)

def view_save_menu(options):
    title("grade calc system - save menu")
    view_options(options, enter_icon="Sair")

def view_save_selection_menu(file_list: list[str]) -> str | None:
    title("carregar save")
    view_options(file_list)

def view_delete_save_menu(file_list: list[str]):
    title("deletar save")
    view_options(file_list)