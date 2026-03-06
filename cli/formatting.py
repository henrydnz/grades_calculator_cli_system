"""
Funções de formatação de texto.
"""

from rich.console import Console
import os

console = Console()

def console_print(s, end = "\n") -> None:
    console.print(s, end=end, highlight=False)

def console_input(s) -> str:
    console_print(s, end = "")
    return input()

def bold(s) -> str: 
    return f"[bold]{s}[/bold]"

def success(s) -> None:
    console_print(f"[bold green]  :) Sucesso:[/bold green] {s}")

def err(s) -> None: 
    console_print(f"[bold red]  :( Erro:[/bold red] {s}")

def sep(): 
    console_print(f"[dim]{"-"*30}[/dim]")

def format_grade(grade: float | None) -> str: 
    return (
    "[dim]--[/dim]" if grade is None
    else f"[red]{grade}[/red]" if int(grade) < 70
    else f"[green]{grade}[/green]"
)

def clr_scr() -> None: 
    os.system('cls' if os.name == 'nt' else 'clear')

def title(s) -> None:
    clr_scr()
    console_print(f"[bold blue]{s.upper()}[/bold blue]\n")

def pause() -> None:
    console_input("\n[bold yellow]<== [Enter][/bold yellow]")

