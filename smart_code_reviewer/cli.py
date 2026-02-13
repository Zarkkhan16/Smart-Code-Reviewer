"""CLI for Smart Code Reviewer."""

from __future__ import annotations

from pathlib import Path

import typer

from .formatters import format_json, format_rich
from .review import review_path, review_stdin

app = typer.Typer(
    name="smart-code-reviewer",
    help="Review code for readability, structure, and maintainability.",
    add_completion=False,
)


def _run(target: str, json_out: bool) -> None:
    if target == "-":
        reports = [review_stdin()]
    else:
        path = Path(target)
        if not path.exists() and target != "-":
            typer.echo(f"Error: path does not exist: {target}", err=True)
            raise typer.Exit(1)
        reports = review_path(path)

    if not reports:
        typer.echo("No supported files found.", err=True)
        raise typer.Exit(0)

    if json_out:
        print(format_json(reports))
    else:
        format_rich(reports)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    target: str = typer.Option(
        ".",
        "--target",
        "-t",
        help="File or directory to review, or '-' for stdin.",
    ),
    json_out: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output report as JSON.",
    ),
) -> None:
    """Review code for readability, structure, and maintainability."""
    if ctx.invoked_subcommand is not None:
        return
    _run(target, json_out)


@app.command()
def web(
    port: int = typer.Option(8000, "--port", "-p", help="Port to run the web UI on."),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind."),
) -> None:
    """Start the web UI for paste-and-review."""
    from .app import run_web
    run_web(host=host, port=port)


def run_cli() -> None:
    app()


if __name__ == "__main__":
    run_cli()
