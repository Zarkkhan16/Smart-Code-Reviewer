# Smart Code Reviewer

An AI-ready assistant that reviews code for **readability**, **structure**, and **maintainability** before human review. Run it on files or directories to get actionable feedback.

## Features

- **Readability**: naming, line length, comment ratio, clarity hints
- **Structure**: function/module length, nesting depth, separation of concerns
- **Maintainability**: cyclomatic complexity, maintainability index, duplication cues

Supported languages: **Python** (full analysis). Other languages get basic line-based metrics.

## Install

```bash
pip install -r requirements.txt
```

## Usage

Review current directory (default):

```bash
python -m smart_code_reviewer
```

Review a file or directory:

```bash
python -m smart_code_reviewer -t path/to/file.py
python -m smart_code_reviewer -t path/to/project/
```

Review from stdin (paste code, then Ctrl+D):

```bash
python -m smart_code_reviewer -t -
```

Output formats: default (rich console), or `--json` for machine-readable report.

**Web UI** – paste code and get instant feedback:

```bash
python -m smart_code_reviewer web
# Open http://127.0.0.1:8000
```

## Example output

```
📁 example.py
  Readability   ████████░░  Good – consider shorter lines in 2 places
  Structure     █████████░  Good – 1 long function (45 lines)
  Maintainability ████████░░  Good – 2 blocks with elevated complexity
```

## Deploy (free)

Deploy the web UI to **Render** (free tier):

1. Push this repo to **GitHub** (if not already).
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New** → **Web Service**.
3. Connect your repo and use:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn smart_code_reviewer.app:app --host 0.0.0.0 --port $PORT`
4. Deploy. Your app will be at `https://<your-service-name>.onrender.com`.

Or use the **Blueprint**: connect the repo and Render will read `render.yaml` to create the service.

**Note:** Free tier services spin down after ~15 min idle; the first request after that may take a minute to wake.

## Project layout

- `smart_code_reviewer/` – main package
- `render.yaml` – Render deploy config
- `runtime.txt` – Python version for Render

## License

MIT
