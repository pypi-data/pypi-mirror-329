# -*- coding: utf-8 -*-
import itertools
import tempfile
from pathlib import Path

import tomli
import typer
import wakepy
from rich.console import Console

toml = Path("/Users/evanbaird/Projects/Learning/wakeypy/pyproject.toml")


with toml.open(mode="rb") as fp:
    config = tomli.load(fp)


console = Console()


def version_callback(value: bool):
    """
    Version callback.
    """
    if value:
        print(f"Awesome CLI Version: {config['project']['version']} ")
        raise typer.Exit()


def nulling():
    """This function will create an inifinite loop"""
    for _ in itertools.count(1):
        temp = tempfile.TemporaryFile()
        temp.write(b"YARP!")
        temp.close()


def keep_presenting():
    """This function will run keep presenting."""
    try:
        with console.status(
            "[italic green]Staying AWAKE![/] [bold][Press Ctrl+C to exit][/] :sleepy:",
            spinner="smiley",
        ):
            with wakepy.keep.presenting():
                nulling()

    except KeyboardInterrupt:
        console.print("[bold red]Exited[/] :tired_face:")


def keep_returning():
    """This function will run keep returning."""
    try:
        with console.status(
            "[italic red]Staying AWAKE![/] [bold][Press Ctrl+C to exit][/] :dizzy_face:",
            spinner="clock",
        ):
            with wakepy.keep.running():
                nulling()

    except KeyboardInterrupt:
        console.print("[bold red]Exited[/] :drooling_face:")
