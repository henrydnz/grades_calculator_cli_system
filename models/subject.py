from utils.types_and_constants import MIN_PASSING_GRADE, Grades

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Subject:
    name: str
    formula: str
    grades: dict[str, Optional[float]] = field(default_factory=dict)

    def to_json(self) -> dict:
        return {
            "formula" : self.formula,
            "notas" : self.grades
        }
    
    @classmethod
    def from_json(cls, name: str, data: dict) -> "Subject":
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
        return {k: v for k, v in self.grades.items() if v is not None}
    
    def get_missing_grades(self):
        return sorted(k for k, v in self.grades.items() if v is None)
    
    def get_status(self) -> str:
        if self.has_passed():
            return "[green][APROVADO][/green]"
        if self.get_missing_grades():
            return "[blue][PENDENTE][/blue]"
        else:
            return "[red][REPROVADO][/red]"
        
    def set_grade(self, var, val):
        self.grades[var] = val
