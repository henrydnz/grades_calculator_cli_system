from cli.formatting import (
    pause, 
    success, 
    title, 
    bold, 
    format_grade, 
    sep, 
    console_print, 
    err
)
from cli.prompts import (
    get_formula, 
    get_grade, 
    get_var, 
    get_new_filename,
    confirm_file_deletion, 
    confirm_subject_deletion
)
from cli.views import display_grades
from core.formula import get_variables
from core.engine import solve_target_grade
from core.save_manager import delete_json, get_path, save_data
from models.subject import Subject
from utils.types_and_constants import Grades, MIN_GRADE

def create_subject(data, filename):
    title("criar materia")

    name = input("Nome da nova matéria (Enter = cancelar): ").strip()
    if not name: return
    
    formula = get_formula()
    detected_vars = get_variables(formula)
    grades: Grades = {v: None for v in detected_vars}
    data[name] = Subject(name, formula, grades)

    print(f"Variaveis detectadas: {", ".join(detected_vars)}")
    save_data(data, filename)
    success("Nova materia salva.")
    pause()

def edit_grade(data, subject, filename):
    title(f"edicao de notas - {subject.name}")

    display_grades(subject)

    sorted_vars = subject.get_sorted_vars()

    console_print(
        "\n" +
        "([bold yellow]1[/bold yellow] - Editar uma nota | " +
        "[bold yellow]2[/bold yellow] - Editar todas as notas | " +
        "[bold yellow]Enter[/bold yellow] - Voltar)"
    )

    op = input()
    match op:
        case "2":
            sep()
            has_changes = False
            for var in sorted_vars:
                query = f"{bold(var)} [{format_grade(subject.grades[var])}]: "
                val = get_grade(query)
                has_changes |= subject.grades[var] != val
                subject.set_grade(var, val)
            sep()

            if has_changes:
                save_data(data, filename)
                success("Alteracoes salvas.")
                pause()
                return
            
            print("Sem mudancas.")
            pause()
            return False
        case "1":
            sep()
            query = "Insira a variavel que deseja editar: "
            var = get_var(subject.get_sorted_vars(), query)

            query = "Insira a nova nota: "
            val = get_grade(query, allow_empty=True)
            sep()

            if subject.grades[var] != val:
                subject.set_grade(var, val)
                success("Alteracao salva.")
                pause()
                return True
            
            print("Sem mudancas.")
            pause()
            return False
        
        case "":
            return False
        
        case _:
            err("Opcao invalida.")
            pause()
            return False
        
def solver(subject) -> None:
    title(f"calcular variavel - {subject.name}")

    missing_grades = subject.get_missing_grades()

    if not missing_grades:
        err("Todas as notas preenchidas. Nao ha variavel para calcular")
        pause()
        return
    
    if subject.has_passed():
        err(f"Ja foi aprovado em {subject.name}. Nao ha o que calcular.")
        pause()
        return

    
    display_grades(subject)
    sep()

    simulation_grades = subject.get_filled_grades().copy()
    if len(missing_grades) > 1:
        target = get_var(missing_grades, "Insira a variavel que quer calcular: ")
        other_missing = [n for n in missing_grades if n != target]
        if len(other_missing) > 1:
            print("Insira hipoteses para as notas faltantes...")
            for other in other_missing:
                simulation_grades[other] = get_grade(f"{other}: ", allow_empty=False)
        else:
            missing = other_missing[0]
            simulation_grades[missing] = get_grade(f"Insira uma hipotese para {missing}: ", allow_empty=False)
    else:
        print(f"Calculando nota minima para {missing_grades[0]}")
        target = missing_grades[0]

    required = solve_target_grade(subject.formula, simulation_grades, target)

    sep()
    console_print(
        f"[red]Impossivel atingir a nota minima...[/red]" if required is None else
        "[green]Ja passou![/green]" if required == MIN_GRADE else
        f"[blue]Meta em {target}: {bold(int(required))}[/blue]"
    )
    pause()

def edit_name(data, subject, filename):
    title("renomear materia")
    old_name = subject.name
    print(f"Nome antigo: {old_name}")
    new_name = input(f"Novo nome (Enter - voltar): ")

    if not new_name or old_name == new_name:
        return
    
    if new_name in data:
        err("Ja existe uma materia com esse nome.")
        pause()
        return
    
    subject = data.pop(old_name)
    subject.name = new_name
    data[new_name] = subject

    save_data(data, filename)
    success(f"Nome alterado para {new_name}.")
    pause()
    

def edit_formula(data, subject, filename):
    title(f"mudar formula de {subject.name}")

    console_print("[red]Atencao:[/red] essa acao pode excluir algumas variaveis dessa materia. Continuar? (s/n)")

    if input() != "s":
        return
    
    old_formula = subject.formula
    print(f"Formula antiga: {old_formula}")

    new_formula = get_formula()

    if new_formula == old_formula:
        return
    
    subject.formula = new_formula
    new_vars = get_variables(new_formula)
    subject.grades = {v: subject.grades.get(v, None) for v in new_vars}

    save_data(data, filename)
    success(f"Formula alterada para: {new_formula}")
    print(f"Variaveis detectadas: {", ".join(new_vars)}")
    pause()
    

def delete_subject(data, subject_name, filename):
    if confirm_subject_deletion(subject_name):
        del data[subject_name]
        save_data(data, filename)
        success(f"Materia [red]\"{subject_name}\"[/red] excluida.")
        pause()
    return True

def create_save():
    title("create save")

    new_filename = get_new_filename()
    if new_filename is None: return

    with open(get_path(new_filename), "w") as f:
        f.write("{}")
    
    success(f"Save [green]\"{new_filename}\"[/green] criado.")
    if input("Selecionar novo save? (s/n) ").strip().lower() == "s":
        return new_filename

def delete_save(filename):    
    if confirm_file_deletion(filename):
        delete_json(filename)
        success(f"Save [red]\"{filename}\"[/red] foi deletado.")
        pause()
    return True