"""Review report: scores and suggestions for readability, structure, maintainability."""

from __future__ import annotations

from dataclasses import dataclass, field

from .analyzer import (
    FileMetrics,
    HIGH_COMPLEXITY,
    LONG_FUNCTION_LINES,
    MAX_LINE_LENGTH,
)


@dataclass
class CategoryResult:
    """Score (0–10) and list of suggestion strings for one category."""

    score: float
    suggestions: list[str] = field(default_factory=list)


@dataclass
class ReviewReport:
    """Full review for one file."""

    path: str
    readability: CategoryResult
    structure: CategoryResult
    maintainability: CategoryResult
    metrics: FileMetrics | None = None
    error: str | None = None  # e.g. syntax error

    def to_dict(self) -> dict:
        out = {
            "path": self.path,
            "readability": {"score": self.readability.score, "suggestions": self.readability.suggestions},
            "structure": {"score": self.structure.score, "suggestions": self.structure.suggestions},
            "maintainability": {"score": self.maintainability.score, "suggestions": self.maintainability.suggestions},
            "error": self.error,
        }
        if self.metrics:
            out["line_count"] = self.metrics.line_count
        return out


def _score_from_issues(n_issues: int, thresholds: tuple[int, int]) -> float:
    """Map number of issues to 0–10. thresholds = (warning_count, bad_count)."""
    w, b = thresholds
    if n_issues == 0:
        return 10.0
    if n_issues <= w:
        return max(7.0, 10.0 - n_issues * 0.5)
    if n_issues <= b:
        return max(4.0, 7.0 - (n_issues - w) * 0.5)
    return max(0.0, 4.0 - (n_issues - b) * 0.3)


def build_report(metrics: FileMetrics) -> ReviewReport:
    """Convert raw metrics into readability/structure/maintainability scores and suggestions."""
    r_suggestions: list[str] = []
    s_suggestions: list[str] = []
    m_suggestions: list[str] = []

    if metrics.syntax_error:
        return ReviewReport(
            path=metrics.path,
            readability=CategoryResult(0, [f"Syntax error: {metrics.syntax_error}"]),
            structure=CategoryResult(0, []),
            maintainability=CategoryResult(0, []),
            metrics=metrics,
            error=metrics.syntax_error,
        )

    # —— Readability ——
    r_issues = 0
    if metrics.long_line_count > 0:
        r_issues += min(metrics.long_line_count, 5)
        r_suggestions.append(
            f"{metrics.long_line_count} line(s) exceed {MAX_LINE_LENGTH} chars – consider breaking for readability."
        )
    if metrics.line_count > 0:
        comment_ratio = metrics.comment_count / metrics.line_count
        if comment_ratio == 0 and metrics.line_count > 30:
            r_issues += 1
            r_suggestions.append("No comments detected – consider docstrings or key comments for long files.")
        elif comment_ratio > 0.5:
            r_issues += 1
            r_suggestions.append("High comment ratio – ensure code is self-explanatory where possible.")
    readability = CategoryResult(
        score=_score_from_issues(r_issues, (2, 5)),
        suggestions=r_suggestions,
    )

    # —— Structure ——
    s_issues = 0
    long_functions = [f for f in metrics.functions if f["long"] > LONG_FUNCTION_LINES]
    if long_functions:
        s_issues += min(len(long_functions), 3)
        names = [f["name"] for f in long_functions[:3]]
        s_suggestions.append(
            f"Long function(s): {', '.join(names)} – consider splitting into smaller functions."
        )
    if metrics.line_count > 400 and metrics.language == "python":
        s_issues += 1
        s_suggestions.append("Large file – consider splitting into modules or submodules.")
    structure = CategoryResult(
        score=_score_from_issues(s_issues, (1, 3)),
        suggestions=s_suggestions,
    )

    # —— Maintainability ——
    m_issues = 0
    complex_blocks = [f for f in metrics.functions if f["complexity"] >= HIGH_COMPLEXITY]
    if complex_blocks:
        m_issues += min(len(complex_blocks), 4)
        names = [f["name"] for f in complex_blocks[:3]]
        m_suggestions.append(
            f"High cyclomatic complexity in: {', '.join(names)} – simplify branches or extract helpers."
        )
    if metrics.maintainability_index is not None:
        if metrics.maintainability_index < 20:
            m_issues += 2
            m_suggestions.append(
                f"Low maintainability index ({metrics.maintainability_index:.0f}) – refactor for clarity and size."
            )
        elif metrics.maintainability_index < 40:
            m_issues += 1
            m_suggestions.append(
                f"Moderate maintainability index ({metrics.maintainability_index:.0f}) – consider small refactors."
            )
    maintainability = CategoryResult(
        score=_score_from_issues(m_issues, (1, 3)),
        suggestions=m_suggestions,
    )

    return ReviewReport(
        path=metrics.path,
        readability=readability,
        structure=structure,
        maintainability=maintainability,
        metrics=metrics,
    )
