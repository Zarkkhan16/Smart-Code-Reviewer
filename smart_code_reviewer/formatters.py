"""Output formatters: rich console and JSON."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .report import ReviewReport


def _bar(score: float, width: int = 10) -> str:
    filled = int(round(score * width / 10))
    return "█" * filled + "░" * (width - filled)


def _label(score: float) -> str:
    if score >= 9:
        return "Excellent"
    if score >= 7:
        return "Good"
    if score >= 5:
        return "Fair"
    if score >= 3:
        return "Needs work"
    return "Poor"


def format_rich(reports: list[ReviewReport]) -> None:
    """Print reports to console using rich formatting."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.theme import Theme

    console = Console(theme=Theme({"info": "dim", "warn": "yellow", "err": "red"}))

    for r in reports:
        if r.error and not r.metrics:
            console.print(f"[red]✗[/red] [bold]{r.path}[/bold]: {r.error}")
            continue

        title = f"📄 [bold]{r.path}[/bold]"
        if r.metrics:
            title += f"  [dim]({r.metrics.line_count} lines)[/dim]"
        lines = [title, ""]

        for name, cat in [
            ("Readability", r.readability),
            ("Structure", r.structure),
            ("Maintainability", r.maintainability),
        ]:
            bar = _bar(cat.score)
            label = _label(cat.score)
            lines.append(f"  [bold]{name:16}[/bold]  {bar}  [dim]{label}[/dim]")
            for s in cat.suggestions:
                lines.append(f"    [yellow]→[/yellow] {s}")

        if r.error:
            lines.append("")
            lines.append(f"  [red]Error: {r.error}[/red]")

        text = "\n".join(lines)
        console.print(Panel(text, border_style="blue", padding=(0, 1)))


def format_json(reports: list[ReviewReport]) -> str:
    """Format reports as a single JSON object."""
    return json.dumps(
        {"reports": [r.to_dict() for r in reports]},
        indent=2,
    )
