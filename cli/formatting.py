from rich.console import Console
import os

console = Console()

def console_print(s, end="\n") -> None:
    console.print(s, end=end, highlight=False)

def bold(s) -> str:
    return f"[bold]{s}[/bold]"

def title(t: str) -> None:
    clr_scr()
    console_print(f"[bold cyan]{t.upper()}[/bold cyan]\n")

def success(s: str) -> None:
    console_print(f"[bold green]  :) Sucesso:[/bold green] {s}")

def err(s: str) -> None:
    console_print(f"[bold red]  :( Erro:[/bold red] {s}")


def itemize(lst, emphasis=True):
    for i, s in enumerate(lst, 1):
        emphasis_ini = "[bold yellow]" if emphasis else ""
        emphasis_end = "[/bold yellow]" if emphasis else ""
        console_print(f"{emphasis_ini}{i}.{emphasis_end}   {s}") 

def sep() -> None: 
    print("- " * 10)

def format_grade(grade) -> str:
    if grade is None:
        return "[dim]--[/dim]"
    grade = int(grade)
    return f"[red]{grade}[/red]" if grade < 70 else f"[green]{grade}[/green]"

def clr_scr() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def pause() -> None:
    console_print("\n[bold yellow][Enter][/bold yellow][yellow] voltar...[/yellow]\n", end="")
    input()
    clr_scr()