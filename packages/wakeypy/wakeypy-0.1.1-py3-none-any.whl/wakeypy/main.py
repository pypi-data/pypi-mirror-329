# -*- coding: utf-8 -*-
from typing import Annotated, Optional

import typer

from .functions import keep_presenting, keep_returning, version_callback
from .text_print import running_presenting, running_programs

app = typer.Typer()


# Create -h short name
CONTEXT_SETTING = dict(help_option_names=["-h", "--help"])


@app.command(context_settings=CONTEXT_SETTING)
def main(
    running: Annotated[
        bool,
        typer.Option(
            "-r",
            "--keep-running",
            help="Keep programs running (DEFAULT); inhibit automatic",
            metavar="🥱",
        ),
    ] = False,
    presenting: Annotated[
        bool,
        typer.Option(
            "-p",
            "--keep-presenting",
            help="Display is kept on and automatic screenlock disabled.",
            metavar="😵",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Print out version and exit.",
        ),
    ] = None,
) -> None:
    """
    Wakepy CLI clone.
    """
    if presenting:
        running_presenting()
        keep_presenting()

    elif running:
        running_programs()
        keep_returning()

    else:
        running_programs()
        keep_returning()


if __name__ == "__main__":
    app()
