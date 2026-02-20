from cli.formatting import format_grade, console_print, bold, itemize, sep, title, err, pause
from models.subject import Subject

def display_grades(subject: Subject) -> None:
    console_print(bold("Notas registradas:"))
    for var in subject.get_sorted_vars(): 
        grade = format_grade(subject.grades[var])
        console_print(f"{bold(var)}: {grade}")

def display_subject_summary(subject: Subject) -> None:      
    display_grades(subject)
    sep()
    console_print(f"Formula: {bold(subject.formula)}")
    console_print(f"Media Atual: {bold(format_grade(int(subject.final_grade())))}")
    console_print(f"Status: {bold(subject.get_status())}")
    sep()

def show_subject_menu(subject_options: list[str], subject: Subject):
    title(f"{subject.name} - resumo")
    display_subject_summary(subject)
    itemize(subject_options)
    console_print(f"[bold yellow][Enter][/bold yellow]   Voltar (Escolher Materia)") 

def show_subject_selection_menu(subject_list: list[str]):
    title("selecionar materia")

    if not subject_list:
        err("Nenhuma materia cadastrada!")
        pause()
        return
    
    itemize(subject_list)
    console_print(f"[bold yellow][Enter][/bold yellow]   Voltar (Menu Principal)\n") 

def show_main_menu(options, filename):
    title("grade calc system - main menu")
    console_print(f"Save atual: [green]{filename}[/green]\n")
    itemize(options)
    console_print(f"[bold yellow][Enter][/bold yellow]   Voltar (Save Selection)") 

def show_save_menu(options):
    title("grade calc system - save menu")
    itemize(options)
    console_print(f"[bold yellow][Enter][/bold yellow]   Quit")

def show_save_selection_menu(file_list: list[str]) -> str | None:
    title("carregar save")

    if not file_list:
        err("Nenhum save existente!")
        print("Crie um save para carregar.")
        pause()
        return

    itemize(file_list)
    console_print(f"[bold yellow][Enter][/bold yellow]   Voltar (Save Menu)") 

def show_delete_save_menu(file_list: list[str]):
    title("deletar save")

    if not file_list:
        err("Nenhum save existente!") 
        pause()
        return 
    
    itemize(file_list)
    console_print(f"[bold yellow][Enter][/bold yellow]   Voltar (Save Menu)") 