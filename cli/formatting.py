from rich.console import Console
import os

console = Console()


console_print = lambda s, end="\n": console.print(s, end=end, highlight=False)
bold = lambda s: f"[bold]{s}[/bold]"
success = lambda s: console_print(f"[bold green]  :) Sucesso:[/bold green] {s}")
err = lambda s: console_print(f"[bold red]  :( Erro:[/bold red] {s}")
sep = lambda: console_print(f"[dim]{"-"*30}[/dim]")
format_grade = lambda grade: (
    "[dim]--[/dim]" if grade is None
    else f"[red]{grade}[/red]" if int(grade) < 70
    else f"[green]{grade}[/green]"
)
clr_scr = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def title(s):
    clr_scr()
    console_print(f"[bold blue]{s.upper()}[/bold blue]\n")


def pause() -> None:
    console_print("\n[bold yellow][Enter][/bold yellow][yellow] voltar...[/yellow]\n", end="")
    input()