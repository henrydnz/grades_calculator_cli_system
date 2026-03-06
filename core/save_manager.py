import os
import json
from utils.types_and_constants import SAVES_DIRECTORY
from models.subject import Subject

def list_saves() -> list[str]:

    """
    Retorna lista de arquivos .json em SAVES_DIRECTORY
    """

    return sorted([
        f for f in os.listdir(SAVES_DIRECTORY) 
        if f.endswith(".json")
    ])

def get_path(filename) -> str: 
    return os.path.join(SAVES_DIRECTORY, filename)

def file_exists(filename) -> bool:
    return os.path.exists(get_path(filename))

def delete_json(name) -> None:   
    os.remove(os.path.join(SAVES_DIRECTORY, name))

def load_data(filename) -> dict[str, Subject]:

    """
    Recebe como argumento um arquivo .json com os dados das matérias. 
    Retorna um dicionário com objetos Subject (Data) contendo esses dados. 
    Se o arquivo não existe ou não pode ser decodificado, retorna um dicionário vazio.
    """

    if not file_exists(filename): 
        return {} 
    
    try: 
        path = get_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f) 

        return {
            name: Subject.from_json(name, info) 
            for name, info in raw_data.items()
        }
    except json.JSONDecodeError:
        return {}

def save_data(subjects: dict[str, Subject], filename) -> None:

    """
    Recebe um dicionário de objetos Subject (Data) e um arquivo .json. 
    Escreve os dados dos objetos no arquivo especificado.
    """

    raw_data = {
        name: s.to_json() 
        for name, s in subjects.items()
    }
    path = get_path(filename)
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(raw_data, f, indent=4, ensure_ascii=False)