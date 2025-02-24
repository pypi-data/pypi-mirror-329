# -*- coding: utf-8 -*-
"""
Text Print
"""
from art import tprint
from rich.console import Console

console = Console()


def running_programs():
    """
    This will have the text print with the checkmark(X) for "System will continue running".
    """
    tprint("WakeyPy!!!")
    console.print("[green]v.0.1.0")
    print()
    console.print(
        ":white_check_mark: [blue]System will continue running programs.",
    )
    console.print(
        ":x: [strike]Display is kept on and automatic screenlock disabled.[/]",
    )
    print()


def running_presenting():
    """
    This will have system continue running programs AND have screenlock disabled.
    """
    tprint("WakeyPy!!!")
    console.print("[green]v.0.1.0")
    print()
    console.print(
        ":white_check_mark: [bold blue]System will continue running programs.",
    )
    console.print(
        ":white_check_mark: [bold blue]Display is kept on and automatic screenlock disabled.[/]",
    )
    print()
