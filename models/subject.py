"""
Modelo para Matéria
"""

from utils.types_and_constants import MIN_PASSING_GRADE, Grades
from dataclasses import dataclass, field

@dataclass
class Subject:

    name: str
    formula: str
    grades: Grades = field(default_factory=dict)

    def to_json(self) -> dict:

        """
        Converte a Data Class Subject para dict type.
        """

        return {
            "formula" : self.formula,
            "notas" : self.grades
        }
    
    @classmethod
    def from_json(cls, name: str, data: dict) -> "Subject":

        """
        Converte um dict de Subject para Data Class.
        """

        return cls(
            name=name,
            formula=data["formula"],
            grades=data.get("notas", {})
        )
    
    def final_grade(self) -> float:
        safe_grades = {k: (v if v is not None else 0.0) for k, v in self.grades.items()}
        return float(eval(self.formula, {"__builtins__": None}, safe_grades))
    
    def has_passed(self) -> bool:
        return self.final_grade() >= MIN_PASSING_GRADE
    
    def get_sorted_vars(self) -> list[str]:
        return sorted(self.grades.keys())

    def get_filled_grades(self) -> Grades: 

        """
        Retorna um dict[str, float] contendo as notas que não são nulas.
        """

        return {k: v for k, v in self.grades.items() if v is not None}
    
    def get_missing_grades(self) -> list[str]:

        """
        Retorna uma list[str] contendo as variáveis de notas que são nulas.
        """

        return sorted(k for k, v in self.grades.items() if v is None)
    
    def get_status(self) -> str:
        return (
            "[green][APROVADO][/green]" if self.has_passed()
            else "[blue][PENDENTE][/blue]" if len(self.get_missing_grades()) > 0
            else "[red][REPROVADO][/red]"
        )