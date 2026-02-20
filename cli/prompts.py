
from typing import Callable

from cli.formatting import err, clr_scr, console_print, itemize, title, pause
from models.subject import Subject

from core.formula import validate_formula
from core.save_manager import file_exists, list_saves

def get_formula() -> str:
    while True:
        formula = input("Formula: ")
        is_valid, msg = validate_formula(formula)
        if is_valid: return formula
        err(msg)

def get_grade(q, allow_empty = True) -> float | None:
    console_print(q, end="")
    while True:
        user_input = input().strip()
        if not user_input: 
            if allow_empty:
                return None
            err("Valor necessario!")
            continue
        try:
            val = float(user_input)
            if 0 <= val <= 100: return val
            err("Valor deve ser 0-100.")
        except ValueError:
            err("Nao eh numero.")
        print("Tente novamente: ", end="")

def get_var(vars: list[str], q) -> str:
    console_print(q, end="")
    while True:
        user_input = input().strip().lower()
        var = next((k for k in vars if k.lower() == user_input), None)
        if var: return var
        err("Variavel invalida ou inexistente. Tente novamente:")

def get_new_filename() -> str | None:
    itemize(list_saves(), emphasis=False)
    print()
    while True:
        name = input("Digite o nome do novo save (Enter = cancelar): ")

        if not name: 
            return None
        
        if not name.endswith(".json"):
            name += ".json"

        if not file_exists(name): 
            return name
        
        err("Um save com esse nome ja existe!")



def get_option(option_length):
    while True: 
        op = input("\n>> ").strip()

        valid_digit = op.isdigit() and int(op)-1 in range(option_length)
        enter = op == ""

        if valid_digit or enter:
            return op
        
        err("Opcao invalida.")

def confirm_file_deletion(filename):
    console_print(
        f"[red]Voce tem certeza que deseja deletar o save [bold]\"{filename}\"[/bold] permanentemente?\n" + 
        "Essa acao nao pode ser desfeita![/red]"
    )
    return input("Digite \"sim\" para confirmar: ").strip().lower() == "sim"

def confirm_subject_deletion(subject_name):
    console_print(
        f"[red]Voce tem certeza que deseja deletar a materia [bold]\"{subject_name}\"[/bold] permanentemente?\n" + 
        "Essa acao nao pode ser desfeita![/red]"
    )
    return input("Digite \"sim\" para confirmar: ").strip().lower() == "sim"

def run_menu(options_factory: Callable, show_function: Callable):
    while True: 
        options = options_factory()

        if not options:
            show_function([])
            return 
        
        labels = list(options.keys())
        actions = list(options.values())

        show_function(labels)

        choice = get_option(len(options))
        if not choice: return

        exit = actions[int(choice) - 1]()
        if exit: return 


        