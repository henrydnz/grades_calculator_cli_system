""" 
Prompts para receber inputs válidos do usuário.
"""

from cli.formatting import err, console_print, bold, format_grade, sep, title, console_input
from core.formula import validate_formula
from core.save_manager import file_exists
from models.subject import Subject
from utils.types_and_constants import Grades, MIN_GRADE, MAX_GRADE
from typing import Callable

def get_formula() -> str:

    """
    Retorna uma fórmula válida.
    """

    while True:
        formula = input("Formula: ")
        is_valid, msg = validate_formula(formula)
        if is_valid: 
            return formula
        err(msg)

def get_grade(q, allow_empty = True) -> float | None:

    """
    Pede uma nota válida ao usuário. Se allow_empty = True, retorna None ao enviar Enter.
    """ 

    while True:
        user_input = console_input(q).strip()

        if not user_input: 
            if allow_empty: 
                return None

            err("Valor necessario!")
            continue

        try:
            if val := float(user_input) in range(int(MIN_GRADE), int(MAX_GRADE) + 1): 
                return val
            
            err(f"Valor deve ser entre {MIN_GRADE}-{MAX_GRADE}.")

        except ValueError:
            err("Valor deve ser numerico.")

def get_var(q, vars: list[str]) -> str:

    """
    Retorna uma variável eixstente dentro da lista de variáveis vars.
    """

    while True:
        user_input = console_input(q).strip().lower()

        # vê se variável de input existe dentro de vars
        var = next((k for k in vars if k.lower() == user_input), None)
        if var: 
            return var
        
        err("Variavel invalida ou inexistente.")

def get_new_filename() -> str | None:

    """
    Retorna o nome de um novo arquivo JSON válido. Retorna None ao enviar Enter.
    """

    while True:
        name = input("Digite o nome do novo save (Enter = cancelar): ")

        if not name: 
            return None
        
        if not name.endswith(".json"):
            name += ".json"

        if not file_exists(name): 
            return name
        
        err("Um save com esse nome ja existe!")

def get_option(option_length) -> str:

    """
    Retorna uma string numérica contendo uma opção válida em função da quantidade de opções.
    Retorna "" caso o usuário envie Enter
    """

    while True: 
        op = console_input("\n[green]>>[/green] ").strip()

        valid_digit = op.isdigit() and int(op)-1 in range(option_length)
        enter = (op == "")

        if valid_digit or enter:
            return op
        
        err("Opcao invalida.")

def confirm_file_deletion(filename) -> bool:
    console_print(
        f"[red]Voce tem certeza que deseja deletar o save [bold]\"{filename}\"[/bold] permanentemente?\n" + 
        "Essa acao nao pode ser desfeita![/red]"
    )
    return input("Digite \"sim\" para confirmar: ").strip().lower() == "sim"

def confirm_subject_deletion(subject_name) -> bool:
    console_print(
        f"[red]Voce tem certeza que deseja deletar a materia [bold]\"{subject_name}\"[/bold] permanentemente?\n" + 
        "Essa acao nao pode ser desfeita![/red]"
    )
    return input("Digite \"sim\" para confirmar: ").strip().lower() == "sim"

# Chamada em todos os menus.
def run_menu(options_factory: Callable, view: Callable) -> None:
    while True: 
        # Cria as opções do menu dinamicamente.
        options = options_factory()
        
        # Separa descrições e ações.
        labels = list(options.keys())
        actions = list(options.values())

        # Mostra a view do menu com opções.
        view(labels)

        # se usuário presisona enter, volta na linha de fluxo.
        op = get_option(len(options))
        if not op: 
            return

        # executa opção escolhida. Se a ação retorna True, volta na linha de fluxo .
        action_index = int(op) - 1
        exit = actions[action_index]()
        if exit: 
            return 

def build_simulation(filled_grades: Grades, missing_grades: list[str]) -> tuple[Grades, str]:

    """
    Helper para Solver.

    Retorna notas de simulação para o cálculo e a variável target que o usuário deseja calcular. 
    """

    if len(missing_grades) == 1:
        return filled_grades, missing_grades[0]
    
    simulation_grades = filled_grades

    sep()
    target = get_var("Insira a variavel que quer calcular: ", missing_grades)
    print("Insira hipoteses para as notas faltantes...")
    for other_missing in [g for g in missing_grades if g != target]:
        simulation_grades[other_missing] = get_grade(f"{other_missing}: ", allow_empty=False)
    
    return simulation_grades, target

def prompt_grade_edit(sorted_vars: list[str]) -> tuple[str, float | None]:

    """
    Helper para edit_grade.

    Retorna uma variável válida entre sorted_vars e um valor válido (ou None) para a nota.
    """

    var = get_var("\nInsira a variavel que deseja editar: ", sorted_vars)
    val = get_grade("Insira a nova nota: ", allow_empty=True)

    return var, val

def get_new_grades(subject: Subject) -> tuple[Grades, bool]:

    """
    Helper para edit_grade

    Retorna um dicionário de novas notas e um booleano dizendo se tiveram mudanças em relação às notas antigas.
    """

    old_grades: Grades  = subject.grades.copy()
    new_grades: Grades = {}

    has_changes: bool = False

    for var, val in old_grades.items():
        new_val = get_grade(f"{bold(var)} [{format_grade(val)}]: ")
        new_grades[var] = new_val
        has_changes |= val != new_val

    return new_grades, has_changes

def prompt_name_edit(data, old_name) -> None | str:

    """
    Helper para edit_name

    Retorna um novo nome válido para a edição do nome da matéria
    """

    title("renomear materia")
    print(f"Nome antigo: {old_name}")

    while True:
        new_name = input(f"Novo nome (Enter - voltar): ")

        if not new_name or old_name == new_name:
            return None
    
        if new_name not in data:
            return new_name

        err("Ja existe uma materia com esse nome.")

def prompt_formula_edit(subject_name, old_formula):

    """"
    Helper para edit_formula

    Retorna uma fórmula válida para a substituição.
    """

    title(f"mudar formula de {subject_name}")
    print(f"Formula antiga: {old_formula}")
    return get_formula()