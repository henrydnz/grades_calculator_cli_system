"""
Visualizações e Gráficos.
"""

from cli.formatting import (
    console_print, bold,
    sep, title, pause,
    format_grade, err
)
from models.subject import Subject
from utils.types_and_constants import MIN_GRADE

# MENUS
def view_options(options, enter_icon="<==") -> None:
    sep()
    for i, s in enumerate(options, 1):
        console_print(f"  [bold yellow]{i}.[/bold yellow] {s}")
    sep()
    console_print(f"\n[bold yellow]{enter_icon} [Enter][/bold yellow]")

def view_edit_grades_menu(options, subject: Subject):
    title(f"edicao de notas - {subject.name}")
    list_grades(subject)
    console_print("\n[blue]> Dica:[/blue] Pressione Enter ao editar uma nota para apagá-la.\n")
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

# OUTROS
def list_grades(subject: Subject) -> None:
    print("Notas registradas:")
    for var in subject.get_sorted_vars(): 
        console_print(f"  {var}: {format_grade(subject.grades[var])}")

def display_subject_summary(subject: Subject) -> None:      
    console_print(
        f"Formula: {subject.formula}\n" +
        f"Media Atual: {bold(format_grade(subject.final_grade()))}" +
        f"Status: {bold(subject.get_status())}\n"
    )
    list_grades(subject)
    print()



def view_solver(subject, missing_grades):
    title(f"calcular variavel - {subject.name}")    

    if not missing_grades:
        err("Todas as notas preenchidas. Nao ha variavel para calcular")
        pause()
        return
    
    if subject.has_passed():
        err(f"Ja foi aprovado em {subject.name}. Nao ha o que calcular.")
        pause()
        return

    list_grades(subject)

def view_solver_result(required, target):
    sep()
    print(f"Calculando a variável ({target}):")

    reprovou = f"[red]Impossivel passar...[/red]"
    passou = "[green]Passou.[/green]"
    meta = f"[blue]Meta: {bold(int(required))}[/blue]"

    console_print(
        reprovou if required is None 
        else passou if required == MIN_GRADE
        else meta
    )
    pause()