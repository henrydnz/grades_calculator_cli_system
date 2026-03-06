from re import findall

def get_variables(formula: str) -> list[str]:
    """ 
    Extrai as variáveis de uma fórmula e retorna numa lista
    """
    return sorted(set(findall(
        r"\b[a-zA-Z_]\w*\b",
        formula
    )))

def validate_formula(formula: str) -> tuple[bool, str]:
    """
    Tenta validar uma fórmula e retorna uma string de erro em caso de falha.
    """
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