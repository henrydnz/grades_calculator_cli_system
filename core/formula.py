from re import findall

def get_variables(formula: str) -> list[str]:
    return sorted(set(findall(r"\b[a-zA-Z_]\w*\b", formula)))

def validate_formula(formula: str) -> tuple[bool, str]:
    try:
        default_grades = {v: 1.0 for v in get_variables(formula)}
        eval(formula, {"__builtins__": None}, default_grades)
        return True, ""
    except SyntaxError:
        return False, "Erro de Sintaxe (parênteses desbalanceados ou operador errado?)"
    except NameError as e:
        return False, f"Variável desconhecida na fórmula: {e}"
    except ZeroDivisionError:
        return False, "Divisão por zero detectada."
    except Exception as e:
        return False, f"Erro genérico: {e}"