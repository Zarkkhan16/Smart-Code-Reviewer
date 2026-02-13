"""Orchestrate analysis and report generation."""

from __future__ import annotations

import sys
from pathlib import Path

from .analyzer import analyze
from .report import CategoryResult, ReviewReport, build_report


def _empty_result() -> CategoryResult:
    return CategoryResult(0, [])


def review_file(file_path: str | Path, source: str | None = None) -> ReviewReport:
    """Review a single file. If source is given, use it; otherwise read from file_path."""
    path = Path(file_path)
    if source is None:
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return ReviewReport(
                path=str(path),
                readability=_empty_result(),
                structure=_empty_result(),
                maintainability=_empty_result(),
                metrics=None,
                error=str(e),
            )
    metrics = analyze(source, str(path))
    return build_report(metrics)


def __empty_result():
    from .report import CategoryResult
    return CategoryResult(0, [])


def review_path(path: str | Path) -> list[ReviewReport]:
    """Review all supported files under path (file or directory)."""
    p = Path(path)
    reports: list[ReviewReport] = []

    if p.is_file():
        if _is_supported(p):
            reports.append(review_file(p))
        return reports

    if p.is_dir():
        for f in sorted(p.rglob("*")):
            if f.is_file() and _is_supported(f):
                reports.append(review_file(f))
    return reports


def _is_supported(file_path: Path) -> bool:
    suffix = file_path.suffix.lower()
    return suffix in (".py", ".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx")


def review_stdin() -> ReviewReport:
    """Read source from stdin and review as <stdin>."""
    source = sys.stdin.read()
    return review_file("<stdin>", source)
