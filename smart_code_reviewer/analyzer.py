"""Static analysis for code: complexity, structure, and style metrics."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    HAS_RADON = True
except ImportError:
    HAS_RADON = False


@dataclass
class FileMetrics:
    """Raw metrics for a single file."""

    path: str
    language: str  # "python" | "generic"
    line_count: int = 0
    comment_count: int = 0
    blank_count: int = 0
    max_line_length: int = 0
    long_line_count: int = 0  # lines > 100 chars
    # Python-specific
    functions: list[dict[str, Any]] = field(default_factory=list)  # name, lines, complexity, etc.
    maintainability_index: float | None = None
    syntax_error: str | None = None


# Thresholds
MAX_LINE_LENGTH = 100
LONG_FUNCTION_LINES = 40
HIGH_COMPLEXITY = 10
MAX_NESTING = 4


def _detect_language(path: str | Path) -> str:
    p = Path(path) if isinstance(path, str) else path
    suffix = p.suffix.lower()
    if suffix == ".py":
        return "python"
    if suffix in (".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx"):
        return "javascript"
    return "generic"


def _count_lines_and_lengths(source: str) -> tuple[int, int, int, int, int]:
    """Returns (total, comment, blank, max_line_len, long_line_count)."""
    lines = source.splitlines()
    total = len(lines)
    comment = 0
    blank = 0
    max_len = 0
    long_count = 0
    for line in lines:
        s = line.strip()
        if not s:
            blank += 1
        elif s.startswith("#") or (s.startswith("//") or s.startswith("/*") or s.startswith("*")):
            comment += 1
        length = len(line)
        if length > max_len:
            max_len = length
        if length > MAX_LINE_LENGTH:
            long_count += 1
    return total, comment, blank, max_len, long_count


def analyze_python(source: str, path: str) -> FileMetrics:
    """Run Python-specific analysis (radon + ast)."""
    total, comment, blank, max_len, long_count = _count_lines_and_lengths(source)
    metrics = FileMetrics(
        path=path,
        language="python",
        line_count=total,
        comment_count=comment,
        blank_count=blank,
        max_line_length=max_len,
        long_line_count=long_count,
    )

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        metrics.syntax_error = str(e)
        return metrics

    if HAS_RADON:
        try:
            metrics.maintainability_index = mi_visit(source, True)
        except Exception:
            pass
        for block in cc_visit(source):
            metrics.functions.append({
                "name": block.name,
                "line": block.lineno,
                "complexity": block.complexity,
                "long": getattr(block, "end_line", block.lineno) - block.lineno + 1,
            })
    else:
        # Fallback: no radon – still get function line counts from AST
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end = node.end_lineno if hasattr(node, "end_lineno") else node.lineno
                metrics.functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "complexity": 0,
                    "long": (end - node.lineno + 1) if end else 1,
                })

    return metrics


def analyze_generic(source: str, path: str) -> FileMetrics:
    """Basic metrics for non-Python files."""
    total, comment, blank, max_len, long_count = _count_lines_and_lengths(source)
    return FileMetrics(
        path=path,
        language="generic",
        line_count=total,
        comment_count=comment,
        blank_count=blank,
        max_line_length=max_len,
        long_line_count=long_count,
    )


def analyze(source: str, path: str = "<stdin>") -> FileMetrics:
    """Analyze source code; language inferred from path."""
    lang = _detect_language(path)
    if lang == "python":
        return analyze_python(source, path)
    return analyze_generic(source, path)
