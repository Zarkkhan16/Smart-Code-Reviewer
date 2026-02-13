# Smart Code Reviewer

An AI-ready assistant that reviews code for **readability**, **structure**, and **maintainability** before human review. Run it on files or directories to get actionable feedback.

## Features

- **Readability**: naming, line length, comment ratio, clarity hints
- **Structure**: function/module length, nesting depth, separation of concerns
- **Maintainability**: cyclomatic complexity, maintainability index, duplication cues

Supported languages: **Python** (full analysis). Other languages get basic line-based metrics.


## Example output

```
📁 example.py
  Readability   ████████░░  Good – consider shorter lines in 2 places
  Structure     █████████░  Good – 1 long function (45 lines)
  Maintainability ████████░░  Good – 2 blocks with elevated complexity
```
