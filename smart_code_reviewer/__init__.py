"""Smart Code Reviewer – review code for readability, structure, and maintainability."""

__version__ = "0.1.0"

from .review import review_file, review_path
from .report import ReviewReport

__all__ = ["review_file", "review_path", "ReviewReport"]
